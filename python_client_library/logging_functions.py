"""
    Client side functions for working with LDM framework.
"""

import json
import requests

#SERVER_URL = "http://127.0.0.1:80"

DEFAULT_SERVER_URL = "http://localhost:5000"

SERVER_URL = DEFAULT_SERVER_URL
CURR_PROJECT_NAME = ""
CURR_RUN_ID = ""
TOKEN = ""


def log(msg, role_name = "" ):    
    """ Log message msg to server.
  
    Parameters: 

    msg (string): Message to log 

    role_name (string): Role name of a message. Role name is optional and can be ommited.
  
    Returns: 

    None  
    """
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
    """ 
    Start a new run.
  
    Parameters: 

    project_name (string): Name of a project this newly started run will belong to.

    comment (string): Comment for a run.  This parameter is optional and can be ommited.

    git_commit_url (string): URL of a git commit representing the state of a code base used in this run. This prm is optional and can be ommited.
  
    Returns: 

    None  
    """
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
    """ 
    Finish the current run.
  
    Parameters: 
  
    Returns: 

    None
  
    """    
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
    """ 
    Upload file (file_name) to the logging server and attaches it to the current run.
  
    Parameters: 

    file_name (string): File path (on a local machine) of file to be uploaded.

    comment (string): Comment for a file to be uploaded.  This prm is optional and can be ommited.

    role_name (string): Role name for a file to be uploaded. This prm is optional and can be ommited.

  
    Returns: 

    None
  
    """    
    global CURR_RUN_ID
    try:
        with open(file_name, 'rb') as f:            
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


def login(user_id, psw, server_url_prm = DEFAULT_SERVER_URL ):
    """ 
    Authorize user user_id with password psw on server server_url_prm.
    
    Parameters: 
    
    user_id (string): User ID.

    psw (string): User password.

    server_url_prm (URL): URL of an instance of LDM framework to connect to. All subsequent calls to LDM framework functions will be directed to this URL. This prm is optional and can be ommited, in this case default URL of "http://localhost:5000" will be used .
  
    Returns: 
    
    True in case of success, False otherwise.  
    """   
    try:
        global TOKEN
        global SERVER_URL
        
        SERVER_URL = server_url_prm

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
    except:
        print("Failed to login ... ")
        print("Unknown error in login.")
