import time
import pandas as pd
import requests as rs
from lxml import etree

pageurl = 'https://www.hqms.org.cn/usp/roster/index.jsp'
dataurl = 'https://www.hqms.org.cn:443/usp/roster/rosterInfo.jsp'

def getProvinces(url):
    rqpu = rs.get(url)
    html = etree.HTML(rqpu.text)
    provs = html.xpath('//select')
    for p in provs:
        if 'organid' in p.values():
            pv = p
    li = []
    #import pdb;pdb.set_trace()
    try:
        op = pv.xpath('option')
        for o in op:
            if o.attrib['value'] != '':
                li.append(o.attrib['value'])
    except:
        print('got an error')
    return li

def getData(pid):
    data = {'provinceId': pid, 'htype': '', 'hgrade': '', 'hclass': '', 'hname': ''}
    rq = rs.post(dataurl, data=data)
    df = pd.read_json(rq.text)
    df.to_csv('p{0}.csv'.format(pid), index=False, header=False)
    
if __name__ == '__main__':
    print(time.asctime(time.localtime(time.time())))
    pli = getProvinces(pageurl)
    for l in pli:
        getData(l)
    print(time.asctime(time.localtime(time.time())))
    
