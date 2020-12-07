from bson import ObjectId
from pymongo.collection import Collection

from backend.main import db

this_db: Collection = db.groups


class Groups:
	@staticmethod
	def insert(grpname):
		this_db.insert_one({'name': grpname,
		                    'channels': []})
	
	@staticmethod
	def remove(grpname):
		this_db.delete_one({'name': grpname})
		
	@staticmethod
	def add_channel(channelid, grpid: str):
		this_db.update_one({'_id': ObjectId(grpid)},
		                   {'$push': {'channels': channelid}})
	
	@staticmethod
	def remove_channel(channelid, grpid: str):
		this_db.update_one({'_id': ObjectId(grpid)},
		                   {'$pull': {'channels': channelid}})
	
	@staticmethod
	def list():
		return this_db.find()
	
	@staticmethod
	def get(grpid: str):
		return this_db.find_one({'_id': ObjectId(grpid)})
