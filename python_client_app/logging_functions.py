import json

import requests

#SERVER_URL = "http://127.0.0.1:80"
SERVER_URL = "http://localhost:5000"
CURR_PROJECT_NAME = ""
CURR_RUN_ID = ""
TOKEN = ""


def log(msg, role_name = "" ):
    # logs msg to server
    print("logging msg to server")
    try:
        print("logging run " + CURR_RUN_ID)
        r = requests.get(
            SERVER_URL + "/log", 
            {
                'run_id': CURR_RUN_ID, 
                'msg': msg, 
                'token': TOKEN,
                'role_name': role_name
            }
        )
        if r.status_code != 200:
            print("Log FAILED. \n" + r.json()['err'])
    except:
        print("Unknown Error in log(msg)")


def start_run(project_name, comment = "", git_commit_url = "" ):
    # starts a new run
    print("starting run")

    global CURR_PROJECT_NAME
    global CURR_RUN_ID

    CURR_PROJECT_NAME = project_name
    try:
        r = requests.get(
            SERVER_URL + "/start_run/" + CURR_PROJECT_NAME, 
                        {
                            'token': TOKEN, 
                            'comment': comment, 
                            'git_commit_url': git_commit_url
                        }
        )

        if r.status_code == 200:
            CURR_RUN_ID = r.json()['id']
            print(CURR_RUN_ID)
        else:
            print("START RUN FAILED. \n" + r.json()['err'])
    except:
        print("Unknown Error in start_run.")


def finish_run():
    # finish current run
    global CURR_RUN_ID
    print("finishing run")
    try:
        print(" finish run run_id " + CURR_RUN_ID)
        r = requests.get(
            SERVER_URL + "/finish_run", 
            {
                'run_id': CURR_RUN_ID, 
                'token': TOKEN
            }
        )
        if r.status_code != 200:
            print("Finish run FAILED. \n" + r.json()['err'])
    except:
        print("Unknown error in finish_run.")


def upload_file(file_name, role_name = "", comment = "" ):
    global CURR_RUN_ID
    try:
        with open(file_name, 'rb') as f:
            #r = requests.post(SERVER_URL + '/upload_file?run_id=' + CURR_RUN_ID + '&token=' + TOKEN,
            r = requests.post(SERVER_URL + '/upload_file',
                              params = {
                                  'run_id' : CURR_RUN_ID,
                                  'token' : TOKEN,
                                  'comment': comment,
                                  'role_name': role_name
                              },
                              files={'file': f}
            )
    except:
        print("Unknown error in upload_file.")


def login(user_id, psw):
    #try:
    global TOKEN
    r = requests.post(
        SERVER_URL + '/login/', 
        json={
            'user_id': user_id, 
            'user_psw_hash': psw
        }
    )
    
    if r.status_code == 200:
        # print(r)
        # print(r.json())
        # token = r.json()['token'].split('.')
        # print(token)
        TOKEN = r.json()['token']
        return True
    else:
        print('Login failed.')
        return False
    #except:
    #    print("Unknown error in login.")
