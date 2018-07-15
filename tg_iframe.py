import requests
import bs4
import json
from jmodule import Movies

url='http://tamilgun.vip/video/kattappava-kanom-hd/'
url_page='http://tamilgun.vip/categories/hd-movies/page/'
page_total=29

def getPage(page):
	r = requests.get(page)
	if r.status_code == 200:
		return r
	else:	
		return None
		
def main():
	print('Hello John')
	moviesLinks = []
	r = requests.get(url)
	soup = bs4.BeautifulSoup(r.text)
	frames = soup.findAll('iframe')
	for frame in frames:
		url1 = frame.get('src')
		if url1 is not None:
			r1 = requests.get(url1)
			soup1 = bs4.BeautifulSoup(r1.text)
			scripts = soup1.findAll('script')
			for script in scripts:
				scr1 = script.text.split('"')
				for s in scr1:
					if s.startswith('http://') and s.endswith('mp4'):
						print(s)
		
if __name__ == "__main__":
	main()