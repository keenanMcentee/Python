import random 
import time
import pickle
from itertools import islice
from collections import Counter
with open('bigWords.txt', errors='ignore') as df:
    rawdataSources = df.read()
source_words_list = rawdataSources.split()

with open('words.txt', errors='ignore') as df:
    rawdataDictionary = df.read()  
allWords = rawdataDictionary.split()

def save_score(score, name):
    leaderboard = pickle.load( open( "leaderboard.p", "rb" ) )
    print(leaderboard)
    leaderboard[score] = name
    print(leaderboard)
    pickle.dump(leaderboard, open( "leaderboard.p", "wb" ) )
    
def load_scores():
    leaderboard = pickle.load( open( "leaderboard.p", "rb" ) )
    sorted_scores = {(k, leaderboard[k]) for k in sorted(leaderboard, key=leaderboard.get, reverse=True)}
    top_ten = list(islice(sorted_scores, 10))
    pos = 1
    print("\n \n \n \nTop 10 scores: ")
    for row in top_ten:
        print("     ", pos, '. ', row[1], row[0])
        pos += 1

    
def check_in_given_word(given_word, to_check):
        '''Subtracts letters from one word to another so we can find if any invalid letters used.'''
        given_word_counter = Counter(given_word)
        word_counter = Counter(to_check)
        given_word_counter.subtract(word_counter)
        return (given_word_counter)

replay = True
while replay == True:
    start = 0.0
    end = 0.0
    time_taken = 0.0
    print("Rules:")
    print('''
    1. Each word must be made up from letters contained within the source word 
    2. The words all have 3 or more letters. 
    3. There are no duplicate words 
    4. None of the 7 submitted words is the source word''')

    inpur_var = 0
    input_var = input("Enter Y to start: ")
    while (input_var[0] != 'y' and input_var[0] != 'Y'):
        input_var = input("Error, please enter Y to start: \n")

    source_word = random.choice(source_words_list)
    print("Please enter 7 words seperated by a space")
    print("  The source word is : " + source_word)
    start = time.time()

    player_input = input("")
    player_words = player_input.split(' ')

    print("\n\n\n\n\n")

    rules_followed = True

    ##Check the amount of Words we have
    if len(player_words) < 7:
        print("Not enough words! Word count: " + str(len(player_words)))
        rules_followed = False
    elif len(player_words) > 7:
        print("Too many words! Word count: "+ str(len(player_words)))
        rules_followed = False
    ##Check that all the words have more than 3 letters.
    for word in player_words:
        if len(word) < 3:
            print("word too small: " + word)
            rules_followed = False
    ##Check that all the letters match the source word without repeating letters.
    for word in player_words:    
        answer = check_in_given_word(source_word , word)
        for letter in word:
            if answer[letter] < 0:
                rules_followed = False
    ##Check for repeats
    if len(player_words) != len(set(player_words)):
        print("Repeated words in answer")
        rules_followed = False
    ##Checks for word in the dictionary   
    for word in player_words:
        if word not in allWords:
            print("Made up word: " + word)
            rules_followed = False
    rules_followed = True
    if rules_followed == True:
        end = time.time()
        time_taken = end - start
        print("Time taken: " + "{0:.2f}".format(time_taken) + "s")
        name = input("Enter name: ")
        save_score(time_taken, name)
        
    load_scores()
    want_replay = input("Would you like to play again?")
    if want_replay[0] != 'y' and want_replay[0] != 'Y':
        replay = False;

