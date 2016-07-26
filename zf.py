import urllib.request
from bs4 import BeautifulSoup
import bs4
import re
from zfInfo import zfInfo
from zfInfo import zfInfos

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

def GetResponse(url):
    header = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers = header)
    response = urllib.request.urlopen(req)
    
    with open("response.html","wb")as f:
        f.write(response.read())
        
def GrabOnePageInfo(url, _zfInfos):
    GetResponse(url)
    soup = BeautifulSoup(open("response.html",'r',encoding= 'utf-8'),'html.parser')
    col = soup.find(class_="wrentm")
    if not col:
        GetResponse(url)
        soup = BeautifulSoup(open("response.html",'r',encoding= 'utf-8'),'html.parser')
        col = soup.find(class_="wrentm")
        if not col:
            return -1
    
    with open("response.html","wb")as f:
        f.write(soup.prettify().encode())
    '''
    data=urllib.request.urlopen(url).read()  
    page_data=data.decode('utf-8')  
    soup=BeautifulSoup(page_data) '''
    #soup = BeautifulSoup(response.read())
   # print('s:' + soup.prettify()+' s')


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
        _zfInfo = zfInfo()
        _zfInfo.date = Date
        for a in tr.find_all('a',class_='t'):
            result += a.prettify()
            _zfInfo.url = a['href']
            _zfInfo.title = a.string
            break
        for b in tr.find_all('b', class_="pri"):
            result += b.prettify()
            _zfInfo.pri = float(b.string)
        for span in tr.find_all('span', class_="showroom"):
            result += span.prettify()
        result += '</td></tr><tr/>'

        _zfInfos.push(_zfInfo)
        #print( _zfInfo.title + '\n' + _zfInfo.url + '\n' + _zfInfo.date + '\n' + '%d'%_zfInfo.pri)
    return 0

def GrabRentInfo(dist, _zfInfos):
    for i in range(1,11,1):
        url = 'http://gz.58.com/' + dist + '/chuzu/pn' + str(i) + '/?utm_source=market&spm=b-31580022738699-me-f-824.bdpz_biaoge_house01'
        ret = GrabOnePageInfo(url, _zfInfos)
        print('%s:%d:  total : %d'%(url, ret, len(_zfInfos._zfInfos)))
        
        
def WriteHtml(result_html, link_html, _zfInfos):
    result_html.write('<head><meta content="text/html; charset=utf-8" http-equiv="Content-Type"/><script type="text/javascript" src="jquery-latest.js"></script>\
        <script type="text/javascript" src="jquery.tablesorter.js" ></script></head>'.encode('utf-8'))
    result_html.write('<body>'.encode('utf-8'))
    result_html.write('<script type="text/javascript">'.encode('utf-8'))
    result_html.write('$(document).ready(function() \
                { \
                $("#myTable").tablesorter(); \
                } \
                );'.encode('utf-8'))
    result_html.write('</script>'.encode("utf-8"))
    result_html.write(link_html.encode('utf-8'))
    result_html.write(r'<table id="myTable" class="tablesorter">'.encode('utf-8'))
    result_html.write('<thead> \
                <tr> \
                <th>title</th> \
                <th>date</th> \
                <th>pri</th> \
                </tr> \
                </thead> \
                <tbody> '.encode('utf-8'))
            
    
    for info in _zfInfos._zfInfos:
        result_html.write(('<tr> \
        <td>' + '<a href = "' +  info.url + '">' + info.title + '</a></td> \
        <td>' + info.date + '</td> \
        <td>' + str(info.pri) + '</td> \
        </tr>').encode('utf-8'))
    result_html.write(r'</tbody></table></body>'.encode('utf-8'))
    
    
if __name__ == '__main__':
    dists = {'dongpu', 'huangcun'}
            
    link_html = ""
    for dist in dists:
        link_html  = link_html + '<a href = "' + dist + '.html">' + dist + '</a><br />'
    
    for dist in dists:
        _zfInfos = zfInfos()    
        GrabRentInfo(dist, _zfInfos)
        
        with open(dist + '.html', 'wb') as result_html:
            WriteHtml(result_html, link_html, _zfInfos)
        
        