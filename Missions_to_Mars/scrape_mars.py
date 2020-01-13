from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.parse import urljoin

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    scraped_dict = {}
    
    browser = init_browser()

    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    soup = bs(browser.html, 'html.parser')

    # Using BS, we can execute standard functions to capture the page's content
    news_title_text = soup.find("div", class_="content_title").text
    news_paragraph_text = soup.find("div", class_="article_teaser_body").text
    scraped_dict["news_title_text"] = news_title_text
    scraped_dict["news_paragraph_text"] = news_paragraph_text


    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
    browser.visit(JPL_url)
    soup = bs(browser.html, 'html.parser')
    #currently featured image's max size is medium. ALSO, there is no mars-specific featured image?
    featured_image_url = urljoin(JPL_url, soup.find("a", class_="button fancybox")["data-fancybox-href"])
    scraped_dict["featured_image_url"] = featured_image_url


    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)
    soup = bs(browser.html, 'html.parser')
    mars_weather_tweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    scraped_dict["mars_weather_tweet"] = mars_weather_tweet


    mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts_html = mars_facts.to_html()
    scraped_dict["mars_facts_html"] = mars_facts_html


    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    soup = bs(browser.html, 'html.parser')
    descriptions = soup.find_all('div', class_='description')
    hemisphere_image_urls = []

    for i in descriptions:
        title = ""
        tsplit = i.h3.text.split(" ")
        for t in tsplit:
            title += t
            if t == "Hemisphere":
                break
            else:
                title += " "
        
        browser.visit(urljoin(mars_hemispheres_url, i.a["href"]))
        soup = bs(browser.html, 'html.parser')
        img_url = soup.find('a', text='Sample')["href"]
        
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    scraped_dict["hemisphere_image_urls"] = hemisphere_image_urls

    
    return scraped_dict