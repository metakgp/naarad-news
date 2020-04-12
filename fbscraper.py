from __future__ import print_function

import os
import re
import json
from dateutil.parser import parse, tz
import time
import requests

from frontend import write_html

# Put Facebook 'Access Token' in a plain text file ACCESS_TOKEN in same dir.
# To get an access token follow this SO answer:
# http://stackoverflow.com/a/16054555/1780891

base_url = 'https://graph.facebook.com/v2.8/'
with open('./ACCESS_TOKEN', 'r') as f:
	access_token = f.readline().rstrip('\n')
payload = {'access_token': access_token, 'appsecret_proof':'d05c8510fd28501a023f1b7c3b46d4f5bccb907a2e9c9f43049bdd4864b8ca54','limit': 2}

req_session = requests.Session()


def get_comments(post_id):
	sub_url = post_id + '/comments'

	# scrape the first page
	print('scraping:', sub_url)
	response = req_session.get(base_url + sub_url, params=payload)
	comments = json.loads(response.text)
	data = comments['data']
	return data


def get_picture(post_id, dir="."):
	sub_url = post_id + '?fields=object_id'
	try:
		response = req_session.get(base_url + sub_url, params=payload)
		pic_obj = json.loads(response.text)
		pic_id = pic_obj['object_id']
	except KeyError:
		return None

	try:
		sub_url = pic_id + '?fields=images'
		response = req_session.get(base_url + sub_url, params=payload)
		pic = json.loads(response.text)
		return (pic['images'][0]['source'])
		# f_name = "{}/{}.png".format(dir, pic_id)
		# f_handle = open(f_name, "wb")
		# f_handle.write(pic)
		# f_handle.close()
		# return "{}.png".format(pic_id)
	except KeyError:
		return None


def get_event_picture(post_id, dir="."):
	sub_url = post_id + '?fields=object_id'
	try:
		response = req_session.get(base_url + sub_url, params=payload)
		pic_id = json.loads(response.text)['object_id']
	except KeyError:
		return None
	try:
		sub_url = pic_id + '?fields=cover'
		response = req_session.get(base_url + sub_url, params=payload)
		pic = json.loads(response.text)
		return (pic['cover']['source'])
		# urllib.request.urlretrieve(pic['cover']['source'] , "{}/{}.png".format(dir, pic_id))
		# return "{}.png".format(pic_id)
	except KeyError:
		return None


def get_link(post_id):
	sub_url = post_id + '?fields=link'

	try:
		response = req_session.get(base_url + sub_url, params=payload)
		pic = json.loads(response.text)
		link = pic['link']
	except KeyError:
		return None

	return link


def get_event(post_id, page_id):
	sub_url = page_id + '/events'
	response = req_session.get(base_url + sub_url, params=payload)
	all_events = json.loads(response.text)

	message = """
{}
Date: {}
Time: {}
Veunu: {}
	"""
	for event in all_events['data']:
		if event['id'] in post_id:
			DateTime = prettify_date([{'created_time': event['start_time']}])
			if 'description' in event.keys():  # checking if the event have description
				message = message.format(event['description'],
										 DateTime[0]['real_time'],
										 DateTime[0]['real_date'],
										 event['place']['name'])
			else:
				message = message.format(event['name'],
										 DateTime[0]['real_time'],
										 DateTime[0]['real_date'],
										 event['place']['name'])
			return message


def get_shared_post(post_id):
	print (post_id)
	sub_url = post_id + '?fields=parent_id'
	# getting id of the original post
	try :	
		response = req_session.get(base_url + sub_url, params=payload)
		parent_id = json.loads(response.text)['parent_id']
		query = parent_id + '?fields=message'
	except KeyError :
		query = post_id + '?fields=message'
	try :
		response = req_session.get(base_url + query, params=payload)
		original_message = json.loads(response.text)['message']
	except KeyError :
		original_message = ""
	return original_message

def get_video(post_id) :
	video_id = post_id.split('_')[1]
	sub_url = video_id + "?fields=embeddable"
	try : 
		response = req_session.get(base_url + sub_url, params=payload)
		embed_flag = json.loads(response.text)['embeddable']
	except KeyError:
		return ""
	if embed_flag : #checking if the video is embedddable 
		embed_html_url=video_id + '?fields=from,source'
		response = req_session.get(base_url + embed_html_url, params=payload)
		query = json.loads(response.text)
		video_url = query['source']
		page_name = query['from']['name']
		msg = """<b>{} shared the following video\n\n
				<video width="320" height="240" controls>
				<source src="{}" >
				 Your browser does not support the video tag.
					</video>""".format(page_name,video_url)
		return msg
	else : 
		return ""
def get_feed(page_id, pages=10):
	# check last update time
	try:
		old_data = json.load(open('docs/{}.json'.format(page_id), 'r'))
		last_post_time = parse(old_data[0]['created_time'])
	except FileNotFoundError:
		old_data = []
		last_post_time = parse("1950-01-01T12:05:06+0000")

	sub_url = page_id + '/feed'

	# scrape the first page
	print('scraping:', sub_url)
	response = req_session.get(base_url + sub_url, params=payload)
	feed = json.loads(response.text)
	print('payload is ', payload)
	print('feed is ', feed)
	new_page_data = feed['data']

	data = []
	is_new_post = (parse(new_page_data[0]['created_time']) > last_post_time)

	if is_new_post:
		data = new_page_data

	# determine the next page
	next_page = feed['paging']['next']
	next_search = re.search('.*(until=[0-9]+)', next_page, re.IGNORECASE)
	if next_search:
		the_until_arg = next_search.group(1)

	pages = pages - 1

	# scrape the rest of the pages
	while (next_page is not False) and is_new_post and pages > 0:
		sub_url = page_id + '/feed?' + the_until_arg
		print('baking:', sub_url)
		try:
			response = req_session.get(base_url + sub_url, params=payload)
			feed = json.loads(response.text)
			new_page_data = feed['data']
			is_new_post = (
				parse(new_page_data[0]['created_time']) > last_post_time)

			data.extend(new_page_data)
		except requests.exceptions.RequestException:
			print('start again at', the_query)
			break

		# determine the next page, until there isn't one
		try:
			next_page = feed['paging']['next']
			next_search = re.search(
				'.*(until=[0-9]+)', next_page, re.IGNORECASE)
			if next_search:
				the_until_arg = next_search.group(1)
		except IndexError:
			print('last page...')
			next_page = False
		pages = pages - 1
		for post_dict in data:
			post_dict['pic'] = get_picture(post_dict['id'], dir='docs')
			post_dict['link'] = get_link(post_dict['id'])
			if "story" in post_dict :  #Events and shared post have story key
				if "event" in post_dict['story'] :
					post_dict['message'] = get_event(post_dict['id'], page_id)
					post_dict['pic'] = get_event_picture(post_dict['id'],dir='docs')
				elif "shared" in post_dict['story'] :

					post_dict['message'] = '<b>' + post_dict['story'] + '</b>' + '\n\n' + get_shared_post(post_dict['id']) 

			  #  print (post_dict['message'])
			else :
				if not "message" in post_dict :
					post_dict['message'] = get_video(post_dict['id'])

			
	data.extend(old_data)
	data.sort(key=lambda x: parse(x['created_time']), reverse=True)

	json.dump(data, open('docs/{}.json'.format(page_id), 'w'))

	return data


def remove_duplicates(data):
	uniq_data = []
	for item in data:
		if item not in uniq_data:
			uniq_data.append(item)

	return uniq_data


def prettify_date(data):
	for item in data:
		date = parse(item['created_time'])
		tzlocal = tz.gettz('Asia/Kolkata')
		local_date = date.astimezone(tzlocal)
		item['real_date'] = local_date.strftime('%d-%m-%Y')
		item['real_time'] = local_date.strftime('%I:%M%p')
	return data


def get_aggregated_feed(pages):
	"""
	Aggregates feeds give a list of pages and their ids.

	Input: A list of tuples
	Output: Combined list of posts sorted by timestamp
	"""
	data = list()
	for page_name, _id in pages:
		page_data = get_feed(_id)
		for data_dict in page_data:
			data_dict['source'] = page_name
		data.extend(page_data)

	data.sort(key=lambda x: parse(x['created_time']), reverse=True)
	return data


if __name__ == "__main__":
	# Great thanks to https://gist.github.com/abelsonlive/4212647
	news_pages = json.load(open("./pages.json"))
	# for_later = ['Cultural-IIT-Kharagpur']

	data = get_aggregated_feed(news_pages)
	data = remove_duplicates(data)
	data = prettify_date(data)

	json.dump(data, open('docs/feed.json', 'w'))
	write_html(data, 'docs/index.html')

	localtime = str(time.asctime( time.localtime(time.time()) ))
	stamp="            <font size=2 color=\"white\"><div align=\"right\"><b>Last updated: "+localtime+" IST</b></div></font>\n"
	fn=open("docs/index.html","r+")
	fo=open("docs/indext.html","w")
	while (True):
  		abc=fn.readline()
  		fo.write(abc)
  		if not abc: break
  		if (abc[:30]=="            <!Time stamp here>"):    fo.write(stamp)
fn.close()
fo.close()
os.system("mv docs/indext.html docs/index.html")