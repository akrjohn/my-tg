import requests
import bs4
import json
from jmodule import Movies

url='http://tamilgun.vip/categories/hd-movies/'
url_page='http://tamilgun.vip/categories/hd-movies/page/'
page_total=29

def getPage(page):
	r = requests.get(page)
	if r.status_code == 200:
		return r
	else:	
		return None

def dumpJson2File(fileName, jsonObj):
	obj = open(fileName, 'w')
	obj.write(jsonObj)
	obj.close
		
def main():
	print('Hello John')
	movies = []
	#r = requests.get(url)
	for pg in range(1,page_total):
		#Generating the page.
		page = url_page+str(pg)
		r = getPage(page)
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
				print(mTitle)
				#print(json.dumps(m.__dict__))	
			#print(len(movies))
			
	movieJson = json.dumps([m.dump() for m in movies])
	print(movieJson)
	dumpJson2File('movies.json',movieJson)
	#fileObj = open('movies.txt', 'wb')
	#json.dump([m.dump() for m in movies], fileObj)
	#dumpJson2File('movie.txt',json.dumps([m.dump() for m in movies])) 
if __name__ == "__main__":
	main()