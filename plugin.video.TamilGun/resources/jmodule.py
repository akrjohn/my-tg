#JModule
import requests
import bs4
import json

class Movies(object):
	def __init__(self,name, link, image):
		self.name = name
		self.link = link
		self.image = image
		
	def printMovie(self):
		print(self.name, self.link, self.image)
		
	def getLink(self):
		return self.link
		
	def getImage(self):
		return self.image
		
	def getMovieName(self):
		return self.name

	def saveMovieLinks(self, movieLinks):
		self.movieLinks = movieLinks
	
	def dump(self):
		return {"movie": {'name': self.name,
				'link': self.link,
				'image': self.image}}
				
	def dumpFull(self):
		return {"movie": {'name': self.name,
				'link': self.link,
				'image': self.image,
				'movieLinks': self.movieLinks}}			
				
'''
Gets the page data.
'''
def getPage(page):
	if page is not None:
		try:
			r = requests.get(page)
			if r.status_code == 200:
				return r
		except requests.exceptions.RequestException as e:
			print('Error loading url')
			return None
	return None
		
def dumpJson2File(fileName, jsonObj):
	obj = open(fileName, 'w')
	obj.write(jsonObj)
	obj.close
		

def getMoviesInIframe(iframe):
	print('Hello John')
	movieLinks = []
	r = getPage(iframe)
	if r is not None:
		soup = bs4.BeautifulSoup(r.text)
		frames = soup.findAll('iframe')
		for frame in frames:
			url1 = frame.get('src')
			r1 = getPage(url1)
			if r1 is not None:
				soup1 = bs4.BeautifulSoup(r1.text)
				scripts = soup1.findAll('script')
				sources = soup1.findAll('source')
				for script in scripts:
					scr1 = script.text.split('"')
					for s in scr1:
						if s.startswith('http://') and s.endswith('mp4'):
							#print(s)
							movieLinks.append(s)
				for source in sources:
					link = source.get('src')
					if link.endswith('mp4'):
						movieLinks.append(link)
	return movieLinks
	
def getMovieList(url):
	r = getPage(url)
	movies = []
	if r is not None:
		soup = bs4.BeautifulSoup(r.text)
		movieList =  soup.findAll("div", class_="col-lg-3 col-md-3 col-sm-12 item")
		#Creating an array of movie objects
		for movie in movieList:
			section = movie.find('section')
			mTitle = section.find('h3').find('a').get('title')
			mLink = section.find('h3').find('a').get('href')
			mImage = movie.find('img').get('src').strip()
			m = Movies(mTitle,mLink,mImage)
			#m.printMovie()
			movies.append(m)
			#print(mTitle)
	
	return movies
	#movieJson = json.dumps([m.dump() for m in movies])
	#print(movieJson)
	#dumpJson2File('movies.json',movieJson)
	
def insertMovie(movie):
	movieJson = json.dumps(movie.dumpFull())
	headerInfo={'Content-Type':'application/json'}
	users = requests.post('http://localhost:5984/movies/', data=movieJson , headers=headerInfo)
	#return json.dumps((users.text))