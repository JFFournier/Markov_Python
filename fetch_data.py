""" By JFF. From Markov Project.
This module 
	- fetches lyrics from the web,
		- use urllib2
	- cleans it
		- removes html encoding ??? Get list of codes to remove/ how is formatted? 
			--> use BeautifulSoup() then Get_text() ref https://www.crummy.com/software/BeautifulSoup/bs4/doc/
	- compiles the different songs  (
		- use a dictionnary : song title/song lyric 
		- concat lyrics and dump the whole thing in a file
	- computes average song length and std dev
		- iterate through dictionnary; use counter (for i in a for i)"""
	
import urllib2
import re
from bs4 import BeautifulSoup

class UrlText(object):
	#Attributes are url, title, title_lst, title_len, text, text_len, url_title_file, url_text_file
	
	def __init__(self, file_or_url, url, url_title_file, url_text_file):
		self.file_or_url = file_or_url
		self.url = url
		self.url_title_file = url_title_file
		self.url_text_file = url_text_file
		#gets the text and title
		self.get_data()
		#gets the lengths of title and text
		self.stats()
		
	def __repr__(self):
		return "This is %s; it has %d words in the title and %d in the text.\n" %(self.title, self.title_len, self.text_len)
		
	# url as string; returns clean data from it as a list of two elements: title + text
	#creates attributes text, title and title_lst from url or file; writes files with text and title
	def get_data(self):
		#If user wants to look at URLs, then parses them using BeautifulSoup
		if self.file_or_url.lower() == 'u':
			try:
				url_open = urllib2.urlopen(self.url)
			except:
				print "Bad internet or web address. Try restarting box. "
				quit()
			raw_html = url_open.read()
			soup = BeautifulSoup(raw_html, 'html.parser')
			
			#find_next_siblings("b") #gets only the <b> tagged text; - the title of the text
			b_tag_title = soup.find_all("b", limit=2)
			#Gets from the list only the 2nd element which contains the title (first is junk)
			title_str = unicode(b_tag_title[1])
			#Makes a soup out of it so we can use get_text() to clean it
			title_soup = BeautifulSoup(title_str,"html.parser")
			self.title = title_soup.get_text() + "\n"
			#writes content to a file - with ponctuation
			self.url_title_file.write(self.title.encode('utf-8'))

			#gets only the <br> tagged text; that is text with hard returns (poems or lyrics)
			br_tag_text = soup.br.br.div
			self.text = br_tag_text.get_text()
			self.url_text_file.write(self.text.encode('utf-8') + "\nEND OF TEXT\n")
			
		#If user wants to read from a file, then reads the file to get data
		else:
			self.text = ""
			self.title = self.url_title_file.readline().decode('utf-8')
			line = self.url_text_file.readline().decode('utf-8') 
			#Reads each line, but stops when the text is marked as ended
			while line != "END OF TEXT\n":
				#Removes empty lines
				if line != "\n":
					self.text += line
				line = self.url_text_file.readline().decode('utf-8')

		#writes content to a file - without ponctuation
		with open("clean_title.txt", "a") as title_file:
			self.title = re.sub('-+',' ',self.title)
			self.title = re.sub('[;:!.?,"()]','',self.title)
			title_file.write(self.title.encode('utf-8'))

		with open("clean_txt.txt", "a") as txt_file:
			self.text = re.sub('-+',' ',self.text).lower()
			self.text = re.sub('[;:!.?,"()\n]','',self.text)
			txt_file.write(self.text.encode('utf-8'))
			
		#split title to a list ; filter-None removes empty strings from list
		self.title_lst = filter(None,re.split('\s+',self.title))
		#split text to a list ; filter-None removes empty strings from list
		self.text = filter(None,re.split('\s+',self.text))
		
	def stats(self):
		try:
			self.title_len = len(self.title_lst)
			self.text_len = len(self.text)
		except AttributeError:
			get_data()
			self.title_len = len(self.title_lst)
			self.text_len = len(self.text)
		
def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
	
#calculates average from list of numbers
def average(numbers):
	return sum(numbers)/float(len(numbers))

#calculates std deviation from arithmetic mean of a list of numbers
def stddev(numbers):
	num_average = average(numbers)
	error_sum = 0
	for num in numbers:
		error_sum += (num_average - num)**2
	return (error_sum/len(numbers))**0.5 

#url_list=['http://www.azlyrics.com/lyrics/morrissey/alsatiancousin.html', 'http://www.azlyrics.com/lyrics/morrissey/littlemanwhatnow.html']

# gets the list of urls from call; this is the  main function that runs the whole thing
def __main__(ans_data_source, url_list):
	#file_or_url = 'f'	# uncomment for faster debugging of using only data in files

	#I was a bit lazy; this to avoid changing variable lower and in functions; stems from code change
	if ans_data_source == 'a':
		file_or_url = 'f'
		url_title_file =  open("title_from_url.txt", "r")
		url_text_file =  open("text_from_url.txt", "r")
	else:
		file_or_url = 'u'
		url_title_file = open("title_from_url.txt", "w")
		#Added '+ 'so file can be read to get lines length
		url_text_file = open("text_from_url.txt", "w+")
		print "Done erasing files"
		
	#deletes files (if any) for clean and no ponctuation files
	with open("clean_title.txt", "w") as title_file:
		pass
	with open("clean_txt.txt", "w") as txt_file:
		pass


	titles_len_lst = []
	texts_len_lst = []
	#this is a dictionnary of the UrlText Class objects and will contain other stats; this is the returned variable
	texts_dico = {
		'url_objects' : []}

	#url_list = ['http://www.azlyrics.com/lyrics/morrissey/everydayislikesunday.html'] #for debugging ; look at faulty url
	
	try:
		#Creates as  many UrlText objects as a list in dico as there are URLs in the list.
		for i in range(0,len(url_list)):
			#in the case of running local db; url_list is non-sensical
			texts_dico['url_objects'].append(UrlText(file_or_url, url_list[i], url_title_file, url_text_file))
			titles_len_lst.append(texts_dico['url_objects'][i].title_len)
			texts_len_lst.append(texts_dico['url_objects'][i].text_len)
			#print "Added to database:", texts_dico['url_objects'][i].title
			print "Added to database text No ", i+1
	except TypeError:
		print "Empty list. Try starting from scratch."
		quit()
		
	print ("\ntitle_from_url.txt and text_from_url.txt written. You can save for later if you want.")	
	
	#Read the text file to get the number of words in each line as a list & number of lines
	url_text_file.seek(0,0)
	txt_line_length_lst = []
	txt_no_lines = 0
	txt_no_lines_lst = []
	for line in url_text_file:
		if not (line == "\n" or line == "\r\n"):
			txt_line_length_lst.append(len(line.split(' ')))
			if line == "END OF TEXT\n":
				txt_no_lines_lst.append(txt_no_lines)
				txt_no_lines = 0
			else:
				txt_no_lines += 1
			
	url_title_file.close()
	url_text_file.close()
		
	texts_dico['title_average'] = int(average(titles_len_lst))
	texts_dico['title_stddev'] = int(stddev(titles_len_lst))
	texts_dico['text_average'] = int(average(texts_len_lst))
	texts_dico['text_stddev'] = int(stddev(texts_len_lst))
	texts_dico['line_length_average'] = int(average(txt_line_length_lst))
	texts_dico['line_length_stddev'] = int(stddev(txt_line_length_lst))
	texts_dico['txt_no_lines_average'] = int(average(txt_no_lines_lst))
	texts_dico['txt_no_lines_stddev'] = int(stddev(txt_no_lines_lst))
	
	return texts_dico
	#print url_text_list, titles_len_lst, texts_len_lst
	#print("title length is %d +/- %.0f\ntext length is %d +/- %.0f\n There are %d +/1 %d lines.") %(title_average, title_stddev, text_average, text_stddev, txt_no_lines_average, txt_no_lines_stddev)
