import json
import requests as rs
from lxml import etree

li = [x*20 for x in range(11)]
shortDicts = [] 
url = 'https://movie.douban.com/subject/26213252/comments?start={}&limit=20&sort=new_score&status=P'

for num in li:
    res = rs.get(url.format(num))
    if res.status_code == 200:
        html = etree.HTML(res.text)
        comments = html.xpath('.//div[@class="comment-item"]')
        for ct in comments:
            cinfo = ct.xpath('.//span[@class="comment-info"]')
            username = cinfo[0].xpath('.//a/text()')[0]
            userurl = cinfo[0].xpath('.//a')[0].attrib['href']
            cttime = cinfo[0].xpath('.//span[@class="comment-time "]')[0].attrib['title']
            content = ct.xpath('.//span[@class="short"]/text()')[0]
            shortDicts.append({
                'username': username,
                'userurl': userurl,
                'cttime': cttime,
                'content': content,
            })
    else:
        print('get request got error')
        continue

for sd in shortDicts:
    print(sd)

#with open('shorts.txt', 'w') as fo:
#    for sd in shortDicts:
#        fo.write(str(sd)+'\n')

with open('shorts.json', 'w') as fo:
    json.dump(shortDicts, fo)
