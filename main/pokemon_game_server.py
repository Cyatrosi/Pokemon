from flask import Flask, jsonify #For GET and basics
#from flask import make_response #For error handling
#from flask import request #For POST
#from flask import abort #for 404 error
from pokemon_utils_new import *
import os,random

app = Flask(__name__)
'''
@app.route('/',methods=['GET','POST'])
def index():
	return 'test'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''
@app.route("/")
def hello():
	return "Hello World!"

@app.route('/login',methods = ['GET'])
def login():	
	id = random.randint(1,9);
	return get_random_pokemon(id,35);

@app.route('/list',methods = ['GET'])
def list():	
	return str(['a','b']);

if __name__ == '__main__':
	app.run(debug=True)