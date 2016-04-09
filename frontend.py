import jinja2
from jinja2 import Template
import json


def fixnewlines(data):
    for post in data:
        try:
            post['message'] = post['message'].replace('\n', '<br>')
        except KeyError:
            pass
    return data


def get_html(data):
    template_raw = "".join(open('feed.tmpl', 'r').readlines())
    template = Template(template_raw)
    data = fixnewlines(data)
    html = template.render(data=data)
    return html


def write_html(data, file_name):
    html = get_html(data)
    file_handle = open(file_name, 'w')
    file_handle.write(html)


if __name__ == "__main__":
    data = json.load(open('output/feed.json', 'r'))

    write_html(data, 'output/feed.html')
