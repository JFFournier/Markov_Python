""" This module 
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
		
		

"""
response = urllib2.urlopen('http://www.gutenberg.org/files/135/135-h/135-h.htm')
html = response.read()

#print html
sad = 0

list_of_words = html.split(' ')

for word in list_of_words:
    if word == 'sad':
        sad += 1
print sad

soup = BeautifulSoup(html, 'html.parser')
print soup.get_text()
"""


import urllib2
import re
from bs4 import BeautifulSoup


class UrlText(object):
	"""Attributes are url, title, title_lst, title_len, text, text_len, url_title_file, url_text_file"""
	
	def __init__(self, file_or_url, url, url_title_file, url_text_file):
		self.file_or_url = file_or_url
		self.url = url
		self.url_title_file = url_title_file
		self.url_text_file = url_text_file
		self.get_data()														#gets the text and title
		self.stats()														#gets the lengths of title and text
		
	
	def __repr__(self):
		return "This is %s; it has %d words in the title and %d in the text.\n" %(self.title, self.title_len, self.text_len)
		
	def get_data(self): 							# url as string; returns clean data from it as a list of two elements: title + text
		#creates attributes text, title and title_lst from url or file; writes files with text and title
				
		if self.file_or_url.lower() == 'u':										#If user wants to look at URLs, then parses them using BeautifulSoup
			try:
				url_open = urllib2.urlopen(self.url)
			except:
				print "Bad internet or web address. Try restarting box. "
				quit()
			raw_html = url_open.read()
			soup = BeautifulSoup(raw_html, 'html.parser')
			
			b_tag_title = soup.find_all("b", limit=2) 							#find_next_siblings("b") #gets only the <b> tagged text; - the title of the text
			title_str = unicode(b_tag_title[1])									#Gets from the list only the 2nd element which contains the title (first is junk)
			title_soup = BeautifulSoup(title_str,"html.parser")					#Makes a soup out of it so we can use get_text() to clean it
			self.title = title_soup.get_text() + "\n"
			self.url_title_file.write(self.title.encode('utf-8'))				#writes content to a file - with ponctuation

			br_tag_text = soup.br.br.div 										#gets only the <br> tagged text; that is text with hard returns (poems or lyrics)
			self.text = br_tag_text.get_text()
			self.url_text_file.write(self.text.encode('utf-8') + "\nEND OF TEXT\n")
			
		else:																	#If user wants to read from a file, then reads the file to get data
			self.text = ""
			self.title = self.url_title_file.readline().decode('utf-8')
			line = self.url_text_file.readline().decode('utf-8') 
			while line != "END OF TEXT\n":										#Reads each line, but stops when the text is marked as ended
				if line != "\n":												#Removes empty lines
					self.text += line
				line = self.url_text_file.readline().decode('utf-8')

		with open("clean_title.txt", "a") as title_file:						#writes content to a file - without ponctuation
			self.title = re.sub('-+',' ',self.title)
			self.title = re.sub('[;:!.?,"()]','',self.title)
			title_file.write(self.title.encode('utf-8'))

		with open("clean_txt.txt", "a") as txt_file:
			self.text = re.sub('-+',' ',self.text).lower()
			self.text = re.sub('[;:!.?,"()\n]','',self.text)
			txt_file.write(self.text.encode('utf-8'))
			
		self.title_lst = filter(None,re.split('\s+',self.title))				#split title to a list ; filter-None removes empty strings from list
		self.text = filter(None,re.split('\s+',self.text))						#split text to a list ; filter-None removes empty strings from list
		
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
	
def average(numbers): 				#calucates average from list of numbers
	return sum(numbers)/float(len(numbers))

def stddev(numbers):				#calculates std deviation from arithmetic mean of a list of numbers
	num_average = average(numbers)
	error_sum = 0
	for num in numbers:
		error_sum += (num_average - num)**2
	return (error_sum/len(numbers))**0.5 


	
#url_list=['http://www.azlyrics.com/lyrics/morrissey/alsatiancousin.html', 'http://www.azlyrics.com/lyrics/morrissey/littlemanwhatnow.html']

def __main__(ans_data_source, url_list):																# gets the list of urls from call; this is the  main function that runs the whole thing
	#file_or_url = 'f'																# uncomment for faster debugging of using only data in files

	if ans_data_source == 'a':														#I was a bit lazy; this to avoid changing variable lower and in functions; stems from code change
		file_or_url = 'f'
		url_title_file =  open("title_from_url.txt", "r")
		url_text_file =  open("text_from_url.txt", "r")
	else:
		file_or_url = 'u'
		url_title_file = open("title_from_url.txt", "w")
		url_text_file = open("text_from_url.txt", "w+")								#Added '+ 'so file can be read to get lines length
		print "Done erasing files"
		
	with open("clean_title.txt", "w") as title_file:								#deletes files (if any) for clean and no ponctuation files
		pass
	with open("clean_txt.txt", "w") as txt_file:
		pass


	titles_len_lst = []
	texts_len_lst = []
	texts_dico = {
		'url_objects' : []}															#this is a dictionnary of the UrlText Class objects and will contain other stats; this is the returned variable

	#url_list = ['http://www.azlyrics.com/lyrics/morrissey/everydayislikesunday.html'] #for debugging ; look at faulty url
	
	try:
		for i in range(0,len(url_list)):											#Creates as  many UrlText objects as a list in dico as there are URLs in the list.
			texts_dico['url_objects'].append(UrlText(file_or_url, url_list[i], url_title_file, url_text_file))	#in the case of running local db; url_list is non-sensical
			titles_len_lst.append(texts_dico['url_objects'][i].title_len)
			texts_len_lst.append(texts_dico['url_objects'][i].text_len)
			#print "Added to database:", texts_dico['url_objects'][i].title
			print "Added to database text No ", i+1
	except TypeError:
		print "Empty list. Try starting from scratch."
		quit()
		
	print ("\ntitle_from_url.txt and text_from_url.txt written. You can save for later if you want.")	
		
	url_text_file.seek(0,0)															#Read the text file to get the number of words in each line as a list & number of lines
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

