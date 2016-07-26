import urllib.request
from bs4 import BeautifulSoup
import bs4
import re

def GetObject(values,index):
    count = 0
    for v in values:
        if(count == index):
            return v
        else:
            count += 1

hour = re.compile(r'\d{1,2}小时')   
min = re.compile(r'\d{1,2}分钟')       
def DateFilt(date):
    if(date == '今天'):
        return True
    elif hour.match(date):
        return True
    elif min.match(date):
        return True
    else:
        return False
        
        
def GrabZF(url):
    print(url)
    header = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers = header)
    response = urllib.request.urlopen(req)
    
    with open("response.html","wb")as f:
        f.write(response.read())
   
    soup = BeautifulSoup(open("response.html",'r',encoding= 'utf-8'),'html.parser')
    with open("response.html","wb")as f:
        f.write(soup.prettify().encode())
    '''
    data=urllib.request.urlopen(url).read()  
    page_data=data.decode('utf-8')  
    soup=BeautifulSoup(page_data) '''
    #soup = BeautifulSoup(response.read())
   # print('s:' + soup.prettify()+' s')
    col = soup.find(class_="wrentm")
    
    result = ''
    for tr in col.children:
        if 'tr' != tr.name:
            continue 
        p = tr.find('p', class_="qj-renaddr")
        if not p :
            continue
        Date = GetObject(p.stripped_strings,4)
        if not DateFilt(Date):
            continue
        result += r'<tr><td>'
        result += Date
        for a in tr.find_all('a',href = re.compile(r'http://\S*58.com\S*')):
            result += a.prettify()
        for b in tr.find_all('b', class_="pri"):
            result += b.prettify()
        for span in tr.find_all('span', class_="showroom"):
            result += span.prettify()
        result += '</td></tr><tr/>'
    return result

    
if __name__ == '__main__':
    with open('result.html', 'wb') as result:
        result.write(r'<head><meta content="text/html; charset=utf-8" http-equiv="Content-Type"/></head>'.encode('utf-8'))
        result.write(r'<table cellpadding="0" cellspacing="0" class="tbimg">'.encode('utf-8'))
        for i in range(1,11,1):
            result_html = GrabZF('http://gz.58.com/dongpu/chuzu/pn' + str(i) + '/?utm_source=market&spm=b-31580022738699-me-f-824.bdpz_biaoge_house01')
            result.write(result_html.encode('utf-8'))
        result.write(r'</table>'.encode('utf-8'))
    