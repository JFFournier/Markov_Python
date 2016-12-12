# Markov_Python
CodeAcademy.com Python project: Creates new lyrics using a Markov Chain

 Requires BeautifulSoup and urllib2

<B> Just run 'run_lyrics_generator.py' in Python (2.7) to run this program. </B>

This program will ask user for a source of data (default list for Morrissey and Suede provided); parse the html source to get the clean text, saves the text in files, create a Markov object then generate a new song using Markov chain. Average and standard deviations for the compilations of text are use to get similar lengths. Users can then save the files.

If like me you have crappy internet, your internet box might get confused hitting http://www.azlyrics.com/ so many times and you may need to reset it. In that case, just edit the default_lists.py. If you still want to use all the texts, you can merge the text/title_from_url.txt files.
