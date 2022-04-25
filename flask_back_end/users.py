import requests, json, math, re, os, time, datetime, random, string
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import jsonify, request, make_response
from flask_login import current_user

import utilities as u

class Users():

	def __init__(self, mongo, app, auth):
		self.mongo = mongo
		# self.fr_service_path = app.config["FR_SERVICE_PATH"]
		# self.file_storage_path = app.config["FILE_STORAGE_PATH"]
		# self.file_storage_global_path = app.config["FILE_STORAGE_GLOBAL_PATH"]
		self.auth = auth

		self.no_access_rights_text = "No access rights"


	def get_current_user(self):

		response = {"id": current_user.get_id(),
					"name": current_user.name,
					"surname": current_user.surname,
				}

		return jsonify(**{"status": 200, "response": response,})


	def get_current_user_profile(self):
		
		response = {"id": current_user.get_id(),
					"name": current_user.name,
					"surname": current_user.surname,
					"email": current_user.email,
					"role": current_user.role,
					"createdAt": current_user.createdAt,
					"profileImage": current_user.profileImage,
					"token": current_user.token,
				}

		return make_response(dumps(response))


	def find_all(self):
		if (current_user and current_user.is_admin()):

			user_email = current_user.get_email() 
			if (user_email == "root"):
				users = json.loads(dumps(self.mongo.db.users.find({}).sort("email", 1)))
				return jsonify(**{"status": 200, "response": users})

			else:
				users = json.loads(dumps(self.mongo.db.users.find({"email": user_email}).sort("email", 1)))
				return jsonify(**{"status": 200, "response": users})

		else:
			return jsonify(**{"status": 500, "response": self.no_access_rights_text,})


	def add_user(self, data, is_system=False):
		user = self.add_user_object(data, is_system)
		if (user):
			return jsonify(**{"status": 200, "response": user})
		else:
			return jsonify(**{"status": 500, "response": self.no_access_rights_text,})	


	def add_user_object(self, data, is_system=False):
		is_login_allowed = True

		# created_by = "system"
		# if (is_system == True):
		# 	is_login_allowed = True
		# else:
		# 	if (current_user and current_user.is_admin()):
		# 		is_login_allowed = True
		# 		created_by = current_user.get_id()

		if (is_login_allowed):
			user = {
					# "name": data["name"],
					# "surname": data["surname"],
					"email": data["email"],
					# "role": data["role"],
					"password": self.auth.hash_password(data["password"]),
					# "createBy": "manual",
					"createdAt": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
					"projects": [],
					"token": self.generate_token(),
					# "profileImage": "",
					# "followingTo": [],
				}

			user_out = self.mongo.db.users.insert_one(user)
			user["_id"] = str(user_out.inserted_id)

			return user
		else:
			return False


	def generate_token(self):
		random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
		return self.auth.hash_password(random_string)


	def edit_user(self, user_id, data):

		if (current_user and current_user.is_admin()):

			update = {"name": data["name"],
						"surname": data["surname"],
						"role": data["role"],
					}

			self.mongo.db.users.update_one({"_id": ObjectId(user_id),}, {"$set": update})
			self.mongo.db.Media.update_many({"uploadedBy": user_id,}, {"$set": {"uploadedByName": data["name"], "uploadedBySurname": data["surname"]}})

			return jsonify(**{"status": 200, "response": []})

		else:
			return jsonify(**{"status": 500, "response": self.no_access_rights_text,})


	def edit_user_profile(self, current_user_in, data):

		if (current_user_in):

			user_id = current_user_in.get_id()

			update = {"name": data["name"],
						"surname": data["surname"],
						# "organization": data["organization"],
					}

			result = self.mongo.db.users.update_one({"_id": ObjectId(user_id),}, {"$set": update})
			self.mongo.db.Media.update_many({"uploadedBy": user_id,}, {"$set": {"uploadedByName": data["name"], "uploadedBySurname": data["surname"]}})

			return jsonify(**{"status": 200, "response": {"updated_count": result.matched_count,}})

		else:
			return jsonify(**{"status": 200, "response": {"updated_count": 0,}})


	def edit_user_password(self, current_user_in, data):
		if (current_user_in.check_password(data["oldPassword"])):
			new_password_hash = self.auth.hash_password(data["newPassword"])
			result = self.mongo.db.users.update_one({"_id": ObjectId(current_user_in.get_id())}, {"$set": {"password": new_password_hash,}})
			return jsonify(**{"status": 200, "response": {"updated_count": result.matched_count,}})

		else:
			return jsonify(**{"status": 200, "response": {"updated_count": 0,}})


	def edit_user_profile_image(self, current_user_in, files, token):
		if (current_user_in and len(files) > 0):
			f = files[0]
			file_to_send = [("files", (f.filename, f.stream, f.mimetype))]
			header = u.make_header(token)
			resp_images = requests.post(self.file_storage_path + "/samples/" + "" + token, files=file_to_send, headers=header)

			content = json.loads(resp_images.content.decode('utf-8'))
			if (content["status"] == 200 and len(content["response"]) > 0):
				image_content = content["response"][0]
				result = self.mongo.db.Users.update_one({"_id": ObjectId(current_user_in.get_id())}, {"$set": {"profileImage": image_content["fileRelativePath"],}})

				return jsonify(**{"status": 200, "response": {"updated_count": result.matched_count, "profileImage": image_content["fileRelativePath"],}})

			else:
				return jsonify(**{"status": 200, "response": {"updated_count": 0,}})

		else:
			return jsonify(**{"status": 200, "response": {"updated_count": 0,}})


	def delete_user(self, user_id):
		if (current_user and current_user.is_admin()):
			self.mongo.db.users.delete_one({"_id": ObjectId(user_id)})
			return jsonify(**{"status": 200, "response": []})

		else:
			return jsonify(**{"status": 500, "response": self.no_access_rights_text,})


	def update_token(self):
		if (current_user):
			new_token = self.generate_token()
			self.mongo.db.users.update_one({"_id": ObjectId(current_user.get_id())},
											{"$set": {"token": new_token}})

			return make_response(dumps({"token": new_token}))

