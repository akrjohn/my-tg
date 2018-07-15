import requests
import bs4
import json
from jmodule import Movies
import jmodule

url='http://tamilgun.vip/categories/hd-movies/'
url_page='http://tamilgun.vip/categories/hd-movies/page/'
page_total=2
		
def main():
	print('Hello John')
	movies = []
	for pg in range(1,page_total):
		tmpMovie = []
		page = url_page+str(pg)
		tmpMovie = jmodule.getMovieList(page)
		movies.extend(tmpMovie)
	#movieJson = json.dumps([m.dump() for m in movies])
	#print(movieJson)
	#jmodule.dumpJson2File('movies12.json',movieJson)
	
	for movie in movies:
		print(movie.getLink())
		movie.saveMovieLinks(jmodule.getMoviesInIframe(movie.getLink()))
		jmodule.insertMovie(movie)

	movieJson1 = json.dumps([m.dumpFull() for m in movies])
	#print(movieJson1)
	jmodule.dumpJson2File('movies12.json',movieJson1)
if __name__ == "__main__":
	main()