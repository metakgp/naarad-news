import json
from django.utils.encoding import smart_str
from jinja2 import Template
import commonregex

parser = commonregex.CommonRegex()


def fixnewlines(message):
    return message.replace('\n', '<br>')


def enable_links(message):
    links = parser.links(message)

    for link in links:
        http_link = link
        if not link.startswith('http'):
            http_link = "http://{}".format(link)

        message = message.replace(link, "<a href=\"{}\" target=\"_blank\">{}</a>".format(http_link, link))

    return message


def get_html(data):
    template_raw = open('feed.tmpl', 'r').read()

    for post in data:
        if 'message' in post:
            post['message'] = enable_links(post['message'])
            post['message'] = fixnewlines(post['message'])

    template = Template(template_raw)
    html = template.render(data=data)
    # smart_str helps in unicode rendering
    return smart_str(html)


def write_html(data, file_name):
    html = get_html(data)
    file_handle = open(file_name, 'w')
    file_handle.write(html)


if __name__ == "__main__":
    data = json.load(open('docs/feed.json', 'r'))

    write_html(data, 'docs/index.html')
