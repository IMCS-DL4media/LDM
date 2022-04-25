import os, datetime, zipfile, time, json, shutil, uuid

# import argparse, sys, os, json, time, datetime, math, re, uuid, zipfile

from flask import jsonify, request, make_response, send_from_directory, send_file
from flask_login import current_user
from bson.objectid import ObjectId
from bson.json_util import dumps

from werkzeug.utils import secure_filename
from flask_pymongo import DESCENDING

import utilities as u

class Datasets():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}
		self.data_limit = 20

		self.dataset_collections = {"Train": {"dataset_collection": "training_data",
												"labels_collection": "training_labels",
											},
									"Validation": {"dataset_collection": "validation_data",
													"labels_collection": "validation_labels",
												},
									"Test": {"dataset_collection": "test_data",
												"labels_collection": "test_labels",
											},

									"All": {"dataset_collection": "all_data",
												"labels_collection": "all_labels",
											},
									}

		self.silvers_collections = {"Train": "silvers_train",
									"Validation": "silvers_validate",
									"Test": "silvers_test",
								}


		self.predefined_dataset_collections = {"Train": {"dataset_collection": "predefined_training_data",
															"labels_collection": "predefined_dataset_labels",
														},
												"Validation": {"dataset_collection": "predefined_validation_data",
																"labels_collection": "predefined_validation_labels",
															},
												"Test": {"dataset_collection": "predefined_test_data",
															"labels_collection": "predefined_test_labels",
														},

												"All": {"dataset_collection": "predefined_all_data",
															"labels_collection": "predefined_all_labels",
														},

												}

		self.types = {
					"jpeg": "image",
					"jpg": "image",
					"png": "image",
					"tiff": "image",

					"mp3": "video",
					"mp4": "video",
				}


# this is tmp cleaning
		# self.mongo.db.predefined_datasets.delete_many({})
		# self.mongo.db.predefined_training_data.delete_many({})
		# self.mongo.db.predefined_dataset_labels.delete_many({})


		self.init_predefined_datasets()

		self.predefined_datasets = {}
		for dataset in list(self.mongo.db.predefined_datasets.find({})):
			self.predefined_datasets[str(dataset["_id"])] = dataset



	def init_predefined_datasets(self):
		path = os.path.join(u.get_app_root_dir(), "PredefinedDatasets")
		predefined_datasets = [f.path for f in os.scandir(path) if f.is_dir()]

		for dataset_dir in predefined_datasets:
			dataset_name = dataset_dir.split("/")[-1]

			count = self.mongo.db.predefined_datasets.count_documents({"name": dataset_name})
			if (count > 0):
				continue

			dataset_dir = dataset_dir + "/All"

			# print ("dataset_dir ", dataset_dir)
			for file_path in os.scandir(dataset_dir):

				# print ("file_path ", file_path)

				labels_file = None
				file = file_path.path.split("/")[-1]

				if (file == "labels.txt"):
					labels_file = file_path.path
					break

				if (labels_file is None):
					print ("Error, no labels.txt file")
					continue

			# print ("labels_file ", labels_file)
			# labels_file = labels_file + "/All"

			labels_image_map = self.get_labels_image_map(labels_file)
			self.init_predefined_dataset(labels_image_map, dataset_name, "All")


		print ("predefined_datasets ", predefined_datasets)


	def init_predefined_dataset(self, labels_image_map, dataset_name, dataset_type):
		predefined_dataset_inserted = self.mongo.db.predefined_datasets.insert_one({"name": dataset_name, "dataset_type": dataset_type})
		predefined_dataset_id = str(predefined_dataset_inserted.inserted_id)

		predefined_data_collection = self.predefined_dataset_collections[dataset_type]["dataset_collection"]
		predefined_label_collection = self.predefined_dataset_collections[dataset_type]["labels_collection"]


		files_out = []
		labels_dict = {}
		for label, files in labels_image_map.items():
			for fname in files:

				file_out = {"gold": label,
							"src": fname,
							"predefined_dataset_id": predefined_dataset_id,
						}
				files_out.append(file_out)

			if (label not in labels_dict):
				labels_dict[label] = {"category": label,
										"predefined_dataset_id": predefined_dataset_id,
									}

		labels_out = []
		for _, label in labels_dict.items():
			labels_out.append(label)

		self.mongo.db[predefined_data_collection].insert_many(files_out)
		self.mongo.db[predefined_label_collection].insert_many(labels_out)


	def use_predefined_dataset(self, project_id, data_type, predefined_dataset_id):
		data_collection = self.dataset_collections[data_type]["dataset_collection"]
		label_collection = self.dataset_collections[data_type]["labels_collection"]

		predefined_data_collection = self.predefined_dataset_collections[data_type]["dataset_collection"]
		predefined_label_collection = self.predefined_dataset_collections[data_type]["labels_collection"]

		images = self.mongo.db[predefined_data_collection].find({"predefined_dataset_id": predefined_dataset_id})
		images_out = []
		for img in images:
			img_out = {
					"gold": img["gold"],
					"src": predefined_dataset_id + "/" + img["src"],
					"uploaded_file_name": img["src"],
					"project_id": project_id,
				}
			images_out.append(img_out)

		if (len(images_out) > 0):
			self.mongo.db[data_collection].insert_many(images_out)
	
		existing_labels_map = self.get_existing_labels_map(project_id, label_collection)

		labels = self.mongo.db[predefined_label_collection].find({"predefined_dataset_id": predefined_dataset_id})
		categories = []
		for lbl in labels:
			if (lbl["category"] not in existing_labels_map):
				categories.append({"category": lbl["category"],
									"project_id": project_id,
								})

		categories_out = []
		if (len(categories) > 0):
			categories_ids = self.mongo.db[label_collection].insert_many(categories)
			categories_out = u.merge_collection_with_ids(categories, categories_ids.inserted_ids)

		labels_count = self.mongo.db[data_collection].aggregate([{"$match": {"project_id": project_id},},
																	{"$group": {"_id": "$gold", "count": {"$sum": 1}}}])

		return images_out, categories_out, labels_count


	def upload_all_data(self, project_id):
		return self.upload_dataset(project_id, "All")


	def upload_training_data(self, project_id):
		return self.upload_dataset(project_id, "Train")


	def upload_testing_data(self, project_id):
		return self.upload_dataset(project_id, "Test")


	def upload_validation_data(self, project_id):
		return self.upload_dataset(project_id, "Validation")	


	def upload_data(self, project_id):
		# print ("upload data", project_id)

		# if 'dataset_spec_kind' in request.form:
		# 	dataset_spec_kind = request.form['dataset_spec_kind']
		# 	if dataset_spec_kind == 'PredefinedDataSet':
		# 		predefined_dataset_id = request.form['predefined_dataset_id']
		# 		images_out, categories_out, labels_count = self.use_predefined_dataset(project_id, data_type, predefined_dataset_id)
				
		# 		return make_response(dumps({"media": images_out[:self.data_limit],
		# 									"labels": categories_out,
		# 									"labelsCount": labels_count,
		# 									"totalImages": len(images_out),
		# 									"step": self.data_limit,
		# 								}))

		data_type = "All"

		if 'zip_file' in request.files:
			self.unzip_uploaded_dataset(project_id, data_type)

			data_collection = self.dataset_collections[data_type]["dataset_collection"]
			label_collection = self.dataset_collections[data_type]["labels_collection"]

			images_out = []
			categories = []

			labels = self.get_gold_label_map(project_id, data_type)
			existing_labels_map = self.get_existing_labels_map(project_id, label_collection)

			for category, values in labels.items():
				images = []
				for value in values:

					file_extension = value.split(".")[-1]

					img = {"gold": category,
							"type": self.types[file_extension],
							"uploaded_file_name": value,
							"src": project_id + "/" + value,
							"project_id": project_id,
							"_id": ObjectId(),
						}
					images.append(img)


				# data_collection = self.dataset_collections[data_type]["dataset_collection"]
				# all_data_collection = self.dataset_collections["All"]["dataset_collection"]

				# if (data_collection != all_data_collection):
				# 	self.mongo.db[all_data_collection].insert_many(files)


				images_ids = self.mongo.db[data_collection].insert_many(images)

				if (category not in existing_labels_map):
					categories.append({"category": category, "project_id": project_id})

				images_out = images_out + u.merge_collection_with_ids(images, images_ids.inserted_ids)


				print ("images_out ", images_out)


			categories_out = []
			if (len(categories) > 0):
				categories_ids = self.mongo.db[label_collection].insert_many(categories)
				categories_out = u.merge_collection_with_ids(categories, categories_ids.inserted_ids)

			labels_count = self.mongo.db[data_collection].aggregate([{"$match": {"project_id": project_id},},
																	{"$group": {"_id": "$gold", "count": {"$sum": 1}}}])


			return make_response(dumps({"media": images_out[:self.data_limit],
										"labels": categories_out,
										"labelsCount": labels_count,
										"total": len(images_out),
										"step": self.data_limit,
									}))

		return 'Malformed request. Params \'zip_file\' and \'project_id\' must be present. ', 400


	def upload_object_detection_dataset(self, project_id, data_type):

		if ('zip_file' in request.files):
			self.unzip_uploaded_dataset(project_id, data_type)

			if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', "All")):
				return {}

			labels_file_path = ""
			for r, d, f in os.walk(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', "All")):
				for file in f:
					if os.path.isfile(os.path.join(r, file)) and file == "data.json":
						labels_file_path = os.path.join(r, file)

			if labels_file_path == "":
				return {}

			with open(labels_file_path) as json_file:
				data = json.load(json_file)


			images = []
			labels = []
			for item in data["images"]:
				value = item["file_name"]
				img = {"gold": item["gold"],
						"type": self.types["jpg"],
						"uploaded_file_name": value,
						"src": project_id + "/" + value,
						"project_id": project_id,
						"_id": ObjectId(),
						"width": item["width"],
						"height": item["height"],
					}

				images.append(img)

			images_out = []
			categories_out = []
			labels_count = 0

			if (len(images) > 0):
				all_data_type = "All"
				all_data_collection = self.dataset_collections[all_data_type]["dataset_collection"]

				images_ids = self.mongo.db[all_data_collection].insert_many(images)
				images_out = images_out + u.merge_collection_with_ids(images, images_ids.inserted_ids)

				label_collection = self.dataset_collections[data_type]["labels_collection"]
				all_label_collection = self.dataset_collections[all_data_type]["labels_collection"]


				# existing_labels_map = self.get_existing_labels_map(project_id, label_collection)
				# print ("existing_labels_map ", existing_labels_map)

				# if (category not in existing_labels_map):
				# 	label_id = ObjectId()
				# 	categories.append({"category": category,
				# 						"project_id": project_id,
				# 						"_id": label_id,
				# 					})

				# print ("categories ", categories)

				# if (len(categories) > 0):

				# 	categories_ids = self.mongo.db[all_label_collection].insert_many(categories)
				# 	# if (label_collection != all_label_collection):
				# 		# self.mongo.db[label_collection].insert_many(categories)

				# 	categories_out = u.merge_collection_with_ids(categories, categories_ids.inserted_ids)



			return make_response(dumps({"media": images_out[:self.data_limit],
										"labels": categories_out,
										"labelsCount": labels_count,
										"total": len(images_out),
										"step": self.data_limit,
									}))


	def upload_dataset(self, project_id, data_type):

		if 'dataset_spec_kind' in request.form:
			dataset_spec_kind = request.form['dataset_spec_kind']
			if dataset_spec_kind == 'PredefinedDataSet':
				predefined_dataset_id = request.form['predefined_dataset_id']
				images_out, categories_out, labels_count = self.use_predefined_dataset(project_id, data_type, predefined_dataset_id)
				
				return make_response(dumps({"media": images_out[:self.data_limit],
											"labels": categories_out,
											"labelsCount": labels_count,
											"total": len(images_out),
											"step": self.data_limit,
										}))

		if 'zip_file' in request.files:

			# data_type = "All"

			self.unzip_uploaded_dataset(project_id, data_type)

			all_data_type = "All"
			data_collection = self.dataset_collections[data_type]["dataset_collection"]
			all_data_collection = self.dataset_collections[all_data_type]["dataset_collection"]

			label_collection = self.dataset_collections[data_type]["labels_collection"]
			all_label_collection = self.dataset_collections[all_data_type]["labels_collection"]

			images_out = []
			categories = []

			labels = self.get_gold_label_map(project_id, data_type)
			existing_labels_map = self.get_existing_labels_map(project_id, label_collection)

			for category, values in labels.items():
				images = []
				for value in values:
					file_extension = value.split(".")[-1]
					img = {"gold": category,
							"type": self.types[file_extension],
							"uploaded_file_name": value,
							"src": project_id + "/" + value,
							"project_id": project_id,
							"_id": ObjectId(),							
						}
					images.append(img)

				images_ids = self.mongo.db[all_data_collection].insert_many(images)
				if (data_collection != all_data_collection):
					self.mongo.db[data_collection].insert_many(images)

				if (category not in existing_labels_map):
					label_id = ObjectId()
					categories.append({"category": category,
										"project_id": project_id,
										"_id": label_id,
									})

				images_out = images_out + u.merge_collection_with_ids(images, images_ids.inserted_ids)

			categories_out = []
			if (len(categories) > 0):

				categories_ids = self.mongo.db[all_label_collection].insert_many(categories)
				if (label_collection != all_label_collection):
					self.mongo.db[label_collection].insert_many(categories)

				categories_out = u.merge_collection_with_ids(categories, categories_ids.inserted_ids)

			labels_count = self.mongo.db[data_collection].aggregate([{"$match": {"project_id": project_id},},
																	{"$group": {"_id": "$gold", "count": {"$sum": 1}}}])


			print ("images_out ", images_out)

			return make_response(dumps({"media": images_out[:self.data_limit],
										"labels": categories_out,
										"labelsCount": labels_count,
										"total": len(images_out),
										"step": self.data_limit,
									}))

		return 'Malformed request. Params \'zip_file\' and \'project_id\' must be present. ', 400


	def unzip_uploaded_dataset(self, project_id, data_type):
		data_type = "All"

		f = request.files['zip_file']
		zip_file_path = os.path.join(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Data', data_type, f.filename))
		if (os.path.isfile(zip_file_path)):
			print ("File already exits", zip_file_path)
			return

		extract_dir = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', data_type)

		f.save(zip_file_path)

		with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
			for name in zip_ref.namelist():
				member = zip_ref.open(name)
				file_name = name.split("/")[-1]
				if (file_name == ""):
					continue

				with open(os.path.join(extract_dir, file_name), 'wb') as outfile:
					shutil.copyfileobj(member, outfile)


	def upload_file(self, project_id, data_type):
		files = []
		for f in request.files.getlist("files[]"):
			file_extension = f.filename.split(".")[-1]
			file_name = str(uuid.uuid1()) + "." + file_extension

			file_path = os.path.join(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'All', file_name))
			# file_path = os.path.join(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', data_type, file_name))
			f.save(file_path)

			file = {"project_id": project_id,
					"src": project_id + "/" + file_name,
					"file_name": file_name,
					"uploaded_file_name": f.filename,
					"file_path": file_path,
					"created_at": datetime.datetime.utcnow(),
					"type": self.types[file_extension] or "unknown",
					"gold": "",
					"_id": ObjectId(),
				}
			files.append(file)

		files_ids = []
		if (len(files) > 0):
			data_collection = self.dataset_collections[data_type]["dataset_collection"]
			all_data_collection = self.dataset_collections["All"]["dataset_collection"]

			if (data_collection != all_data_collection):
				self.mongo.db[all_data_collection].insert_many(files)

			files_ids = self.mongo.db[data_collection].insert_many(files)

		files_out = u.merge_collection_with_ids(files, files_ids.inserted_ids)

		return make_response(dumps({"media": files_out,}))


	def get_existing_labels_map(self, project_id, label_collection):
		existing_labels_map = {}
		existing_labels = list(self.mongo.db[label_collection].find({"project_id": project_id}))
		for existing_label in existing_labels:
			existing_labels_map[existing_label["category"]] = True

		return existing_labels_map


	def get_training_set(self, project_id):
		return self.get_dataset(project_id, "Train")


	def get_testing_set(self, project_id):
		return self.get_dataset(project_id, "Test")


	def get_validation_set(self, project_id):
		return self.get_dataset(project_id, "Validation")


	def get_dataset(self, project_id, dataset_type):
		dataset_type = "All"
		dir_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', dataset_type)
		filePaths = self.retrieve_file_paths(dir_path)

		zip_name = project_id + ".zip"

		zip_file = zipfile.ZipFile(zip_name, 'w')
		with zip_file:
			for file in filePaths:
				zip_file.write(file)
		zip_file.close()

		return send_file(zip_name, attachment_filename = zip_name, as_attachment = True)


	def get_gold_all_data(self, project_id, page_in, exclude, match):
		return self.get_gold_dataset_data(project_id, page_in, exclude, match, "all_data", "all_labels")

	def get_gold_training_data(self, project_id, page_in, exclude, match):
		return self.get_gold_dataset_data(project_id, page_in, exclude, match, "training_data", "training_labels")


	def get_gold_testing_data(self, project_id, page_in, exclude, match):
		return self.get_gold_dataset_data(project_id, page_in, exclude, match, "test_data", "test_labels")


	def get_gold_validation_data(self, project_id, page_in, exclude, match):
		return self.get_gold_dataset_data(project_id, page_in, exclude, match, "validation_data", "validation_labels")


	def get_gold_dataset_data(self, project_id, page_in, exclude, match, data_collection, label_collection):
		limit = self.data_limit
		page = int(page_in)
	
		data_collection_query = {"project_id": project_id,}
		if (exclude is not None):
			exclude_ids = exclude.split(",")
			data_collection_query["gold"] = {"$nin": exclude_ids}

		if (match == "match"):
			data_collection_query["result"] = 1
		elif (match == "mismatch"):
			data_collection_query["result"] = 0


		print ("in get dataset data")

		images_collection = self.mongo.db[data_collection].find(data_collection_query)
		images = list(images_collection.skip(limit * page).limit(limit))

		labels = self.mongo.db[label_collection].find({"project_id": project_id})
		labels_count = self.mongo.db[data_collection].aggregate([{"$match": {"project_id": project_id},},
																{"$group" : {"_id": "$gold", "count": {"$sum": 1}}}])


		# runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		# project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})

		total = self.mongo.db[data_collection].count_documents(data_collection_query)


		return make_response(dumps({"media": images,
									"labels": labels,
									"total": total,
									"step": limit,
									# "runs": runs,
									"labelsCount": labels_count,
									# "silversCount": [],
									"predefined_datasets": self.predefined_datasets,
									# "project": project,
								}))



	def get_silver_training_data(self, project_id, run_id, page_in, exclude, match):
		return self.get_silver_dataset_data(project_id, run_id, page_in, exclude, match, "Train")


	def get_silver_testing_data(self, project_id, run_id, page_in, exclude, match):
		return self.get_silver_dataset_data(project_id, run_id, page_in, exclude, match, "Test")


	def get_silver_validation_data(self, project_id, run_id, page_in, exclude, match):
		return self.get_silver_dataset_data(project_id, run_id, page_in, exclude, match, "Validation")


	def get_silver_dataset_data(self, project_id, run_id, page_in, exclude, match, data_type):
		limit = self.data_limit
		page = int(page_in)
	
		silvers_collection = self.silvers_collections[data_type]

		data_collection_query = {"project_id": project_id, "run_id": run_id,}
		if (exclude is not None):
			exclude_ids = exclude.split(",")
			data_collection_query["gold"] = {"$nin": exclude_ids}

		if (match == "match"):
			data_collection_query["result"] = 1
		elif (match == "mismatch"):
			data_collection_query["result"] = 0


		print ("in get dataset data")

		silvers_count = []

		images_collection = self.mongo.db[silvers_collection].find(data_collection_query)
		images = list(images_collection.skip(limit * page).limit(limit))

		# labels = self.mongo.db[label_collection].find({"project_id": project_id})
		labels = []

		labels_count = self.mongo.db[silvers_collection].aggregate([{"$match": {"project_id": project_id, "run_id": run_id,},},
																	{"$group": {"_id": "$gold", "count": {"$sum": 1}}},
																	])

		silvers_count = self.mongo.db[silvers_collection].aggregate([{"$match": {"project_id": project_id, "run_id": run_id,},},
																	{"$group": {"_id": "$silver", "count": {"$sum": 1}}},
																	])


		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})

		total = self.mongo.db[silvers_collection].count_documents(data_collection_query)

		return make_response(dumps({"media": images,
									"labels": labels,
									"total": total,
									"step": limit,
									"runs": runs,
									"labelsCount": labels_count,
									"silversCount": silvers_count,
									"predefined_datasets": self.predefined_datasets,
									"project": project,
								}))


	def get_production_data(self, project_id, model_id, page_in, exclude, match):
		limit = self.data_limit
		page = int(page_in)

		data_collection_query = {"project_id": project_id,}
		if (exclude is not None):
			exclude_ids = exclude.split(",")
			data_collection_query["silver"] = {"$nin": exclude_ids}

		images_collection = self.mongo.db.production_data.find(data_collection_query)
		images = list(images_collection.skip(limit * page).limit(limit))

		labels = self.mongo.db.production_labels.find({"project_id": project_id})
		labels_count = self.mongo.db.production_data.aggregate([{"$match": {"project_id": project_id},},
																{"$group" : {"_id": "$silver", "count": {"$sum": 1}}}])

		project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})
		total = self.mongo.db.production_data.count_documents(data_collection_query)

		return make_response(dumps({"media": images,
									"labels": labels,
									"total": total,
									"step": limit,
									"labelsCount": labels_count,
									"project": project,
								}))


	def store_production_result(self, project_id, model_id, data_in, file):
		file_extension = file.filename.split(".")[-1]
		file_name = str(uuid.uuid1()) + "." + file_extension
		path = os.path.join(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Data', "Production", file_name))
		file.save(path)

		silver = data_in["silver"]

		item = {"project_id": project_id,
				"model_id": model_id,
				"silver": silver,
				"created_at": datetime.datetime.utcnow(),
				"path": path,
				"file_name": file_name,
			}

		result = self.mongo.db.production_data.insert_one(item)

		labels_map = {}
		labels = list(self.mongo.db.production_labels.find({"project_id": project_id}))
		for label in labels:
			labels_map[label["category"]] = True

		if (type(silver) == "str" and silver not in labels_map):
			self.mongo.db.production_labels.insert_one({"project_id": project_id,
														"category": silver,
														"created_at": datetime.datetime.utcnow(),
													})

		return make_response(dumps({"status": 200}))


	def get_all_file(self, project_id, name):
		return self.get_dataset_file(project_id, name, "All")

	def get_training_file(self, project_id, name):
		return self.get_dataset_file(project_id, name, "Train")

	def get_testing_file(self, project_id, name):
		return self.get_dataset_file(project_id, name, "Test")

	def get_validation_file(self, project_id, name):
		return self.get_dataset_file(project_id, name, "Validation")


	def get_production_file(self, project_id, name):
		return send_from_directory(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Data', 'Production'), name)


	def get_dataset_file(self, prefix_id, name, dataset_type):
		if (prefix_id in self.predefined_datasets):
			# aa = os.path.join(u.get_app_root_dir(), 'PredefinedDatasets', self.predefined_datasets[prefix_id]["name"], "All")
			# print ("in predefined_datasets ", aa)
			# print ("name ", name)
			# print ("")

			# aa = "/app/uploads/PredefinedDatasets/OxfordFlowers22/All"


			# # return send_from_directory(aa, name)

			return send_from_directory(os.path.join(u.get_app_root_dir(), 'PredefinedDatasets', self.predefined_datasets[prefix_id]["name"], "All"), name)
		else:
			return send_from_directory(os.path.join(u.get_app_root_dir(), 'Projects', prefix_id, 'Unzipped_data', "All"), name)


	def get_media_gold_data(self, project_id, page_in, data_type):
		limit = self.data_limit
		page = int(page_in)
		
		data_collection = self.dataset_collections[data_type]["dataset_collection"]

		media_collection = self.mongo.db[data_collection].find({"project_id": project_id})
		media = list(media_collection.skip(limit * page).limit(limit))

		# runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})

		total = self.mongo.db[data_collection].count_documents({"project_id": project_id})

		return make_response(dumps({"media": media,
									"total": total,
									"step": limit,
									"project": project,
								}))


	def get_media_silver_data(self, project_id, run_id, page_in, data_type):
		limit = self.data_limit
		page = int(page_in)
		
		data_collection = self.silvers_collections[data_type]

		media_collection = self.mongo.db[data_collection].find({"project_id": project_id, "run_id": run_id,})
		media = list(media_collection.skip(limit * page).limit(limit))

		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		project = self.mongo.db.projects.find_one({'_id': ObjectId(project_id)})

		total = self.mongo.db[data_collection].count_documents({"project_id": project_id, "run_id": run_id,})

		return make_response(dumps({"media": media,
									"total": total,
									"step": limit,
									"runs": runs,
									"project": project,
								}))


	def get_gold_media_transcription(self, project_id, media_id, data_type):
		data_collection = self.dataset_collections[data_type]["dataset_collection"]
		media = self.mongo.db[data_collection].find_one({"_id": ObjectId(media_id), "project_id": project_id,})
		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)

		return make_response(dumps({"media": media, "runs": runs}))


	def get_silver_media_transcription(self, project_id, media_id, run_id, data_type):
		silvers_collection = self.silvers_collections[data_type]

		media = self.mongo.db[silvers_collection].find_one({"_id": ObjectId(media_id),
															"run_id": run_id,
															"project_id": project_id,
														})

		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)

		return make_response(dumps({"media": media, "runs": runs}))


	def update_item(self, project_id, id, data_in, data_type):
		all_data_collection = self.dataset_collections["All"]["dataset_collection"]
		train_data_collection = self.dataset_collections["Train"]["dataset_collection"]
		validation_data_collection = self.dataset_collections["Validation"]["dataset_collection"]
		test_data_collection = self.dataset_collections["Test"]["dataset_collection"]

		self.mongo.db[all_data_collection].update_one({"_id": ObjectId(id), "project_id": project_id,},
																	{"$set": {"gold": data_in["gold"]}})

		self.mongo.db[train_data_collection].update_many({"_id": ObjectId(id), "project_id": project_id,},
																{"$set": {"gold": data_in["gold"]}})

		self.mongo.db[validation_data_collection].update_many({"_id": ObjectId(id), "project_id": project_id,},
																{"$set": {"gold": data_in["gold"]}})

		self.mongo.db[test_data_collection].update_many({"_id": ObjectId(id), "project_id": project_id,},
																{"$set": {"gold": data_in["gold"]}})

		return make_response(dumps({"status": 200}))


	def delete_item(self, project_id, id, data_collection):		
		all_data_collection = self.dataset_collections["All"]["dataset_collection"]
		train_data_collection = self.dataset_collections["Train"]["dataset_collection"]
		validate_data_collection = self.dataset_collections["Validation"]["dataset_collection"]
		test_data_collection = self.dataset_collections["Test"]["dataset_collection"]

		self.mongo.db[all_data_collection].delete_one({"_id": ObjectId(id), "project_id": project_id,})
		self.mongo.db[train_data_collection].delete_one({"_id": ObjectId(id), "project_id": project_id,})
		self.mongo.db[validate_data_collection].delete_one({"_id": ObjectId(id), "project_id": project_id,})
		self.mongo.db[test_data_collection].delete_one({"_id": ObjectId(id), "project_id": project_id,})

		return make_response(dumps({"status": 200}))


	def get_public_datasets(self):
		return make_response(dumps({"predefined_datasets": self.predefined_datasets,}))


	def get_public_dataset(self, dataset, dataset_type, page):
		predefined_dataset = self.mongo.db.predefined_datasets.find_one({"name": dataset})

		predefined_data_collection = self.predefined_dataset_collections[dataset_type]["dataset_collection"]
		predefined_label_collection = self.predefined_dataset_collections[dataset_type]["labels_collection"]

		limit = self.data_limit
		page = int(page)

		predefined_dataset_id = str(predefined_dataset["_id"])
		images = self.mongo.db[predefined_data_collection].find({"predefined_dataset_id": predefined_dataset_id}).skip(limit * page).limit(limit)
		labels = self.mongo.db[predefined_label_collection].find({"predefined_dataset_id": predefined_dataset_id})

		total_images = self.mongo.db[predefined_data_collection].count_documents({"predefined_dataset_id": predefined_dataset_id})
		# labels_count = self.mongo.db[predefined_label_collection].count_documents({"predefined_dataset_id": predefined_dataset_id})

		labels_count = self.mongo.db[predefined_label_collection].aggregate([{"$match": {"predefined_dataset_id": predefined_dataset_id},},
																			{"$group": {"_id": "$category", "count": {"$sum": 1}}}])


		return make_response(dumps({
									"media": images,
									"labels": labels,

									"total": total_images,
									"step": limit,
									# "silvers": silvers,
									# "runs": runs,
									"labelsCount": labels_count,
									# "silversCount": silvers_count,
									# "predefined_datasets": self.predefined_datasets,
								}))



	def get_public_dataset_image(self, dataset, dataset_type, name):
		return send_from_directory(os.path.join(u.get_app_root_dir(), 'PredefinedDatasets', dataset, 'Unzipped_data', dataset_type), name)


	# stores file in a folder corresponding to given run_id
	def store_file(self, file, run_id):
	    #find project for this run
	    run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id)})
	    if run is not None:
	        project_id = str(run['project_id'])
	    
	        # if dir for this run does not exist - create dir;
	        # after that store file in a dir corresponding to this run

	        run_dir_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id)
	        #TODO: vai seit ir jabut ensure dir exists izsaukumam ?
	        u.ensure_dir_exists( run_dir_path )
	        # file.save(os.path.join( run_dir_path, secure_filename(file.filename)))
	        file.save(os.path.join(run_dir_path, file.filename))


	def get_gold_label_map(self, project_id, data_type):
	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', "All")):
	        return {}

	    labels_file_path = ""
	    for r, d, f in os.walk(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', "All")):
	        for file in f:
	            if os.path.isfile(os.path.join(r, file)) and file == "labels.txt":
	                labels_file_path = os.path.join(r, file)

	    if labels_file_path == "":
	        return {}

	    return self.get_labels_image_map(labels_file_path)


	def get_labels_image_map(self, labels_file_path):
		labels_2_list_of_files = {}

		with open(labels_file_path, "r") as f:
			for line in f:
				parts = line.strip().split(',', 2)
				if len(parts) == 2:
					fname = parts[0].strip()
					label = parts[1].strip()
					if not label in labels_2_list_of_files:
						labels_2_list_of_files[label] = []

					labels_2_list_of_files[label].append(fname)

		return labels_2_list_of_files


	def retrieve_file_paths(self, dirName):
		filePaths = []

		# Read all directory, subdirectories and file lists
		for root, directories, files in os.walk(dirName):
			for filename in files:
			    filePath = os.path.join(root, filename)
			    filePaths.append(filePath)
		     
		return filePaths