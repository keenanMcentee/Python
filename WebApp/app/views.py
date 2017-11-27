from flask import render_template, request, session
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Welcome to Word Game on the Web')
						   
@app.route('/play')
def play():
	return render_template('play.html')
	
@app.route('/processAnswers', methods=['POST'])
def processAnswers():
	words =  request.form['inputWords']
	words = words.split();
	return render_template('processAnswers.html', words = words)