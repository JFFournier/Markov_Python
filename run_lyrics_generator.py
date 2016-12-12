""" This is the main module for markov chain Forgotten Morissey Song. It will:
	- Get artist/web
	- Check if file input for probalistics exists.
		- If not, run fetch_data
		- If yes, continue to next
	- Setup Markov probalistics
		- get complete list of words (unique)
		- for each word, get the following words.
		- from that, get probability of next word
	- write lyric
		- import random.
		- generate song length from average song length + or - random(0,stddev)
		- random first word (always cap first letter and first letter of first word after '.')
		- In a while statement number of words < song_length
			- from probalistics, get following word.	
	- save it 
	- display it."""

import fetch_data
from markov import MarkovChain
import random
import default_lists
import os

def get_url_list():
	invalid_answer = True
	while invalid_answer:
		ans_data_source = raw_input("Which dataset do you want to use? \na) Current database (whatever it is).\nb) Morrissey\nc) Suede\nd) Someone new (use http://www.azlyrics.com/)\n")
		if ans_data_source.lower() == "a":
			if os.path.isfile('title_from_url.txt') and os.path.isfile('text_from_url.txt'):
				invalid_answer = False
				url_list = []
				with open("title_from_url.txt", 'r') as f:
					for i, line in enumerate(f):
						url_list.append(line) 
			else:
				invalid_answer = True
				print ("Program needs to first generate a local database before using it... You should run b, c, or d.")			
		elif ans_data_source.lower() == "b":
			invalid_answer = False
			url_list = default_lists.morrissey_url_list()
			("Using default Morrissey data.")
		elif ans_data_source.lower() == "c":
			invalid_answer = False
			url_list = default_lists.suede_url_list()
			print ("Using default Suede data.")
		elif ans_data_source.lower() == "d":
			invalid_answer = False
			url_list = []
			while True:
				try:
					nb_sources = int(raw_input("How many sources are you going to use? "))
					for i in range(0,nb_sources):
						url_i = raw_input("Please provide a URL: ")
						url_list.append(url_i)						
				except ValueError:
					print("Try again... like a number please.")
				else:
					break
		else:
			invalid_answer = True
			print ("Try answering the question with 'a', 'b', 'c' or 'd'. I suggest 'b'. ")
	return ans_data_source.lower(), url_list

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
	
def list_to_str(text_as_list, length_ave, length_stddev):						#Converts a list of string into a single string, but with each line of different length around an average and stddev
	word_cursor = 0
	text_len = len(text_as_list)
	text_as_str =  ""
	while word_cursor + length_ave <= text_len:
		line_length = length_ave + random.randint(-length_stddev,length_stddev)
		stupid_end = ['the', 'a', 'we', 'and', 'to', 'you', 'he', 'she', 'I', "I'm", "I've","he'll", 'as']
		try:
			while text_as_list[word_cursor+line_length-1] in stupid_end:		#makes sure the line does not end stupidly
				line_length += 1
		except IndexError:														#If cursor is beyond list index, then sets at last acceptable word in list
			i=0
			while text_as_list[text_len-1-i] in stupid_end:
				line_length -= 1
				i += 1
			line_length = text_len - word_cursor - i							#sets position for last acceptable (i) word
		line = " ".join(text_as_list[word_cursor:word_cursor+line_length])
		text_as_str += first_cap(line) + "\n"
		word_cursor += line_length
	return text_as_str

def first_cap(string):
	line_cap = string[0].upper()												#Capitalizes first letter of line using slicing and upper().
	line_cap += string[1:len(string)+1]
	return line_cap
	
def get_markov_text(text_as_list, length_ave, length_stddev):					#Generates Markov text using MarkovChain objects and average length. Returns a list.
	markov_text = MarkovChain(text_as_list, 3)												
	markov_length = length_ave + random.randint(-length_stddev,length_stddev)
	return markov_text.generate_markov_chain(markov_length)	
		
def save_song(title, song):														#Asks user if he wants to save the song and does it if asked to.
	while True:
		save_song_answer = raw_input("Do you want to save this pretty song to a file (y/n)? ")
		if save_song_answer.lower() == 'y':
			file = raw_input("Great, glad you like it.\nGive me a filename please. ")
			mode = ""
			while mode.lower() not in ['w', 'a']:
				mode = raw_input("One more thing. Should I overwrite (w) or add (a) to this file? ")
			with open(file, mode) as f:
				f.write(title + "\n\n\n")
				f.write(song + "\n\n#################\n\n")
			break
		elif save_song_answer.lower() == 'n':
			print ("Fine! Have it your way.")
			break
		else:
			print ("Just say 'y' or 'n' please. Geez... ")

def cap_word(list,match_list):													#capitalize a word in a list if found in list of word; returns new list
	for i in range(len(list)):
		for word in match_list:
			if list[i] == word:
				list[i] = first_cap(word)
	return list
		
			
print ("This program recreates the brain patterns of authors to create more of their texts. ")

ans_data_source, url_list = get_url_list()
texts_dico = fetch_data.__main__(ans_data_source, url_list)

#this block merges all titles/text as single lists to send to Markov module.
texts_dico['all_texts'] = []
texts_dico['all_titles'] = []
for i in range(len(texts_dico['url_objects'])):
	texts_dico['all_titles'] += texts_dico['url_objects'][i].title_lst
	texts_dico['all_texts'] += texts_dico['url_objects'][i].text

#print texts_dico		#This is just for debugging
#print("title length is %d +/- %.0f\ntext length is %d +/- %.0f\nline length is %d +/- %d.") %(texts_dico['title_average'], texts_dico['title_stddev'], texts_dico['text_average'], texts_dico['text_stddev'], texts_dico['line_length_average'], texts_dico['line_length_stddev'])

while True:
	title_as_lst = cap_word(get_markov_text(texts_dico['all_titles'], texts_dico['title_average'], texts_dico['title_stddev']),["i", "i'm", "i'll", "i've"])
	title = first_cap(" ".join(title_as_lst))
	song_as_lst = get_markov_text(texts_dico['all_texts'], texts_dico['text_average'], texts_dico['text_stddev'])
	song_as_lst = cap_word(song_as_lst,["i", "i'm", "i'll", "i've"])
	song = list_to_str(song_as_lst, texts_dico['line_length_average'], texts_dico['line_length_stddev'])

	print "Get ready for it!"
	pause()
	print "\n\nTitle: ", title
	print "\nSong: \n", song

	save_song(title,song)
	
	more = raw_input("Do you want another song? (y/n) ")
	if more.lower() == 'y':
		print ("Here you go. \n")
	elif more.lower() == 'n':
		break
	else:
		print ("I'll take that as a yes. ")
