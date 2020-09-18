from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import time




conn="mongodb://127.0.0.1:27017"
client=pymongo.MongoClient(conn)
db=client.MissionToMars_DB

hemispheres=db.hemisphere_data.find()

for hemisphere in hemispheres:
	for key, value in hemisphere.items():
		print(f'TITLE: {key}  URL: {value}')


