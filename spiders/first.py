import requests
from lxml import etree
import webbrowser


def response_view(response):
    request_url = response.url
    base_url = '<head><base href="%s">' % request_url
    base_url = base_url.encode()
    content = response.content.replace(b'<head>', base_url)
    tem_html = open('tmp.html', 'wb')
    tem_html.write(content)
    tem_html.close()

    webbrowser.open_new_tab('tmp.html')


response = requests.get('http://study.163.com')

content = response.content.decode()

html = etree.HTML(content)

mydata = html.xpath('//*[@id="j-nav-catebtn"]/text()')

response_view(response)