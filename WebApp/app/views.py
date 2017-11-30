import random 
import time
import pickle
from itertools import islice
from collections import Counter
from flask import Flask,render_template, request, session
from flask import abort, redirect, url_for
from app import app

with open('./app/static/bigWords.txt', errors='ignore') as df:
    rawdataSources = df.read()
source_words_list = rawdataSources.split()

with open('./app/static/words.txt', errors='ignore') as df:
    rawdataDictionary = df.read()  
allWords = rawdataDictionary.split()

source_word = ""
start = 0.0
end = 0.0
time_taken = 0.0
player_words = ' '
num_of_words = 0
bad_words = []
bad_letters = []
repeats = False

def save_score(score, name):
    leaderboard = pickle.load( open( "./app/static/leaderboard.p", "rb" ) )
    print(leaderboard)
    leaderboard[score] = name
    print(leaderboard)
    pickle.dump(leaderboard, open( "leaderboard.p", "wb" ) )
    
def load_scores():
    leaderboard = pickle.load( open( "./app/static/leaderboard.p", "rb" ) )
    sorted_scores = {(k, leaderboard[k]) for k in sorted(leaderboard, key=leaderboard.get, reverse=True)}
    top_ten = list(islice(sorted_scores, 10))
    return top_ten

		
def check_in_given_word(given_word, to_check):
	'''Subtracts letters from one word to another so we can find if any invalid letters used.'''
	given_word_counter = Counter(given_word)
	word_counter = Counter(to_check)
	given_word_counter.subtract(word_counter)

	return (given_word_counter)
	
def word_count(player_words):
	rules_followed = True
	##Check the amount of Words we have
	num_of_words = len(player_words)
	if num_of_words < 7:
		print("Not enough words! Word count: " + str(len(player_words)))
		rules_followed = False
	elif num_of_words > 7:
		print("Too many words! Word count: "+ str(len(player_words)))
		rules_followed = False
	
	return rules_followed
		
def letter_count(word):
	rules_followed = True
    ##Check that all the words have more than 3 letters.
	for word in player_words:
		if len(word) < 3:
			rules_followed = False
			bad_words.append(word)
			print(bad_words)
	return rules_followed

	

@app.route('/')
@app.route('/index')
def index():
	
	return render_template('index.html', title='Welcome to Word Game on the Web')
						   
@app.route('/play')
def play():
	source_word = random.choice(source_words_list)
	start = time.time()
	return render_template('play.html',word = source_word)
	
@app.route('/processAnswers', methods=['POST'])
def processAnswers():
	player_input =  request.form['inputWords']
	player_words = player_input.split(' ')
	rules_followed = True
	
	##Check right amount of words
	rules_followed = word_count(player_words);

	##Checks the word is the right size
	for word in player_words:
		rules_followed = letter_count(word)

	##Check that all the letters match the source word without repeating letters.
	for word in player_words:    
		answer = check_in_given_word(source_word , word)
		for letter in word:
			if answer[letter] < 0:
				rules_followed = False
				bad_words.append(word)

	##Check for repeats
	if len(player_words) != len(set(player_words)):
		rules_followed = False
		repeats = True

	##Checks for word in the dictionary   
	for word in player_words:
		if word not in allWords:
			print("Made up word: " + word)
			rules_followed = False
			bad_words.append(word)
				
	end = time.time()
	time_taken = start - end
	num_of_words = len(player_words)
	rules_followed = True
	return render_template('processAnswers.html', words = player_words, numWord = num_of_words,badWord = set(bad_words),bad_letters = bad_letters ,rules_followed = rules_followed)

@app.route('/leaderboard', methods=['POST'])
def leaderboard():
	name = request.form['name']
	save_score(time_taken, name)
	top_ten = load_scores()
	list = []
	names = []
	for a in top_ten:
		list.append(a[0])
	list.sort()
	
	print (a)
	return render_template('leaderboard.html',names = names, list = list)