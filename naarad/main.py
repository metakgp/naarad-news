# import argparse
import json
from naarad.fbscraper import scrape
from naarad.frontend import write_html


def main():
    news_pages = [('The Scholar\'s Avenue', 'scholarsavenue'),
                  ('Awaaz IIT Kharagpur', 'awaaziitkgp'),
                  ('Technology Students Gymkhana', 'TSG.IITKharagpur'),
                  ('Technology IIT KGP', 'iitkgp.tech'),
                  ('IIT Kharagpur (Official Page)', 'iitkgp')]
    scrape(news_pages)

    data = json.load(open('output/feed.json', 'r'))

    write_html(data, 'output/feed.html')
