from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import time
# I removed imports needed for testing

# These are for testing purposes
#conn="mongodb://127.0.0.1:27017"
#client=pymongo.MongoClient(conn)
#db=client.MissionToMars_DB

#-----------------------------------------------------------------
def mars_scrape():
	executable_path= {"executable_path": "/usr/local/bin/chromedriver"}
	browser = Browser("chrome", **executable_path, headless=False)

	url='https://mars.nasa.gov/news/'
	browser.visit(url)
	time.sleep(2)
	soup=bs(browser.html, 'html.parser')

	news_title=soup.find('ul', {'class': 'item_list'}).find('div', class_= 'content_title')
	news_title=news_title.get_text().strip()

	article_teaser=soup.find('ul', {'class': 'item_list'}).find('div', class_= 'article_teaser_body')
	news_p=article_teaser.get_text().strip()


	#-----------------------------------------------------------------
	url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)
	time.sleep(2)
	browser.find_by_id("full_image").click()
	browser.find_by_text("more info     ").click()

	soup=bs(browser.html, 'html.parser')

	full_image=soup.find('img', {'class': 'main_image'})['src']
	full_image=f"https://www.jpl.nasa.gov{full_image}"
	
	#-----------------------------------------------------------------
	titles=[]
	hemispheres=[]

	url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url)
	time.sleep(2)
	soup=bs(browser.html, 'html.parser')

	hemisphere_types=soup.find_all('div', {'class': 'description'})

	for each in hemisphere_types:
		titles.append(each.find('a').text)
		
	for title in titles:
		hemisphere={}
		browser.find_by_text(title).click()
		time.sleep(1)
		soup1=bs(browser.html, 'html.parser')
		image_url=(f"https://astrogeology.usgs.gov{soup1.find('img', {'class': 'wide-image'})['src']}")
		hemisphere['title']=title
		hemisphere['img_url']=image_url
		hemispheres.append(hemisphere)
		browser.back()

	browser.quit()
	
	#-----------------------------------------------------------------
	url='https://space-facts.com/mars'
	tables=pd.read_html(url)
	df=tables[0]
	df.columns=['Description', 'Mars']
	df.set_index('Description', inplace=True)
	dt=df.to_html()
	

	post={"$set": {'news_title': news_title,
	'news_p': news_p,
	'feature_image_url': full_image,
	'mars_facts': dt,
	'hemisphere_image_urls': hemispheres
	}}
	
	# These is for testing purposes
	# collection=db.mission_to_mars_data
	# collection.update_one({}, post, upsert=True)
	return post
		

# Use this function call for testing
# mars_scrape()





















