#!/usr/bin/env python
import os, datetime, json, jwt, sys


if sys.version_info[:2] >= (3, 8):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping




# from bson import ObjectId
from flask import Flask, render_template, request, jsonify, make_response
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from bson.json_util import dumps

from functools import wraps
import auth, users, projects, runs, datasets
import utilities as u


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-string12345reqfgb'
app.config["MONGO_URI"] = "mongodb://mongo:27017/logging_db"


data_collection_map = {"Train": "training_data", "Validate": "validation_data", "Test": "test_data",}
silvers_datasets_map = {"Train": "silvers_train", "Validate": "silvers_validate", "Test": "silvers_test",}


mongo = PyMongo(app)

Auth = auth.Auth(mongo, app)
Users = users.Users(mongo, app, Auth)

Projects = projects.Projects(mongo, app)
Runs = runs.Runs(mongo, app)
Datasets = datasets.Datasets(mongo, app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user1(user_id):
    user = auth.User(mongo, app)
    user.select_logged_in_user_by_id(user_id)

    return user

@login_manager.request_loader
def load_user2(request):
    token = request.headers.get('Authorization')
    token_obj = Auth.get_token(request)
    
    if (token_obj["status"] == 200):
        token = token_obj["token"]
        resp = Auth.decode_auth_token(token)
        if resp and resp["status"]:
            user_id = resp["id"]
            user = auth.User(mongo, app)
            user.select_logged_in_user_by_id(user_id)

            return user

    return None


def require_role(f):
    @wraps(f)
    def wrap(project_id, *args, **kwargs):
        if (current_user.check_access_rights_to_project(project_id)):
            return f(project_id, *args, **kwargs)
        else:
            return None
            # return "very bad", 401

    return wrap


def require_token_and_project(f):
    @wraps(f)
    def wrap(project_id, *args, **kwargs):
        header = request.headers.get('Authorization')
        if (header):
            token = header.split(" ")[-1]
            user = auth.User(mongo, app)
            if (user.check_token_and_project(token, project_id)):
                return f(project_id, *args, **kwargs)
            else:
                return "very bad", 401

        else:
            return "No header", 401

    return wrap


@app.route('/')
def hello_world():
    return jsonify({'status': 200, 'msg': "Super cool app is running..."})


@app.route('/logger/start-run/<project_id>', methods=['POST'])
@require_token_and_project
def start_run(project_id):
    data_in = request.get_json(force=True)
    user = get_user()
    return Runs.start_run(project_id, data_in, user)


@app.route('/logger/finish-run/<project_id>/<run_id>', methods=['POST'])
@require_token_and_project
def finish_run(project_id, run_id):
    return Runs.finish_run(project_id, run_id)


@app.route('/logger/log/<project_id>/<run_id>', methods=['POST'])
@require_token_and_project
def log(project_id, run_id):
    data_in = request.get_json(force=True)
    return Runs.log(project_id, run_id, data_in)


@app.route("/logger/chart/<project_id>", methods=["POST"])
@login_required
@require_role
def add_project_chart(project_id):
    data_in = request.get_json(force=True)
    return Projects.add_project_chart(project_id, data_in)


@app.route('/logger/log-charts/<project_id>/<run_id>', methods=['POST'])
# @require_token_and_project
def log_charts(project_id, run_id):
    data_in = request.get_json(force=True)
    return Runs.log_charts(project_id, run_id, data_in)


@app.route('/logger/log-chart/<chart_id>/<project_id>/<run_id>', methods=['DELETE'])
# @require_token_and_project
def delete_log_chart(chart_id, project_id, run_id):
    return Projects.delete_log_charts(chart_id, project_id, run_id)



@app.route('/logger/upload-file/<project_id>/<run_id>', methods=['POST'])
@require_token_and_project
def upload_logger_file(project_id, run_id):
    file = request.files['file']
    data_in = json.loads(request.files['data'].read())
    return Runs.upload_file(project_id, run_id, data_in, file)


@app.route('/logger/source-code/<project_id>/<run_id>', methods=['POST'])
@require_token_and_project
def upload_logger_source_code(project_id, run_id):
    file = request.files['file']
    return Runs.upload_source_files(project_id, run_id, file)


@app.route('/logger/project', methods=['POST'])
def add_logger_project():
    header = request.headers.get('Authorization')
    if (header):
        token = header.split(" ")[-1]
        user = auth.User(mongo, app)
        user_obj = user.get_user_by_token(token)
        if (user_obj):
            data_in = request.get_json(force=True)
            return Projects.add_logger_project(data_in, user_obj)
        else:
            return "very bad", 401
    else:
        return "No header", 401



@app.route('/logger/dataset/<project_id>/<dataset_type>', methods=['POST'])
@require_token_and_project
def upload_logger_dataset(project_id, dataset_type):
    dataset_type = (dataset_type).lower()
    if (dataset_type == "train"):
        return Datasets.upload_training_data(project_id)
    elif (dataset_type == "validation"):
        return Datasets.upload_validation_data(project_id)
    elif (dataset_type == "test"):
        return Datasets.upload_testing_data(project_id)
    else:
        return "Incorrect dataset type", 500


@app.route('/logger/dataset/<project_id>/<dataset_type>')
@require_token_and_project
def download_logger_dataset(project_id, dataset_type):
    dataset_type = (dataset_type).lower()
    if (dataset_type == "train"):
        return Datasets.get_training_set(project_id)
    elif (dataset_type == "validation"):
        return Datasets.get_validation_set(project_id)
    elif (dataset_type == "test"):
        return Datasets.get_testing_set(project_id)
    else:
        return "Incorrect dataset type", 500




@app.route('/logger/validate/<project_id>', methods=['POST'])
@require_token_and_project
def logger_validate(project_id):
    data_in = request.get_json(force=True)

    data_collection_map = {"Train": "all_data", "Validate": "all_data", "Test": "all_data",}
    # data_collection_map = {"Train": "training_data", "Validate": "validation_data", "Test": "test_data",}
    silvers_datasets_map = {"Train": "silvers_train", "Validate": "silvers_validate", "Test": "silvers_test",}

    silvers_dataset_name = silvers_datasets_map[data_in["type"]]

    print ("silvers_dataset_name ", silvers_dataset_name)

    file_names = []
    files_map = {}

    for item in data_in["results"]:
        file_names.append(item["file"])
        files_map[item["file"]] = item

    data_collection = data_collection_map[data_in["type"]]
    file_collection = mongo.db[data_collection].find({"project_id": project_id, "uploaded_file_name": {"$in": file_names}})




    silvers = []
    for gold_item in list(file_collection):

        print ("gold_item ", gold_item)


        gold = gold_item["gold"]
        silver = files_map[gold_item["uploaded_file_name"]]["silver"]

        print ("gold ", gold)
        print ("silver", silver)

        res = 0
        if (gold == silver):
            res = 1

        silver = {"gold_id": str(gold_item["_id"]),
                    "src": gold_item["src"],
                    "uploaded_file_name": gold_item["uploaded_file_name"],
                    "project_id": project_id,
                    "run_id": data_in["run_id"],
                    "created_at": datetime.datetime.utcnow(),
                    # "type": gold_item["type"],
                    "type": data_in["type"],
                    "gold": gold,
                    "silver": silver,
                    "result": res,
                }
        silvers.append(silver)


    print ("silvers ", silvers)

    if (len(silvers) > 0):

        print ("inserted silvers")
        print (silvers)
        print ("")

        print ("silvers_dataset_name ", silvers_dataset_name)


        mongo.db[silvers_dataset_name].insert_many(silvers)


    return make_response(dumps({"aa": 22,}))




@app.route('/logger/production-result/<project_id>/<model_id>', methods=['POST'])
@require_token_and_project
def upload_logger_production_result(project_id, model_id):
    file = request.files['file']
    data_in = json.loads(request.files['data'].read())

    print ("file ", file)
    print ("data in ", data_in)


    return Datasets.store_production_result(project_id, model_id, data_in, file)








# this is a tmp route 
@app.route('/clean-predefined-datasets')
# @require_user_token
def clean_dataset():
    mongo.db.predefined_datasets.delete_many({})
    mongo.db.predefined_training_data.delete_many({})
    mongo.db.predefined_dataset_labels.delete_many({})

    return make_response(dumps({"aa": 23,}))





@app.route('/projects')
@login_required
def get_projects():
    return Projects.get_projects()


@app.route('/active-project/<project_id>')
@login_required
def get_active_project(project_id):
    return Projects.get_active_project(project_id)


@app.route('/project', methods=['POST'])
@login_required
def create_new_project():
    data_in = json.loads(request.data.decode("utf-8"))
    return Projects.create_new_project(data_in, current_user.get_id(), current_user.get_email())


@app.route('/project/<project_id>', methods=['DELETE'])
@login_required
@require_role
def delete_project(project_id):
    return Projects.delete_project(project_id)


@app.route('/runs/<project_id>')
@login_required
@require_role
def get_runs(project_id):
    return Runs.get_runs(project_id)


@app.route('/run/<project_id>/<run_id>')
@login_required
@require_role
def get_run(project_id, run_id):
    return Runs.get_run(project_id, run_id)


@app.route('/run-files/<project_id>/<run_id>')
@login_required
@require_role
def get_run_files(project_id, run_id):
    return Runs.get_run_files(project_id, run_id)


@app.route('/source-code/<project_id>/<run_id>')
@login_required
@require_role
def get_source_code_files(project_id, run_id):
    return Runs.get_source_code_files(project_id, run_id)



@app.route('/upload', methods=['POST'])
@login_required
def upload():
    return Datasets.upload()


@app.route('/upload-all-object-detection-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_object_detection_dataset(project_id):
    print("upload_object_detection_dataset", project_id)
    return Datasets.upload_object_detection_dataset(project_id, "All")


@app.route('/upload-all-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_all_data(project_id):
    print("upload_all_data1", project_id)
    return Datasets.upload_all_data(project_id)


@app.route('/upload-training-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_training_data(project_id):
    print("upload_training_data")
    return Datasets.upload_training_data(project_id)


@app.route('/upload-test-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_testing_data(project_id):
    return Datasets.upload_testing_data(project_id)


@app.route('/upload-validation-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_validation_data(project_id):
    return Datasets.upload_validation_data(project_id)



@app.route('/upload-all-file/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_all_file(project_id):
    return Datasets.upload_file(project_id, "All")


@app.route('/upload-training-file/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_training_file(project_id):
    return Datasets.upload_file(project_id, "Train")


@app.route('/upload-validation-file/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_validation_file(project_id):
    return Datasets.upload_file(project_id, "Validation")


@app.route('/upload-testing-file/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_testing_file(project_id):
    return Datasets.upload_file(project_id, "Test")


@app.route('/upload-data/<project_id>', methods=['POST'])
@login_required
@require_role
def upload_data(project_id):
    return Datasets.upload_data(project_id)






@app.route('/file-body/<project_id>/<run_id>')
@login_required
def get_file_body(project_id, run_id):
    return Runs.get_file_body(project_id, run_id, request.args.get('path'))


@app.route('/logged-file-body/<project_id>/<run_id>')
@login_required
def get_logged_file_body(project_id, run_id):
    return Runs.get_logged_file_body(project_id, run_id, request.args.get('path'))


@app.route('/logged-file/<project_id>/<run_id>')
@login_required
def download_logged_file(project_id, run_id):
    return Runs.download_logged_file(project_id, run_id, request.args.get('path'))




# @app.route('/get_file/<name>')
# @login_required
# def get_file(name):
#     return Datasets.get_file(name)

@app.route('/all-dataset-file/<project_id>/<name>')
@login_required
# @require_role
def get_all_file(project_id, name):
    return Datasets.get_all_file(project_id, name)


@app.route('/training-dataset-file/<project_id>/<name>')
@login_required
# @require_role
def get_training_file(project_id, name):
    return Datasets.get_training_file(project_id, name)


@app.route('/validation-dataset-file/<project_id>/<name>')
@login_required
# @require_role
def get_validation_file(project_id, name):
    return Datasets.get_validation_file(project_id, name)


@app.route('/testing-dataset-file/<project_id>/<name>')
@login_required
# @require_role
def get_testing_file(project_id, name):
    return Datasets.get_testing_file(project_id, name)



@app.route('/production-file/<project_id>/<name>')
@login_required
# @require_role
def get_production_file(project_id, name):
    return Datasets.get_production_file(project_id, name)


@app.route('/all-dataset-file-gold-transcription/<project_id>/<media_id>')
@login_required
@require_role
def get_gold_all_media_transcription(project_id, media_id):
    return Datasets.get_gold_media_transcription(project_id, media_id, "All")


@app.route('/training-dataset-file-gold-transcription/<project_id>/<media_id>')
@login_required
@require_role
def get_gold_training_media_transcription(project_id, media_id):
    return Datasets.get_gold_media_transcription(project_id, media_id, "Train")


@app.route('/testing-dataset-file-gold-transcription/<project_id>/<media_id>')
@login_required
@require_role
def get_gold_test_media_transcription(project_id, media_id):
    return Datasets.get_gold_media_transcription(project_id, media_id, "Test")


@app.route('/validation-dataset-file-gold-transcription/<project_id>/<media_id>')
@login_required
@require_role
def get_gold_validation_media_transcription(project_id, media_id):
    return Datasets.get_gold_media_transcription(project_id, media_id, "Validation")



@app.route('/training-dataset-file-silver-transcription/<project_id>/<run_id>/<media_id>')
@login_required
@require_role
def get_silver_training_media_transcription(project_id, run_id, media_id):
    return Datasets.get_silver_media_transcription(project_id, media_id, run_id, "Train")


@app.route('/testing-dataset-file-silver-transcription/<project_id>/<run_id>/<media_id>')
@login_required
@require_role
def get_silver_test_media_transcription(project_id, run_id, media_id):
    return Datasets.get_silver_media_transcription(project_id, media_id, run_id, "Test")


@app.route('/validation-dataset-file-silver-transcription/<project_id>/<run_id>/<media_id>')
@login_required
@require_role
def get_silver_validation_media_transcription(project_id, run_id, media_id):
    return Datasets.get_silver_media_transcription(project_id, media_id, run_id, "Validation")



@app.route('/training-set/<project_id>')
@login_required
@require_role
def get_training_set(project_id):
    return Datasets.get_training_set(project_id)


@app.route('/test-set/<project_id>')
@login_required
@require_role
def get_testing_set(project_id):
    return Datasets.get_testing_set(project_id)


@app.route('/validation-set/<project_id>')
@login_required
@require_role
def get_validation_set(project_id):
    return Datasets.get_validation_set(project_id)


@app.route('/public-datasets')
def get_public_datasets():
    return Datasets.get_public_datasets()

@app.route('/public-dataset/<dataset>/<dataset_type>/<page>')
def get_public_dataset(dataset, dataset_type, page):
    return Datasets.get_public_dataset(dataset, dataset_type, page)


@app.route('/public-image/<dataset>/<dataset_type>/<name>')
def get_public_dataset_image(dataset, dataset_type, name):
    return Datasets.get_public_dataset_image(dataset, dataset_type, name)


@app.route('/gold-all-data/<project_id>/<page>')
@login_required
@require_role
def get_gold_all_data(project_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_gold_all_data(project_id, page, exclude, match)



@app.route('/gold-training-data/<project_id>/<page>')
@login_required
@require_role
def get_gold_training_data(project_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_gold_training_data(project_id, page, exclude, match)

@app.route('/gold-test-data/<project_id>/<page>')
@login_required
@require_role
def get_gold_testing_data(project_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_gold_testing_data(project_id, page, exclude, match)

@app.route('/gold-validation-data/<project_id>/<page>')
@login_required
@require_role
def get_gold_validation_data(project_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_gold_validation_data(project_id, page, exclude, match)



@app.route('/silver-training-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_silver_training_data(project_id, run_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_silver_training_data(project_id, run_id, page, exclude, match)

@app.route('/silver-test-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_silver_testing_data(project_id, run_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_silver_testing_data(project_id, run_id, page, exclude, match)

@app.route('/silver-validation-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_silver_validation_data(project_id, run_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_silver_validation_data(project_id, run_id, page, exclude, match)



# @app.route('/training-data/<project_id>/<run_id>/<page>')
# @login_required
# @require_role
# def get_training_data(project_id, run_id, page):
#     exclude, match = get_exclude_match(request)
#     return Datasets.get_training_data(project_id, run_id, page, exclude, match)

# @app.route('/test-data/<project_id>/<run_id>/<page>')
# @login_required
# @require_role
# def get_testing_data(project_id, run_id, page):
#     exclude, match = get_exclude_match(request)
#     return Datasets.get_testing_data(project_id, run_id, page, exclude, match)

# @app.route('/validation-data/<project_id>/<run_id>/<page>')
# @login_required
# @require_role
# def get_validation_data(project_id, run_id, page):
#     exclude, match = get_exclude_match(request)
#     return Datasets.get_validation_data(project_id, run_id, page, exclude, match)


def get_exclude_match(request):
    exclude = request.args.get('exclude', default=None, type=str)
    match = request.args.get('match', default="all", type=str)

    return exclude, match


@app.route('/production-data/<project_id>/<model_id>/<page>')
@login_required
@require_role
def get_production_data(project_id, model_id, page):
    exclude, match = get_exclude_match(request)
    return Datasets.get_production_data(project_id, model_id, page, exclude, match)



@app.route('/training-media-gold-data/<project_id>/<page>')
@login_required
@require_role
def get_training_media_gold_data(project_id, page):
    return Datasets.get_media_gold_data(project_id, page, "Train")

@app.route('/test-media-gold-data/<project_id>/<page>')
@login_required
@require_role
def get_testing_media_gold_data(project_id, page):
    return Datasets.get_media_gold_data(project_id, page, "Test")

@app.route('/validation-media-gold-data/<project_id>/<page>')
@login_required
@require_role
def get_validation_media_gold_data(project_id, page):
    return Datasets.get_media_gold_data(project_id, page, "Validation")



@app.route('/training-media-silver-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_training_media_data(project_id, run_id, page):
    return Datasets.get_media_silver_data(project_id, run_id, page, "Train")

@app.route('/test-media-silver-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_testing_media_data(project_id, run_id, page):
    return Datasets.get_media_silver_data(project_id, run_id, page, "Test")

@app.route('/validation-media-silver-data/<project_id>/<run_id>/<page>')
@login_required
@require_role
def get_validation_media_data(project_id, run_id, page):
    return Datasets.get_media_silver_data(project_id, run_id, page, "Validation")





@app.route('/all-dataset-file-gold-transcription/<project_id>/<id>', methods=['PUT'])
@login_required
@require_role
def update_all_gold_dataset_item(project_id, id):
    data_in = json.loads(request.data.decode("utf-8"))
    return Datasets.update_item(project_id, id, data_in, "All")


@app.route('/training-dataset-file-gold-transcription/<project_id>/<id>', methods=['PUT'])
@login_required
@require_role
def update_training_gold_dataset_item(project_id, id):
    data_in = json.loads(request.data.decode("utf-8"))
    return Datasets.update_item(project_id, id, data_in, "Train")


@app.route('/validation-dataset-file-gold-transcription/<project_id>/<id>', methods=['PUT'])
@login_required
@require_role
def update_validation_gold_dataset_item(project_id, id):
    data_in = json.loads(request.data.decode("utf-8"))
    return Datasets.update_item(project_id, id, data_in, "Validation")


@app.route('/testing-dataset-file-gold-transcription/<project_id>/<id>', methods=['PUT'])
@login_required
@require_role
def update_test_gold_dataset_item(project_id, id):
    data_in = json.loads(request.data.decode("utf-8"))
    return Datasets.update_item(project_id, id, data_in, "Test")







@app.route('/all-dataset-file/<project_id>/<id>', methods=['DELETE'])
@login_required
@require_role
def delete_training_dataset_item(project_id, id):
    return Datasets.delete_item(project_id, id, "training_data")


@app.route('/validation-dataset-file/<project_id>/<id>', methods=['DELETE'])
@login_required
@require_role
def delete_validation_dataset_item(project_id, id):
    return Datasets.delete_item(project_id, id, "validation_data")


@app.route('/testing-dataset-file/<project_id>/<id>', methods=['DELETE'])
@login_required
@require_role
def delete_test_dataset_item(project_id, id):
    return Datasets.delete_item(project_id, id, "test_data")



@app.route('/user-profile')
@login_required
def get_current_user_profile():
    return Users.get_current_user_profile()


@app.route('/user-token', methods=['PUT'])
@login_required
def update_user_token():
    return Users.update_token()


@app.route('/register', methods=["POST"])
def register_user():
    data_in = json.loads(request.data.decode("utf-8"))
    Users.add_user(data_in)

    return jsonify(**{"status": 200, "response": []})


@app.route('/login', methods=["POST", "GET"])
def post_login_user():
    data_in = request.get_json(force=True)

    email = data_in['email']
    password = data_in['password']

    user = auth.User(mongo, app)
    user.select_by_email(email)
    check = user.check_password(password)
    if (check):
        login_user(user, remember=True)
        user_id = user.get_id()
        user.set_loggend_in(user_id)
        Auth.set_loggend_in(user_id)
        token = Auth.encode_auth_token(user_id)

        return {"status": 200, "response": {"token": token, "_id": user.get_id(), "role": user.role,}}
    else:
        return {"status": 401, "response": "Login failed",}


@app.route("/logout")
@login_required
def logout():
    Auth.logout_user()
    logout_user()
    return jsonify(**{"status": 200, "response": []})



@app.route('/users/<project_id>')
@login_required
def get_users(project_id):
    query = request.args.get('query')
    return Projects.get_users(project_id, query)


@app.route("/run/<project_id>/<run_id>", methods=["PUT"])
@login_required
@require_role
def edit_run(project_id, run_id):
    data_in = json.loads(request.data.decode("utf-8"))
    return Runs.edit_run(data_in)



@app.route("/run/<project_id>/<run_id>", methods=["DELETE"])
@login_required
@require_role
def delete_run(project_id, run_id):
    return Runs.delete_run(project_id, run_id)



@app.route("/project-members/<project_id>")
@login_required
@require_role
def get_project_members(project_id):
    return Projects.get_project_members(project_id)


@app.route("/project-member/<project_id>", methods=["POST"])
@login_required
@require_role
def add_project_member_role(project_id):
    data_in = request.get_json(force=True)
    return Projects.add_project_member_role(project_id, data_in)


@app.route("/project-member/<project_id>/<user_id>", methods=["PUT"])
@login_required
@require_role
def change_project_member_role(project_id, run_id):
    return Projects.change_project_member_role(project_id, user_id)


@app.route("/project-member/<project_id>/<user_id>", methods=["DELETE"])
@login_required
@require_role
def remove_project_member(project_id, user_id):
    return Projects.remove_project_member(project_id, user_id)




@app.route("/project-charts/<project_id>/<run_id>")
@login_required
@require_role
def get_project_chart(project_id, run_id):
    return Projects.get_project_chart(project_id, run_id)





# @app.route("/project-chart/<project_id>/<user_id>", methods=["PUT"])
# @login_required
# @require_role
# def change_project_member_role(project_id, run_id):
#     return Projects.change_project_member_role(project_id, user_id)


# @app.route("/project-chart/<project_id>/<user_id>", methods=["DELETE"])
# @login_required
# @require_role
# def remove_project_member(project_id, user_id):
#     return Projects.remove_project_member(project_id, user_id)








def setUpDB():
    print("setup db")
    # mongo = get_mongo()
    num_of_docs = mongo.db.Users.find({}).count()
    if num_of_docs == 0:
        print("users table is empty - inserting ")
        mongo.db.users.insert_one(
            {
                "login":"user1",
                "password":"psw1",
                "name":"User1 Name"
            }
        )
    col = mongo.db.users.find({})
    for e in col:
        print(e)
    print("/setup db")
    return


def get_user():
    header = request.headers.get('Authorization')
    if (header):
        token = header.split(" ")[-1]
        user = auth.User(mongo, app)
        return user.get_user_by_token(token)



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', threaded=True)
