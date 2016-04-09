from __future__ import print_function
from facepy import GraphAPI
import facepy
import re
import json
from frontend import write_html
from dateutil.parser import parse

# You need to have the Access Token is stored in a plain text file ACCESS_TOKEN
# to get an access token follow this SO answer: http://stackoverflow.com/a/16054555/1780891
with open('./ACCESS_TOKEN', 'r') as file_handle:
    access_token = file_handle.readline().rstrip('\n')

graph = GraphAPI(access_token)


def getcomments(post_id):
    base_query = post_id + '/comments'

    # scrape the first page
    print('scraping:', base_query)
    comments = graph.get(base_query)
    data = comments['data']
    return data


def getfeed(page_id, pages=1):
    base_query = page_id + '/feed?limit=100'

    # scrape the first page
    print('scraping:', base_query)
    feed = graph.get(base_query)
    data = feed['data']

    total_scraped = 0

    # determine the next page
    next = feed['paging']['next']
    next_search = re.search('.*(\&until=[0-9]+)', next, re.IGNORECASE)
    if next_search:
        the_until_arg = next_search.group(1)

    pages = pages - 1

    # scrape the rest of the pages
    while (next is not False) and pages > 0:
        the_query = base_query + the_until_arg
        print('baking:', the_query)
        try:
            feed = graph.get(the_query)
            data.append(feed['data'])
        except facepy.exceptions.OAuthError:
            print('start again at', the_query)
            break

        # determine the next page, until there isn't one
        try:
            next = feed['paging']['next']
            next_search = re.search('.*(\&until=[0-9]+)', next, re.IGNORECASE)
            if next_search:
                the_until_arg = next_search.group(1)
        except IndexError:
            print('last page...')
            next = False
        total_scraped = total_scraped + 100
        print(total_scraped, 'pies in the face so far')
        pages = pages - 1

    return data


def get_aggregated_feed(pages):
    """
    Aggregates feeds give a list of pages and their ids.

    Input: A list of tuples
    Output: Combined list of posts sorted by timestamp
    """
    data = list()
    for page_name, _id in pages:
        page_data = getfeed(_id)
        for data_dict in page_data:
            data_dict['source'] = page_name
        data.extend(page_data)

    data.sort(key=lambda x: parse(x['created_time']), reverse=True)
    return data


if __name__ == "__main__":
    # Great thanks to https://gist.github.com/abelsonlive/4212647
    news_pages = [('The Scholar\'s Avenue', 'scholarsavenue'), ('Awaaz IIT Kharagpur', 'awaaziitkgp')]
    for_later = ['Cultural-IIT-Kharagpur']
    data = get_aggregated_feed(news_pages)
    json.dump(data, open('feed.json', 'w'))
    write_html(data, 'feed.html')
