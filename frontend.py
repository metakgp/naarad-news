import json
from django.utils.encoding import smart_str
from jinja2 import Template
import commonregex

parser = commonregex.CommonRegex()


def fixnewlines(message):
    return message.replace('\n', ' <br> ')




# def shortify_string(message):
    
#     message = message.split(" ")
#     new_message = ""    
#     for mess in message :
#         if len(mess) > 25 :
#             mess = " <a href='" + mess + "' target='_blank'> " + mess[0:25] + "... </a> "
#         new_message = new_message + mess + " "
    
#     return new_message 
 

def truncate(message,length):

    while length < len(message):
        if message[length] == " ":
            if length == len(message)-1:
                return message[0:length]
            else:     
                return message[0:length]
        length = length+1
    return message[0:len(message)-1]

def truncate_length(message,length):

    while length < len(message):
        if message[length] == " ":
            if length == len(message)-1:
                return None
            else:     
                return 1 
        length = length+1
    return None

def enable_links(message):
    if '<video width="320" height="240" controls>' in message :
        return message
    links = parser.links(message)
    links = list(set(links))
    url_identifier = ["www","http","bit.ly",".com",".co.in"]
    for link in links:
        flag = 0
        for keyword in url_identifier :
            if keyword in link :
                flag = 1
                break
        if flag is 0 :
            break
        http_link = link
        if not link.startswith('http'):
            http_link = 'http://{}'.format(link)
        if len(link) < 25:
            link = link[0:25]
            message = message.replace(link, ' <a href=\'{}\' target=\'_blank\'> {} </a> '.format(http_link, link) , 1)
        else:    
           # message = shortify_string(message)
            message = message.replace(link, ' <a href=\'{}\' target=\'_blank\'> {} </a> '.format(http_link, link[0:25]+'...') ,1 ) 

        message = message.replace("\"","'")   
    return message

def get_big_screen_array(data):
    final_data = []
    n = len(data)
    # if n%3 != 1 :
    for i in range(0,n,3) :
        final_data.append(data[i])
    for i in range(1,n,3) :
        final_data.append(data[i])
    for i in range(2,n,3) :
        final_data.append(data[i])                
    # else : 
    #     l1 = len(range(0,n,3)) - 1
    #     l2 = l1 + len(range(2,n,3))
    #     for i in range(0,n,3) :
    #         final_data.append(data[i])
    #     for i in range(1,n,3) :
    #         final_data.append(data[i])
    #     final_data.append(final_data[l1])
    #     final_data[l1] = data[n-1] 
    #     for i in range(2,n-3,3) :
    #         final_data.append(data[i])

    return final_data

def get_html(data):
    template_raw = open('feed.tmpl', 'r').read()

    for post in data:
        if 'message' in post:
            post['message'] = fixnewlines(post['message'])
            if 'flag' not in post :
                post['message'] = enable_links(post['message'])
                post['flag'] = 1 
            post['message'] = post['message'].replace("\"","'")   
            post['short_message'] = truncate(post['message'],150)
            post['read_more'] = truncate_length(post['message'],150)
    json.dump(data, open('docs/feed.json', 'w'))
    template = Template(template_raw)
    data2 = get_big_screen_array(data)
    html = template.render(data=[data,data2])
    # smart_str helps in unicode rendering
    return smart_str(html)


def write_html(data, file_name):
    html = get_html(data)
    file_handle = open(file_name, 'w', encoding="utf8")
    file_handle.write(html)


if __name__ == "__main__":
    data = json.load(open('docs/feed.json', 'r'))

    write_html(data, 'docs/index.html')
