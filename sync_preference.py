from bottle import route, run, get, delete, post, request

@post('/users/<user_id:int>/preferences.json')
def add_preference(user_id):
    preferences = request.body.read()
    print(preferences);
    print("adding preferences for user")
    return "success" + str(user_id)

@delete('/users/<user_id:int>/preferences/destroy')
def delete_preference(user_id):
    print("deletes...")

@get('/users/<user_id:int>/preferences.json')
def get_preference(user_id):
    print("It hits...")
    return "Success" + str(user_id)

run(host='localhost', port=8888, debug=True, reloader=True)
