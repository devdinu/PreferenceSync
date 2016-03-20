from bottle import route, run, get, delete, post, request, abort
from pymongo import MongoClient
import json
import pdb

client = MongoClient('localhost', 27017)
preference_collection = client.preference_db.preferences


@post('/users/<user_id>/preferences.json')
def add_preference(user_id):
    pref_body = request.body.read().decode("utf-8")
    print(pref_body)
    user_preference = json.loads(pref_body)
    print("storing information for user_id:" + user_id)
    inserted_record = preference_collection.replace_one(
        {'user_id': user_id}, {'user_id': user_id, 'preference': user_preference}, upsert=True)
    return str(inserted_record.upserted_id)


@delete('/users/<user_id>/preferences/destroy')
def delete_preference(user_id):
    return str(preference_collection.delete_one({'user_id': user_id}).deleted_count)


@get('/users/<user_id>/preferences.json')
def get_preference(user_id):
    user_pref = preference_collection.find_one({'user_id': user_id})
    if user_pref:
        return user_pref['preference']
    else:
        abort(404, "Preference Not Found")

run(host='localhost', port=8888, debug=True, reloader=True)
