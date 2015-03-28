from app import app
from flask import Flask, jsonify, request

from utilities import InvalidId

tasks = [

    {
        'id':1,
        'title': u'Task 1',
        'description': u'This is task 1',
	'done': False
    },
    {
        'id':2,
        'title': u'Task 2',
        'description': u'This is task 2',
	'done': False
     },
    {
        'id':3,
        'title': u'Task 3',
        'description': u'This is task 3',
	'done': False
     },
	{
		'id':4,
		'title': u'task 4',
		'description': u'This is task 4',
		'done': False
	}
]

@app.errorhandler(InvalidId)
def handle_invalid_id(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/api/v1.0/task/all', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise InvalidId('Task not found', status_code=404)
    return jsonify({'task': task[0]})

@app.route('/api/v1.0/task', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	return jsonify({'task': task}), 201

@app.route('/api/v1.0/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/api/v1.0/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
 