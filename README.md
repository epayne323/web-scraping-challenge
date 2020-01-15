# web-scraping-challenge

In a jupyter notebook, I first scraped data from various Mars-related sites. Then I converted that notebook to a python script and added a function containing all of the scraping code which returned the data as a dictionary.

Unfortunately I was unable to store the data in MongoDB through flask pymongo, and hence I could not display any of the data on the flask site. I still built the basic structure of the site, though.

After the deadline, I edited the home route within app.py to only look for one document within the mars db and in the scrapr route to drop all documents before a new scrape. In index.html, I changed the html field table to render correctly by adding "|safe" after the variable.