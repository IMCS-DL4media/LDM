import requests 
import json

import os, sys, json, shutil, zipfile
from pathlib import Path
import filecmp

class LDMServer:

    server_url = "http://localhost:5000"
    user_token = None
    
    def __init__(self):
        pass


    #  returns List<Projects>
    def getProjects(self):
        r = requests.get(
                LDMServer.server_url + "/projects",
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        # print(r.json())
        # TODO : check that response was success and all fields are present
        project_list = []
        for prj_json_descr in r.json()["projects"]:
            # print(prj_json_descr)
            proj = Project( prj_json_descr["id"], prj_json_descr["name"] )
            project_list.append(proj)
        return project_list


    def registerUser(self, user_name, user_psw):
        r = requests.post(
                LDMServer.server_url + "/register", 
                json={
                    'email': user_name,
                    'password': user_psw,
                },
                headers={'Content-Type':'application/json', 
                        #  "Authorization": "Bearer " + self.token
                        }
        )

        if (r.status_code == 200):
            print("Succesfully registered user: " + user_name)
            return True
        else:
            return False


    def loginUser(self, user_name, user_psw):
        # send request to login
        r = requests.post(
                LDMServer.server_url + "/login", 
                json={
                    'email': user_name,
                    'password': user_psw,
                },
                headers={'Content-Type':'application/json', 
                        #  "Authorization": "Bearer " + self.token
                        }
        )

        if (r.status_code == 200):
            print("Succesfull login: ")
            LDMServer.user_token = r.json()["response"]["token"]
            print("LDMServer.user_token : ", LDMServer.user_token)
            return True
        else:
            return False

    def createProject(self, project_name, project_description=""):
        r = requests.post(
                LDMServer.server_url + "/project", 
                json={
                    'name': project_name,
                    'type': "ImageClassification",
                    'description': project_description
                },
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )

        if (r.status_code == 200):
            print("Project created succesfully")
            print(r.json())
            proj = Project( r.json()["data"]["id"] , r.json()["data"]["name"])
            return proj
        else:
            return None


class Project:

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def deleteProject(self):
        r = requests.delete(
                LDMServer.server_url + "/project/" + self.id,
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        print(r.json())
        if (r.status_code == 200):
            print("Project deleted succesfully")
            return True
        else:
            return False

    def createRun(self, comment = "", git_commit_url = ""):
        r = requests.post(
                LDMServer.server_url + "/logger/start-run/" + self.id,
                json={
                    'comment': comment,
                    'git_commit_url': git_commit_url,
                },
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        print(r.json())
        if (r.status_code == 200):
            print("Run created succesfully")
            print(r.json())
            run = Run( r.json()["id"], self.id)
            return run
        else:
            return None

    def getRuns(self):
        # /runs/{project_id}
        r = requests.get(
                LDMServer.server_url + "/runs/" + self.id,
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        # print(r.json())
        # TODO : check that response was success and all fields are present
        runs_list = []
        for run_json_descr in r.json()["runs"]:
            print("get_runs")
            print(run_json_descr)
            isFinished = "finish_time" in run_json_descr
            run = Run( run_json_descr["_id"]["$oid"] , self.id, 
                run_json_descr["comment"], 
                run_json_descr["git_commit_url"],
                isFinished)
            runs_list.append(run)
        return runs_list

    def uploadDataSet(self, filePath):
        
        with open(filePath, 'rb') as f:
            r = requests.post(
                LDMServer.server_url + '/upload-training-data/' + self.id ,
                files={'zip_file': f, },
                headers={"Authorization": "Bearer " + LDMServer.user_token}
            )

            if (r.status_code == 200):
                print("Training set uploaded successfully")
                return True
            else:
                print("Training set upload failed")
                return False

    def downloadDataSet(self, target_dir):
        r = requests.get(
                LDMServer.server_url + "/training-set/" + self.id ,
                # params = { 'path' : self.name },
                headers={'Content-Type':'application/json',
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        # print("download_file " + str(r.json()))
        if (r.status_code == 200):
            print(r.headers)
            print(r.headers.get("Content-Disposition"))
            # print(r.headers.get("Content-Disposition"))
            # print(r.json())
            str = r.headers.get("Content-Disposition")
            ind = str.find("filename=")
            if ind != -1:
                file_name = str[ind + len("filename="):]
                print("file_name")
                print(file_name)
                abs_path = os.path.join(target_dir, os.path.basename(file_name))
                print(abs_path)
                with open(abs_path, 'wb') as target:
                    r.raw.decode_content = True
                    for chunk in r.iter_content(chunk_size=128):
                        target.write(chunk)
                print("Download succeded")
                return True
        
        print("Download failed")
        return False


    def __str__(self):
        return 'Project\n\tid: ' + str(self.id) + '\n\tname: ' + str(self.name)


class Run:
    def __init__(self, run_id, project_id, comment="", git_commit_url = "", is_finished = False):
        self.run_id = run_id
        self.project_id = project_id
        self.comment = comment
        self.git_commit_url = git_commit_url
        self.is_finished = is_finished

    def finishRun(self):
        # /logger/finish-run/<project_id>/<run_id>
        r = requests.post(
                LDMServer.server_url + "/logger/finish-run/" + self.project_id + "/" + self.run_id,
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        if (r.status_code == 200):
            print("Run finished succesfully")
            return True
        else:
            return False
    
    def deleteRun(self):
        # /run/{project_id}/{run_id}
        r = requests.delete(
                LDMServer.server_url + "/run/" + self.project_id + "/" + self.run_id,
                headers={'Content-Type':'application/json', 
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        print(r.json())
        if (r.status_code == 200):
            print("Run deleted succesfully")
            return True
        else:
            return False

    def createLogEntry(self, logEntryBody):
        # /logger/log/{project_id}/{run_id}
        r = requests.post(
                LDMServer.server_url + "/logger/log/" + self.project_id + "/" + self.run_id,
                json = {
                    "body":logEntryBody
                },
                headers={
                    'Content-Type':'application/json',
                    "Authorization": "Bearer " + LDMServer.user_token
                }
        )
        if (r.status_code == 200):
            print("Log entry created succesfully")
            # TODO: vai seit nebutu jasanem id ?
            return True
        else:
            return False

    def getLogEntries(self):
        # /run/{project_id}/{run_id}
        r = requests.get(
                LDMServer.server_url + "/run/" + self.project_id + "/" + self.run_id,
                headers={'Content-Type':'application/json',
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        if (r.status_code == 200):
            # print(r.json())
            logs = r.json()["logs"]
            print(logs)
            log_entries_to_return = []
            if logs:
                for log_entry_json in logs:
                    log_entrie = LogEntry( log_entry_json["_id"]["$oid"], log_entry_json["run_id"], log_entry_json["body"])
                    log_entries_to_return.append(log_entrie)
            return log_entries_to_return
        else:
            return None

    def uploadFile(self, filePath, comment = ""):
        with open(filePath, 'rb') as f:
            r = requests.post(
                LDMServer.server_url + '/logger/upload-file/' + self.project_id + "/" + self.run_id,
                files={'file': f, 'data': json.dumps({'comment': comment})},
                headers={"Authorization": "Bearer " + LDMServer.user_token}
            )

            if (r.status_code == 200):
                print("File uploaded successfully")
                return True
            else:
                return False


    def getFiles(self):
        # /run-files/{project_id}/{run_id}
        # r = requests.get(
        #     LDMServer.server_url + '/run-files/' + self.project_id + "/" + self.run_id,
        #     headers={"Authorization": "Bearer " + LDMServer.user_token}
        # )
        # print("run_files " + str(r.json()))
        # TODO : lauks files:[] ir tukss 
        # skatoties uz DB izskatas, ka uploadotie faili tiek pieregistreti ieks log kolekcijas ar type:file
        # izskatas ka bugs
        # btw si pati problema ir ari ar log entries; atlasot log entries tiek atlasiti ari entries ar failiem
        
        # tas ko seit var darit sanemt logs tapat ka tas tiek darits ieks getLogEntries
        # tad filtret pec type = file , un sadi dabut ierakstus kas atbilst failiem
        # if (r.status_code == 200):
        #     files = r.json()["files"]
        #     print(files)
        #     file_entries_to_return = []
        #     if files:
        #         for file_entry_json in files:
        #             log_entrie = FileEntry( 
        #                                     file_entry_json["_id"]["$oid"], 
        #                                     file_entry_json["run_id"], 
        #                                     file_entry_json["body"]
        #                                 )
        #             file_entries_to_return.append(log_entrie)
        #     return file_entries_to_return
        # else:
        #     return None
        r = requests.get(
                LDMServer.server_url + "/run/" + self.project_id + "/" + self.run_id,
                headers={'Content-Type':'application/json',
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        print("get_files " + str(r.json()))
        if (r.status_code == 200):
            # print(r.json())
            logs = r.json()["logs"]
            print(logs)
            file_entries_to_return = []
            if logs:
                for log_entry_json in logs:
                    logEntryRepresentsFile = "type" in log_entry_json and log_entry_json["type"] == "file"
                    if logEntryRepresentsFile:
                        file_entry = FileEntry( self.project_id,
                                                log_entry_json["_id"]["$oid"], 
                                                log_entry_json["run_id"],
                                                
                                                log_entry_json["body"]["file_name"],
                                                log_entry_json["body"]["file_path"],
                                                log_entry_json["body"]["comment"]
                                            )
                        file_entries_to_return.append(file_entry)
            return file_entries_to_return
        else:
            return None

    def uploadSourceCodeFile(self):
        # /source-code/{project_id}/{run_id}
        # root_dir = "."
        # # making tmp zip file of the source dir and its subdirs, then posting is as logger_zip.zip
        # zf_path = os.path.join(Path(root_dir).parent, "logger_zip.zip")
        # zf = zipfile.ZipFile(zf_path, "w")

        # for root, dirs, files in os.walk(root_dir):
        #     for file in files:
        #         zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(root_dir, '..')))
        # zf.close()

        r = None
        with open("./logger_zip.zip", 'rb') as f:
            r = requests.post(LDMServer.server_url + '/logger/source-code/' + self.project_id + "/" + self.run_id,
                                files={'file': f,},
                                headers={"Authorization": "Bearer " + LDMServer.user_token}
                            )
        print("source code" + str(r.json()))
        if (r.status_code == 200):
            print("Source code uploaded successfully.")
            return []
        else:
            return None

    def downloadSourceCode(self, target_dir):
        r = requests.get(
                LDMServer.server_url + "/source-code/" + self.project_id + "/" + self.run_id,
                # params = { 'path' : self.name },
                headers={'Content-Type':'application/json',
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        print("download_file : " )
        print(str(r.raw))
        if (r.status_code == 200):
            print(r.headers)
            print(r.headers.get("Content-Disposition"))
            # print(r.headers.get("Content-Disposition"))
            # print(r.json())
            with open(os.path.join(target_dir, "zipped_sources.zip"), 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            # header_content = r.headers.get("Content-Disposition")
            # ind = header_content.find("filename=")
            # if ind != -1:
            #     file_name = header_content[ind + len("filename="):]
            #     print(file_name)
            #     abs_path = os.path.join(target_dir, os.path.basename(file_name))
            #     with open(abs_path, 'wb') as target:
            #         r.raw.decode_content = True
            #         for chunk in r.iter_content(chunk_size=128):
            #             target.write(chunk)
                print("Download succeded")
                return True
        #Izskatas, ka sobrid nem tikai failu ar vardu logger_zip.zip
        # Augsupieladet source var ar patvaligo arhiva vardu, bet downloadet var tikai "logger_zip.zip"
        print("Download sources failed")
        return False

    def getSourceCodeFiles(self):
        r = requests.get(
            LDMServer.server_url + '/run-files/' + self.project_id + "/" + self.run_id,
            headers={"Authorization": "Bearer " + LDMServer.user_token}
        )
        print( "source code files", r.json() )
        if (r.status_code == 200):
            return []
        else:
            return None

    def __str__(self):
        return 'Run\n\tid: ' + str(self.run_id) + '\n'


class LogEntry:
    def __init__(self, log_entry_id, run_id, body):
        self.log_entry_id = log_entry_id
        self.run_id = run_id
        self.body = body

    def __str__(self):
        return 'LogEntry\n\tid: ' +str(self.log_entry_id) + '\n\trunid: ' + str(self.run_id) + '\n\t' + str(self.body) + "\n"

class FileEntry:
    def __init__(self, project_id, log_entry_id, run_id, name, path, comment):
        self.project_id = project_id
        self.log_entry_id = log_entry_id
        self.run_id = run_id
        self.name = name
        self.path = path
        self.comment = comment

    def __str__(self):
        return 'FileEntry\n\tid: ' +str(self.log_entry_id) + '\n\trunid: ' + str(self.run_id) + '\n\t' + str(self.name) +  '\n\t' + str(self.path) +  '\n\t' + str(self.comment) + "\n"
    
    def downloadFile(self, target_dir):
        r = requests.get(
                LDMServer.server_url + "/logged-file/" + self.project_id + "/" + self.run_id,
                params = { 'path' : self.name },
                headers={'Content-Type':'application/json',
                         "Authorization": "Bearer " + LDMServer.user_token
                        }
        )
        # print("download_file " + str(r.json()))
        if (r.status_code == 200):
            print(r.headers)
            print(r.headers.get("Content-Disposition"))
            # print(r.headers.get("Content-Disposition"))
            # print(r.json())
            str = r.headers.get("Content-Disposition")
            ind = str.find("filename=")
            if ind != -1:
                file_name = str[ind + len("filename="):]
                print(file_name)
                abs_path = os.path.join(target_dir, os.path.basename(file_name))
                with open(abs_path, 'wb') as target:
                    r.raw.decode_content = True
                    for chunk in r.iter_content(chunk_size=128):
                        target.write(chunk)
                print("Download succeded")
                return True
        
        print("Download failed")
        return False


def clearDB(srv, userName, psw):
    if srv.loginUser(userName, psw):
        projects = srv.getProjects()
        if projects != None:
            for prj in projects:
                print("Deleting project: " + prj.id)
                prj.deleteProject()


from pymongo import MongoClient


def dropLoggingDB():
    client = MongoClient('localhost', port=27017)
    client.drop_database("logging_db")

def main():

    # dropLoggingDB()
    run_tests()
    return

    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    clearDB(srv, user_name, psw)

    if srv.loginUser("u2", "u2"):
        print("Login successfull")
        proj1 = srv.createProject("project1")
        run1 = proj1.createRun()
        run1.createLogEntry({"msg":"my first msg", "msg_type":"LogEntry"})
        run1.createLogEntry({"msg":"my second msg", "msg_type":"LogEntry"})
        run1.uploadFile("abc.txt")
        run1.uploadSourceCodeFile()
        run1.finishRun()

        run2 = proj1.createRun()
        run2.finishRun()

    if srv.loginUser("u2", "u2"):
        print("Login successfull")
        projects = srv.getProjects()
        print("<projects>")
        if projects != None:
            for prj in projects:
                print(prj)
                runs = prj.getRuns()
                if runs != None:
                    for run in runs:
                        print(run)
                        logs = run.getLogEntries()
                        if logs != None:
                            for log in logs:
                                print(log)
                        
                        files = run.getFiles()
                        sources = run.getSourceCodeFiles()
                # prj.createRun()

        print("</projects>")
    
def run_tests():
    # dropLoggingDB()
    # test_create_project()
    # dropLoggingDB()
    # test_start_run()
    # dropLoggingDB()
    # test_finish_run()
    # dropLoggingDB()
    # test_create_log_entry()
    # dropLoggingDB()
    # test_upload_file()
    # dropLoggingDB()
    # test_upload_source_code_file()
    dropLoggingDB()
    test_upload_download_dataset()


def test_create_project():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    clearDB(srv, user_name, psw)

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    assert projects[0].name == prjName 
    # assert projects[0].description == prjDescr


def test_start_run():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    # get project runs ; assure it is empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 0 

    # create run 
    comment = "comment"
    git_commit_url = "http://example.com"
    prj.createRun(comment, git_commit_url)

    # get project runs ; assure it is not empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is not finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    # TODO vel seit varetu parbaudit vai nav finished un paskatitties uz start time


def test_finish_run():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    # get project runs ; assure it is empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 0 

    # create run 
    comment = "comment"
    git_commit_url = "http://example.com"
    prj.createRun(comment, git_commit_url)

    # get project runs ; assure it is not empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is not finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    assert run.is_finished == False
    
    run.finishRun()

    prjRuns = prj.getRuns()
    
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    assert run.is_finished == True


def test_create_log_entry():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    # get project runs ; assure it is empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 0 

    # create run 
    comment = "comment"
    git_commit_url = "http://example.com"
    prj.createRun(comment, git_commit_url)

    # get project runs ; assure it is not empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is not finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    
    log_entries = run.getLogEntries()
    assert log_entries is not None and len(log_entries) == 0

    run.createLogEntry({"msg":"text", "msg_type":"type"})

    log_entries = run.getLogEntries()
    assert log_entries is not None and len(log_entries) == 1
    log_e = log_entries[0]
    assert log_e is not None
    assert log_e.run_id == run.run_id
    assert "msg" in log_e.body and "msg_type" in log_e.body
    assert log_e.body["msg"] == "text" and log_e.body["msg_type"] == "type"
    # print( log_e.body ) 

def test_upload_file():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    # get project runs ; assure it is empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 0 

    # create run 
    comment = "comment"
    git_commit_url = "http://example.com"
    prj.createRun(comment, git_commit_url)

    # get project runs ; assure it is not empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is not finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    
    files = run.getFiles()
    assert files is not None and len(files) == 0

    run.uploadFile("./abc.txt","comment123")
    files = run.getFiles()
    assert files is not None and len(files) == 1
    assert files[0].name == "abc.txt" and files[0].comment == "comment123"
    print(files[0])
    target_dir = "./downloaded_files"
    files[0].downloadFile(target_dir)
    # compare files from ./abc.txt and ./downloaded_files/abc.txt
    assert filecmp.cmp('./abc.txt', os.path.join(target_dir ,  files[0].name ))
    

def test_upload_source_code_file():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    
    

    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)
    
    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    # get project runs ; assure it is empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 0 

    # create run 
    comment = "comment"
    git_commit_url = "http://example.com"
    prj.createRun(comment, git_commit_url)

    # get project runs ; assure it is not empty 
    prjRuns = prj.getRuns()
    assert prjRuns is not None and len(prjRuns) == 1 

    # get created run and assure is has actual properties; and is not finished
    run = prjRuns[0]
    assert run is not None 
    assert run.comment == comment and run.git_commit_url == git_commit_url
    
    files = run.getFiles()
    assert files is not None and len(files) == 0

    run.uploadFile("./abc.txt","comment123")
    files = run.getFiles()
    assert files is not None and len(files) == 1
    assert files[0].name == "abc.txt" and files[0].comment == "comment123"
    print(files[0])
    target_dir = "./downloaded_files"
    files[0].downloadFile(target_dir)
    # compare files from ./abc.txt and ./downloaded_files/abc.txt
    assert filecmp.cmp('./abc.txt', os.path.join(target_dir ,  files[0].name ))
    run.uploadSourceCodeFile()

    run.downloadSourceCode(target_dir)
    # compare files from ./abc.txt and ./downloaded_files/abc.txt
    assert filecmp.cmp('./sources_to_upload.zip', os.path.join(target_dir ,  "zipped_sources.zip" ))
    

def test_upload_download_dataset():
    srv = LDMServer()
    user_name = "u2"
    psw = "u2"
    srv.registerUser(user_name, psw)
    


    assert srv.loginUser("u2", "u2")
    
    # get list of projects 
    # assert that list is empty
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 0
    
    # create project 
    prjName = "name1"
    prjDescr = "descr1"
    
    srv.createProject(prjName, prjDescr)

    # get list of projects
    # assert list not empty and new projects has all according properties
    projects = srv.getProjects()
    assert projects is not None and len(projects) == 1
    prj = projects[0]
    assert prj.name == prjName
    # assert prj.description == prjDescr

    prj.uploadDataSet("./animals_train.zip")

    target_dir = "./downloaded_files/"
    prj.downloadDataSet(target_dir)
    assert filecmp.cmp("./animals_train.zip", os.path.join( target_dir, "animals_train.zip") )


main()