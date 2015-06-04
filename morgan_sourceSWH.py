from lxml import html
from lxml import etree
import requests

#store the url for the list of articles and obtain the html tree for that url
base_url = 'http://www.whitehouse.gov'
list_url = '/briefing-room/statements-and-releases'
page = requests.get(base_url+list_url)
list_tree = html.fromstring(page.text)

#get all relative article urls based on the xpath of articles in general
relative_urls = list_tree.xpath("//ul[@class='entry-list']/li/h3/a/@href")

#create an empty list that will be populated with full article urls,
#an empty dictionary that will contain the article contents, 
#and an empty dictionary that will contain a dictionary for each 
#article's contents
article_urls = []
article_contents = {}
article_database = {}

"""
loop through all the relative urls, concatenate the base url with the relative url,
and append them to the empty article_urls list

Note: python lets you do cool/weird things with for() loops.
Here, I'm iterating through the elements in 'relative_urls.'
By placing the temporary variable 'url' in the for() loop syntax,
python automatically assigns the element inside 'relative_urls'
that it's currently on to 'url.' I then add 'base_url' to 'url'
and append it to 'article_urls,' and viola, you have a list of article urls.
"""
for url in relative_urls:
	article_urls.append(base_url+url)

for i in range(0,len(relative_urls)):
	#get the html tree for each article in article_urls
	article = requests.get(article_urls[i])
	article_tree = html.fromstring(article.text)
	#get the title text from each article
	titles = article_tree.xpath("//h1[@property='dc:title']/text()")
	#get the paragraph text (getting both p and ul/li (unordered list and list index) nodes
	words = article_tree.xpath("//div[@id='content']/p/text() | //div[@id='content']/ul/li/text()")
	#get the date of publication of the each article listing
	date = article_tree.xpath("//div[@id='content']/div/div[2]/div[2]/text()") 



	#store the words into the first element of 'article_contents'
	article_contents['title'] = titles
	article_contents['body'] = words
	article_contents['link'] = article_urls[i]
	article_contents['date'] = date
	article_database[i] = article_contents
	print('\n#############################################################################\n')
	print(article_database[i])
