import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='Enter the url you want to scrape')
parser.add_argument('--file', help='Specify the file name', default="export.csv")
parser.add_argument('--page_number', help='Specify the amount of pages to query', default=1)

args = parser.parse_args()

from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
import time


def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('div', {'class':'resultbox_imagebox'})

def get_title(body):
	if body is not None:
		return name.get('title')

def get_url(body):
	if body is not None:
		if name.a is not None:
			return name.a.get('href')


def which_digit(html):
    mappingDict={'icon-ji':9,
                'icon-dc':'+',
                'icon-fe':'(',
                'icon-hg':')',
                'icon-ba':'-',
                'icon-lk':8,
                'icon-nm':7,
                'icon-po':6,
                'icon-rq':5,
                'icon-ts':4,
                'icon-vu':3,
                'icon-wx':2,
                'icon-yz':1,
                'icon-acb':0,
                }
    return mappingDict.get(html,'')

def get_phone_number(body):
	phone = body.find('span',{'class':'callNowAnchor'})
	if phone is not None:
		return phone.text


def get_rating(body):
	text = body.find('div', {'class':'resultbox_totalrate'})
	if text is not None:
		return text.text

def get_rating_count(body):
	text = body.find('div', {'class':'resultbox_countrate'})
	if text is not None:
		return text.text

def get_address(body):
	address = body.find('div', {'class':'resultbox_address'})
	if address is not None:
		return address.text.strip()

# unable to find location
# def get_location(body):
# 	text = body.find('a', {'class':'rsmap'})
# 	if text == None:
# 		return
# 	text_list = text['onclick'].split(",")
	
# 	latitutde = text_list[3].strip().replace("'", "")
# 	longitude = text_list[4].strip().replace("'", "")
	
# 	return latitutde + ", " + longitude

page_number = 1
page_limit = args.page_number
service_count = 1


fields = ['Title', 'Phone', 'Rating', 'Rating Count', 'Address', 'Url']
out_file = open(args.file,'w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
csvwriter.writeheader()
# Write fields first
#csvwriter.writerow(dict((fn,fn) for fn in fields))
while True:
	time.sleep(2)
	# Check if reached end of result
	if page_number > page_limit:
		break

	url="%s/page-%s" % (args.url, page_number)
	print(url)
	req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
	page = urllib.request.urlopen( req )

	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('div', {'class': 'resultbox'})

	# Iterate through the 10 results in the page
	for service_html in services:
		# Parse HTML to fetch data     
		dict_service = {}
		name = get_name(service_html)
		title = get_title(name)
		url = get_url(name)
		phone = get_phone_number(service_html)
		rating = get_rating(service_html)
		count = get_rating_count(service_html)
		address = get_address(service_html)

		if title != None:
			dict_service['Title'] = title
		if phone != None:
			dict_service['Phone'] = '\'' + phone
		if rating != None:
			dict_service['Rating'] = rating
		if count != None:
			dict_service['Rating Count'] = count
		if address != None:
			dict_service['Address'] = address
		if url != None:
			if (not url.startswith('http')):
				url = 'https://www.justdial.com/jdmart' + url
			dict_service['Url'] = url

		# Write row to CSV
		csvwriter.writerow(dict_service)

		print("#" + str(service_count) + " " , dict_service)
		service_count += 1

	page_number += 1

out_file.close()
