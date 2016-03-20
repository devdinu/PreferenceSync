from bottle import route, run, get, delete, post, request, abort
from pymongo import MongoClient
import json
import pdb

client = MongoClient('localhost', 27017)
preference_collection = client.preference_db.preferences
DOT_CHAR = "."
DOT_UNICODE = "\\uff0"


@post('/users/<user_id>/preferences.json')
def add_preference(user_id):
    pref_body = request.body.read().decode("utf-8")
    user_preference = json.loads(pref_body)
    print("storing information for user_id:" + user_id)
    data_to_update = {'user_id': user_id,
                      'preference': user_preference}
    upserted_record = preference_collection.update_one(
        {'user_id': user_id}, {"$set": data_to_update}, upsert=True)
    return str(upserted_record.upserted_id)


@post('/users/<user_id>/files/<file_name>/sync.json')
def add_file(user_id, file_name):
    file_content = request.body.read().decode("utf-8")
    file_name = file_name.replace(DOT_CHAR, DOT_UNICODE)
    data_to_store = {'user_id': user_id, 'file_name': file_name, 'content': file_content}
    upserted_file = preference_collection.replace_one(
        {'user_id': user_id, 'file_name': file_name}, data_to_store, upsert=True)
    return str(upserted_file.upserted_id)


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
