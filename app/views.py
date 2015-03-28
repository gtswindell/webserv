from flask import render_template
from app import app

## @app.route('/')
@app.route('/showme')
def index():
    user = {'nickname': 'Glen'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

