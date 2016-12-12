""" By JFF. From Markov Project.
This modules creates a MarkovChain object that takes a text (from list or file if list_from_file called), can generate a Markov Chain relationship using a dictionnary 
(call get_markov function; stored in object) and cann generate a Markov Chain by calling the generate_markov_chain function (returned as a list)."""

import random

class MarkovChain(object):
	#create variable; count is number of words prefix
	def __init__(self,liste=[], count=2):
		self.liste = liste
		#for word in liste: #lower case specified in fetch_data module now
		#	self.liste.append(word.lower())
		self.count = count
	
	#generates the input list from the specified file instead of specifying a list directly
	def lst_from_file(self, file):
		with open(file, 'r') as f:
			text = f.read()
			self.liste = text.split(' ')

	#figures out the prefix/suffix relationship of Markov Chain using a dictionary.
	def get_markov(self):
		len_lst = len(self.liste)
		#creates the dictionary from prefix/suffix relationship
		self.markov = {}
		i = 0
		#for every word in list,
		while i+self.count < len_lst:
			#create prefix of 'count' words as the key in markov dictionary...
			prefix = self.liste[i:i+self.count]
			#... and create the suffix as the value associated to the key
			suffix = self.liste[i+self.count]
			#print "The i is %d, the prefix is %s and the suffix is %s\n" %(i, prefix, suffix) #this is for debugging
			try:
				#if key already exists, then just add to it
				self.markov[" ".join(prefix)].append(suffix)
			#if first time the key/prefix is seen, then create the dictionary key
			except KeyError:
				try:
					self.markov[" ".join(prefix)] = [suffix]
				except:										
					print "THERE WAS AN ERROR THAT SHOULD NOT HAVE HAPPENED"
					print i, self.count, len_lst
					print self.markov
			except TypeError:
				print "THERE WAS AN ERROR THAT SHOULD NOT HAVE HAPPENED"
				print i, self.count, len_lst
				print self.markov
			i += 1 
	
	#Generate the Markov Chain as a list of words. Specify length as the maximum; but could stop if end-of-chain is met first	
	def generate_markov_chain(self, length):
		try:
			#checks that get_markov was run
			markov = self.markov
		#if get_markov() was not run before, then run it now.
		except AttributeError:
			self.get_markov()
		#-1 'cause list is longer than index and another and -self.count to not put the last word as first word; last word might not have a next word
		try:
			init_pos = random.randint(0,len(self.liste)-1-self.count)
		except ValueError:
			init_pos = 0
		#initiates chain randomly
		chain = self.liste[init_pos:init_pos+self.count]
		i = 0
		#advances one word at a time, taking the self.count last words as prefix/key
		while i + self.count < length:
			prefix = chain[i:i+self.count]
			link = " ".join(prefix)
			try:
				#add to the chain one randomly chosen suffix/value that corresponds to the key/prefix as stored in markov dictionary.
				chain += [self.markov[link][random.randint(0,len(self.markov[link])-1)]]
			except KeyError:
				#end of chain (and text) has been reached
				break
			i += 1
		return chain
