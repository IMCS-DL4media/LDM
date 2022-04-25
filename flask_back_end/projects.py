import os, datetime

from flask import jsonify, request, make_response
from flask_login import current_user
from bson.objectid import ObjectId
from bson.json_util import dumps

from flask_pymongo import DESCENDING

import utilities as u

class Projects():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}
		self.roles =  [{"role_code": 0, "role": "Owner"},
						{"role_code": 1, "role": "Developer"},
						{"role_code": 2, "role": "Reader"},
					]


	def create_new_project(self, data_in, user_id, email):

		project_types_map = {"ImageClassification": {"default": 0,
													 "datasets": [
														{"key": "train", "name": "ImageClassificationTrainingData", "training": "TrainImageClassificationTrainingData", "dataset_root_path":""},
														{"key": "validation", "name": "ImageClassificationValidateData", "training": "TrainImageClassificationValidateData", "dataset_root_path":""},
														{"key": "test", "name": "ImageClassificationTestData", "training": "TrainImageClassificationTestData", "dataset_root_path":""},
													]},

							"ObjectDetection": {"default": 0,
													 "datasets": [
														{"key": "train", "name": "ObjectDetectionTrainingData", "training": "TrainObjectDetectionTrainingData", "dataset_root_path":""},
														{"key": "validation", "name": "ObjectDetectionValidateData", "training": "TrainObjectDetectionValidateData", "dataset_root_path":""},
														{"key": "test", "name": "ObjectDetectionTestData", "training": "TrainObjectDetectionTestData", "dataset_root_path":""},
													]},


							"ImageCaptioning": {"default": 0,
												"datasets": [
													{"key": "train", "name": "ImageCaptioningTrainingData", "training": "TrainImageCaptioningTrainingData", "dataset_root_path":""},
													{"key": "validation", "name": "ImageCaptioningValidateData", "training": "TrainImageCaptioningValidateData", "dataset_root_path":""},
													{"key": "test", "name": "ImageCaptioningTestData", "training": "TrainImageCaptioningTestData", "dataset_root_path":""},
												]},


							"Media2Text": {"default": 0,
												"datasets": [
													{"key": "train", "name": "Media2TextTrainingData", "training": "TrainMedia2TextTrainingData", "dataset_root_path":""},
													{"key": "validation", "name": "Media2TextValidateData", "training": "TrainMedia2TextValidateData", "dataset_root_path":""},
													{"key": "test", "name": "Media2TextTestData", "training": "TrainMedia2TextTestData", "dataset_root_path":""},
												]},



							# "VideoTranscription": {"default": 0,
							# 					"datasets": [
							# 						{"key": "train", "name": "VideoTranscriptionTrainingData", "dataset_root_path":""},
							# 						{"key": "validation", "name": "VideoTranscriptionValidateData", "dataset_root_path":""},
							# 						{"key": "test", "name": "VideoTranscriptionTestData", "dataset_root_path":""},
							# 					]},

							# "AudioTranscription": {"default": 0,
							# 					"datasets": [
							# 						{"key": "train", "name": "AudioTranscriptionTrainingData", "dataset_root_path":""},
							# 						{"key": "validation", "name": "AudioTranscriptionValidateData", "dataset_root_path":""},
							# 						{"key": "test", "name": "AudioTranscriptionTestData", "dataset_root_path":""},
							# 					]},

							}

		project = {'name': data_in["name"], 
		            'created_by': user_id,
		            'settings': project_types_map[data_in["type"]],
		            'type': data_in["type"],
		            'description': data_in["description"],
		            'created_at': datetime.datetime.utcnow(),
		            }

		res = self.mongo.db.projects.insert_one(project)
		proj_id = str(res.inserted_id)

		self.mongo.db.projects_members.insert_one({'project_id': str(proj_id),
													'name': project["name"],
													'type': project["type"],
													'user_id': user_id,
													'email': email, 
													'role': self.roles[0]["role"],
													'role_code': self.roles[0]["role_code"],
													'created_at': datetime.datetime.utcnow(),
													'created_by': user_id,
												})

		res2 = self.mongo.db.users.update_one({"_id": ObjectId(user_id)},
												{"$push": {"projects": {"user_id": user_id, "project_id": proj_id,}}})

		project_out = {'id': proj_id, 
		                'name': project["name"], 
		                'created_by': user_id,
		                'type': project["type"],
		                'description': project["description"],
		                'created_at': project["created_at"],
		                'num_of_runs': 0,
		            }

		self.create_project_dirs(proj_id)

		return make_response(dumps({'msg': 'project created successfully', 'data': project_out}))


	def add_logger_project(self, data_in, user_obj):
		name = data_in["name"]
		user_id = str(user_obj["_id"])
		email = user_obj["email"]

		project = self.mongo.db.projects.find_one({"name": data_in["name"], "created_by": user_id,})
		if (project):
			project_out = {'id': str(project["_id"]), 
							'name': project["name"], 
							'created_by': user_id,
							'type': project["type"],
							'description': project["description"],
						}

			return make_response(dumps({'data': project_out}))
		else:
			return self.create_new_project(data_in, user_id, email)


	def create_project_dirs(self, proj_id):
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects'))    
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id ))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Runs' ))

		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'All'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Train'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Validation'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Test'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Production'))

		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'All'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Train'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Validation'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Test'))


	def get_projects(self):
		user_id = current_user.get_id()

		projects = current_user.get_projects()

		output = []
		for curr_proj in projects:
			output.append({'id': str(curr_proj['project_id']), 
							'name': curr_proj['name'],
							'type': curr_proj['type'],
							'created_at': curr_proj["created_at"],
							'created_by': str(curr_proj['created_by']),
						})

		return make_response(dumps({'projects': output}))


	def get_active_project(self, project_id):
		project = self.mongo.db.projects.find_one({"_id": ObjectId(project_id),})
		return make_response(dumps({'project': project}))


	def delete_project(self, project_id):
		self.mongo.db.projects.delete_one({'_id': ObjectId(project_id)})
		self.mongo.db.projects_members.delete_one({'project_id': project_id})

		self.mongo.db.runs.delete_many({'project_id': project_id})

		self.mongo.db.all_data.delete_many({'project_id': project_id})

		self.mongo.db.training_data.delete_many({'project_id': project_id})
		self.mongo.db.training_labels.delete_many({'project_id': project_id})

		self.mongo.db.validation_data.delete_many({'project_id': project_id})
		self.mongo.db.validation_data.delete_many({'project_id': project_id})

		self.mongo.db.test_data.delete_many({'project_id': project_id})
		self.mongo.db.test_data.delete_many({'project_id': project_id})


		self.mongo.db.silvers.delete_many({'project_id': project_id})	

		# TODO
		print ("remove dirss")

		return make_response(dumps({'result': []}))


	def get_project_members(self, project_id):
		projects_members = self.mongo.db.projects_members.find({'project_id': project_id})
		return make_response(dumps({'members': projects_members, 'roles': self.roles[1:],}))


	def add_project_member_role(self, project_id, data_in):
		member_email = data_in["email"]
		user = self.mongo.db.users.find_one({"email": member_email,})
		if (not user):
			return make_response(dumps({}))

		role_code = data_in["roleCode"]
		role = self.roles[2]["role"]
		for role_in in self.roles:
			if (role_in["role_code"] == int(role_code)):
				role = role_in["role"]
				break

		project = self.mongo.db.projects.find_one({"_id": ObjectId(project_id),})
		if (not project):
			return make_response({})

		item = {'project_id': project_id,
				'name': project["name"],
				'type': project["type"],
				'user_id': str(user["_id"]),
				'email': user["email"],
				'role': role,
				'role_code': role_code,
				'created_at': datetime.datetime.utcnow(),
				'created_by': current_user.get_id(),	
			}

		res = self.mongo.db.projects_members.insert_one(item)
		item["_id"] = str(res.inserted_id)

		return make_response(dumps({'member': item}))


	# def change_project_member_role(self, project_id, user_id):
	# 	print ("in change project members")

	# 	return make_response(dumps({'projects': output}))


	def remove_project_member(self, project_id, member_id):
		self.mongo.db.projects_members.delete_one({"_id": ObjectId(member_id), "role_code": {"$ne": 0},})
		return make_response(dumps({}))


	def get_users(self, project_id, query):
		members = self.mongo.db.projects_members.find({'project_id': project_id})
		users = self.mongo.db.users.find({'email': {'$regex': query, '$options': 'i'}})

		# filtering out members of the project
		users_non_members = [user for user in list(users) if len([m for m in list(members) if m["email"] == user["email"]]) == 0]

		return make_response(dumps({'users': users_non_members,}))


	def get_project_chart(self, project_id, run_id):
		return make_response(dumps({'charts': self.mongo.db.projects_charts.find({'project_id': project_id}),
									'data': self.mongo.db.charts_run_data.find({'project_id': project_id, 'run_id': run_id,}),
									}))


	def add_project_chart(self, project_id, data_in):

		item = {'project_id': project_id,
				'title': data_in["title"],
				'type': data_in["type"],
				'xtitle': data_in["xtitle"],
				'ytitle': data_in["ytitle"],
				'width': data_in["width"],
				'created_at': datetime.datetime.utcnow(),
				'created_by': current_user.get_id(),
				'data': [],
			}

		res = self.mongo.db.projects_charts.insert_one(item)
		item["_id"] = str(res.inserted_id)

		return make_response(dumps({'chart': item}))


	def delete_log_charts(self, chart_id, project_id, run_id):

		self.mongo.db.projects_charts.delete_many({"_id": ObjectId(chart_id), "project_id": project_id,})
		self.mongo.db.charts_run_data.delete_many({"chart_id": chart_id, "project_id": project_id,})

		return make_response(dumps({}))	
