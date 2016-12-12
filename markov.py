""" This modules creates a MarkovChain object that takes a text (from list or file if list_from_file called), can generate a Markov Chain relationship using a dictionnary 
(call get_markov function; stored in object) and cann generate a Markov Chain by calling the generate_markov_chain function (returned as a list)."""

import random

class MarkovChain(object):
	def __init__(self,liste=[], count=2):									#create variable; count is number of words prefix
		self.liste = liste
		#for word in liste: #lower case specified in fetch_data module now
		#	self.liste.append(word.lower())
		self.count = count
	
	def lst_from_file(self, file):											#generates the input list from the specified file instead of specifying a list directly
		with open(file, 'r') as f:
			text = f.read()
			self.liste = text.split(' ')

	def get_markov(self):													#figures out the prefix/suffix relationship of Markov Chain using a dictionary.
		len_lst = len(self.liste)
		self.markov = {}													#creates the dictionary from prefix/suffix relationship
		i = 0
		while i+self.count < len_lst:										#for every word in list,
			prefix = self.liste[i:i+self.count]								#create prefix of 'count' words as the key in markov dictionary...
			suffix = self.liste[i+self.count]								#... and create the suffix as the value associated to the key
			#print "The i is %d, the prefix is %s and the suffix is %s\n" %(i, prefix, suffix) #this is for debugging
			try:
				self.markov[" ".join(prefix)].append(suffix)				#if key already exists, then just add to it
			except KeyError:												#if first time the key/prefix is seen, then create the dictionary key
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
			
	def generate_markov_chain(self, length):								#Generate the Markov Chain as a list of words. Specify length as the maximum; but could stop if end-of-chain is met first
		try:
			markov = self.markov											#checks that get_markov was run
		except AttributeError:												#if get_markov() was not run before, then run it now.
			self.get_markov()
		init_pos = random.randint(0,len(self.liste)-1-self.count)			#-1 'cause list is longer than index and another and -self.count to not put the last word as first word; last word might not have a next word
		chain = self.liste[init_pos:init_pos+self.count]					#initiates chain randomly
		i = 0
		while i + self.count < length:										#advances one word at a time, taking the self.count last words as prefix/key
			prefix = chain[i:i+self.count]
			link = " ".join(prefix)
			try:
				chain += [self.markov[link][random.randint(0,len(self.markov[link])-1)]]	#add to the chain one randomly chosen suffix/value that corresponds to the key/prefix as stored in markov dictionary.
			except KeyError:
				break														#end of chain (and text) has been reached				
			i += 1
		return chain