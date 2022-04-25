import os, datetime, shutil, zipfile, json

from flask import jsonify, request, make_response, send_from_directory, send_file
from flask_login import current_user
from bson.objectid import ObjectId
from bson.json_util import dumps

from flask_pymongo import DESCENDING

import utilities as u

class Runs():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}


	def get_runs(self, project_id):
		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})

		return make_response(dumps({"runs": runs, "project": project}))


	def get_run(self, project_id, run_id):
		logs = []
		project = []
		run = self.mongo.db.runs.find_one({"_id": ObjectId(run_id), "project_id": project_id})
		if run is not None:
			logs = self.mongo.db.logs.find({"run_id": run_id, "project_id": project_id,})
			project = self.mongo.db.projects.find_one({"_id": ObjectId(project_id)})
		else:
			return 'No run, \'run_id\' ', 400

		return make_response(dumps({'run': run, 'logs': logs, 'project': project}))


	def edit_run(self, data_in):
		updated = self.mongo.db.runs.update_one({'_id': ObjectId(data_in["runId"]), "project_id": data_in["projectId"],},
												{"$set": {"comment": data_in["comment"],}})
		return make_response(dumps({}))

	def delete_run(self, project_id, run_id):
		res = self.mongo.db.runs.delete_one({'_id': ObjectId(run_id), "project_id": project_id})
		return make_response(dumps({}))


	def get_run_files(self, project_id, run_id):
		files = self.mongo.db.source_files.find_one({'run_id': run_id, "project_id": project_id,})
		project = self.mongo.db.projects.find_one({"_id": ObjectId(project_id)})

		return make_response(dumps({'files': files, 'project': project}))

	def start_run(self, project_id, data_in, user):
		run = self.mongo.db.runs.insert_one({'project_id': project_id,
												'comment': data_in["comment"],
												'start_time': datetime.datetime.utcnow(),
												'git_commit_url': data_in["git_commit_url"],
												'user_id': str(user["_id"]),
												'user_email': user["email"],
												# 'remote_address': request.remote_addr
											})

		run_id = run.inserted_id

		path = self.build_run_path(str(project_id), str(run_id))
		u.ensure_dir_exists(path)

		return make_response(dumps({"id": str(run_id),}))


	def finish_run(self, project_id, run_id):
		x = self.mongo.db.runs.update_one({"_id": ObjectId(run_id)},
											{"$set": {"finished": True, "finish_time": datetime.datetime.utcnow()}})

		return make_response(dumps({"status": 200,}))


	def log(self, project_id, run_id, data_in):
		body = data_in["body"]
		run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id), "project_id": project_id,})
		if (run is None):
			return jsonify({'err': 'Run with id \'' + run_id + '\' not found.'}), 404
		
		elif ('finished' in run and run['finished']):
			return jsonify({'err': 'Run with id \'' + run_id + '\' has been finished.'}), 403
		
		else:

			# insert log message in to the given run
			self.mongo.db.logs.insert_one({'run_id': run_id, 
											'project_id': project_id,
											'body': body,
											'logged_on': datetime.datetime.utcnow(),
											'type': "log",
										})

			return make_response(dumps({"status": 200,}))


	def log_charts(self, project_id, run_id, data_in):


		print ("in log charts 2")


		charts = data_in["charts"]

		print ("adsaf ", charts)

		run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id), "project_id": project_id,})

		print ("run" , run)

		if (run is None):
			return jsonify({'err': 'Run with id \'' + run_id + '\' not found.'}), 404
		
		# elif ('finished' in run and run['finished']):
			# return jsonify({'err': 'Run with id \'' + run_id + '\' has been finished.'}), 403
		
		else:

			print ("in else")

			# charts_out = []
			for chart in charts:

				print ("in chart ", chart)

				self.mongo.db.charts_run_data.update({"chart_id": chart["_id"], "project_id": project_id, "run_id": run_id,},
													{"$push": {"data": {"$each": chart["data"],}}}, upsert=True)


			# { $push: { scores: { $each: [ 90, 92, 85 ] } } }


			# # insert log message in to the given run
			# self.mongo.db.log_charts.insert_one({'run_id': run_id, 
			# 									'project_id': project_id,
			# 									'body': body,
			# 									'logged_on': datetime.datetime.utcnow(),
			# 									'type': "log",
			# 								})

			return make_response(dumps({"status": 200,}))




	def upload_file(self, project_id, run_id, data_in, file):
		file_path = self.store_uploaded_file(file, project_id, run_id)

		file_opened = False
		try:
			with open(file_path, 'r') as f:
				file_content = f.read()
			f.close()
			file_opened = True

		except:
			file_opened = False

		body = {'file_name': file.filename, 'file_path': file_path, 'comment': data_in["comment"], 'file_opened': file_opened,}
		self.mongo.db.logs.insert_one({'run_id': run_id,
										'project_id': project_id,
										'body': body,
										'logged_on': datetime.datetime.utcnow(),
										'type': "file",
										}
									)
 
		return make_response(dumps({"status": 200,}))


	def build_run_path(self, project_id, run_id):
		return os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id)


	def store_uploaded_file(self, file, project_id, run_id):
		path = self.get_logged_file_root_path(project_id, run_id)

		u.ensure_dir_exists(path)
		file_path = os.path.join(path, file.filename)
		file.save(file_path)

		return file_path


	def upload_source_files(self, project_id, run_id, file):
		file_path = self.store_source_code(project_id, run_id, file)

		path = os.path.join(self.build_run_path(project_id, run_id), "Source")
		source_tree = self.build_dir_structure_as_json_tree(path)

		self.mongo.db.source_files.insert_one({'run_id': run_id,
												'project_id': project_id,
												'source_tree': json.dumps(source_tree),
												'logged_on': datetime.datetime.utcnow(),
												}
											)
 
		return make_response(dumps({"status": 200,}))


	def store_source_code(self, project_id, run_id, file):
		path = os.path.join(self.build_run_path(project_id, run_id), "Source")

		u.ensure_dir_exists(path)
		zip_file_path = os.path.join(path, file.filename)
		file.save(zip_file_path)

		# unzipping
		with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
			zip_ref.extractall(path)
		zip_ref.close()
		# os.remove(zip_file_path)

		# child_dir_name = os.listdir(path)[0]

		child_dir_names = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
		if (len(child_dir_names) == 0):
			print ("Error in finding child dirs")
			return

		child_dir_name = child_dir_names[0]
		for filename in os.listdir(os.path.join(path, child_dir_name)):
			shutil.move(os.path.join(path, child_dir_name, filename), os.path.join(path, filename))

		os.rmdir(os.path.join(path, child_dir_name))
		

	def build_dir_structure_as_json_tree(self, path):
		d = {'name': os.path.basename(path)}
		if os.path.isdir(path):
			d['type'] = "directory"
			d['children'] = [self.build_dir_structure_as_json_tree(os.path.join(path, x)) for x in os.listdir(path)]
		else:
			d['type'] = "file"
		
		return d


	def get_source_code_files(self, project_id, run_id):
		path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id, "Source")
		return send_from_directory(path, "logger_zip.zip")


	def get_file_body(self, project_id, run_id, path_to_file):
		full_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id, "Source", path_to_file)
		file_content = ""
		try:
			with open(full_path, 'r') as file:
				file_content = file.read()
			file.close()

		except:
			file_content = "Unable to read the file"

		return make_response(dumps({'file_content': file_content,}))


	def get_logged_file_body(self, project_id, run_id, path_to_file):
		full_path = self.get_logged_file_path(project_id, run_id, path_to_file)
		file_content = ""
		try:
			with open(full_path, 'r') as file:
				file_content = file.read()
			file.close()

		except:
			file_content = "Unable to read the file"

		return make_response(dumps({'file_content': file_content,}))


	def get_logged_file_root_path(self, project_id, run_id):
		return os.path.join(self.build_run_path(project_id, run_id), 'LoggedFiles')


	def get_logged_file_path(self, project_id, run_id, path_to_file):
		return os.path.join(self.get_logged_file_root_path(project_id, run_id), path_to_file)


	def download_logged_file(self, project_id, run_id, path_to_file):
		path = self.get_logged_file_path(project_id, run_id, path_to_file)
		return send_file(path, as_attachment=True)



	#TODO: rename to get_gold_labels from test-data
	def get_gold_labels(self, project_id):
	    # get first dir in os.path.join('./uploads', project_id, 'unzipped_data')
	    # from that dir get file labels.txt


	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        return {}

	    first_dir = None
	    for dirn in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        print(dirn)
	        if os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', dirn)):
	            first_dir = dirn
	            break
	    # print(first_dir)

	    file_name2label = {}
	    if first_dir is not None:
	        label_file_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', first_dir, "labels.txt")
	        if os.path.isfile(label_file_path):
	            with open(label_file_path, "r") as f:
	                for line in f:
	                    parts = line.strip().split(',', 2)
	                    if len(parts) == 2:
	                        file_name2label[parts[0]]=parts[1]

	    print(file_name2label)
	    return file_name2label


	def get_silver_labels(self, project_id, run_id):
	    
	    label_file_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id, 'silver_labels.txt' )
	    res = {}
	    if os.path.isfile(label_file_path):
	        with open(label_file_path, "r") as f:
	            for line in f:
	                parts = line.strip().split(',', 2)
	                if len(parts) == 2:
	                    res[parts[0]] = parts[1]
	    return res



	def get_human_readable_file_size(self, file_path):
	    size_in_bytes = 0
	    #check below  is necessary, get size returns size of a dir if file_path points to a dir
	    if os.path.isfile(file_path):        
	        size_in_bytes = os.path.getsize(file_path)
	    
	    if size_in_bytes // (1024*1024*1024) > 0 :
	        return str(size_in_bytes // (1024*1024*1024)) + " Gb"
	    elif size_in_bytes // (1024*1024) > 0:
	        return str(size_in_bytes // (1024*1024)) + " Mb"
	    elif  size_in_bytes // (1024) > 0:
	        return str(size_in_bytes // (1024)) + " Kb"
	    
	    return str(size_in_bytes ) + " bytes"