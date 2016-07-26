class zfInfo:
    dist = ''
    title = ''
    url = ''
    date = ''
    pri = 0.00
    room = 1
    pic_url = ''
    
class zfInfos:
    def __init__(self):
        self._zfInfos = []

    def push(self, _zfInfo):
        for info in self._zfInfos:
            if(info.url == _zfInfo.url):
                return -1
            if(info.title == _zfInfo.title):
                return -1
        self._zfInfos.append(_zfInfo)
        return 0