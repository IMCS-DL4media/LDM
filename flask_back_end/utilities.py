import json, math, os

from flask_pymongo import PyMongo

from bson.json_util import dumps
from bson.objectid import ObjectId

import requests
import shutil



def ensure_dir_exists(dir):
   if not os.path.isdir(dir):
        os.mkdir(dir)


def get_app_root_dir():
    return '/app/uploads'


def merge_collection_with_ids(collection_in, ids):
	collection_out = []

	for i, item in enumerate(collection_in):
		item["_id"] = str(ids[i])
		collection_out.append(item)

	return collection_out

def make_header(token):
	return {'Authorization': 'token {}'.format(token)}

