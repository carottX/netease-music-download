import json
import urllib
import urllib.request
import os
import re

class downloader():

    path='D:/music/'
    
    def __init__(self,path):
        if not os.path.exists(path):
            print('The dictinary doesn\' exist. Create one? Y/N')
            op=input()
            if(op=='Y'):
                os.makedirs(path)
            else:
                exit(0)

    def songdownload(self,songid):
        lk='https://api.imjad.cn/cloudmusic/?type=song&id='+songid+'&br=128000'
        song=urllib.request.urlopen(lk)
        songdata=json.loads(song.read())
        downlink=songdata['data'][0]['url']
        detaillk='https://api.imjad.cn/cloudmusic/?type=detail&id='+songid
        detailobj=urllib.request.urlopen(detaillk)
        details=json.loads(detailobj.read())
        songname=details['songs'][0]['name']
        authornames=[]
        authorname=''
        for k in details['songs'][0]['ar']:
            authornames.append(k['name'])
        authorname=''
        for k in range(0,len(authornames)):
            authorname+=authornames[k]
            if k<len(authornames)-1:
                authorname+=','
        try:
            urllib.request.urlretrieve(downlink,self.path+authorname+'-'+songname+'.mp3')
            print('Download Success for Song %s'%(authorname+'-'+songname))
            return 1
        except:
            print('Download Failed for Song %s'%(authorname+'-'+songname))
            return 0

    def playlistdownload(self,playlistid):
        url='https://api.imjad.cn/cloudmusic/?type=playlist&id='+playlistid
        playlist=urllib.request.urlopen(url)
        d=playlist.read()
        txt=json.loads(d)
        songid=[]
        for i in txt['playlist']['trackIds']:
            songid.append(i['id'])
        print('Songs\' ID get! %d in total.'%(len(songid)))
        print('Now trying to download!')
        downloadnum=0
        for j in songid:
            downloadnum+=songdownload(str(j),path)
        print('Download Complete! %d/%d Success in total!'%(downloadnum,len(songid)))

    def getplaylistid(self,playlisturl):
        p=len(playlisturl)-1
        while(p>=0 and playlisturl[p].isdigit()):
            p-=1
        playlistid=playlisturl[p+1:]
        return playlistid

    def getsongid(self,songurl):
        p=len(songurl)-1
        while(p>=0 and songurl[p].isdigit()):
            p-=1
        songid=songurl[p+1:]
        return songid

    def isvalidlink(self,url):
        if re.match('https://music.163.com/#/song?id=\d+',url) or re.match('https://music.163.com/#/playlist?id=\d+',url):
            return True
        else:
            return False


conf=1
s=''
if not os.path.exists('download.conf'):
    print('Find that config file is missing.')
    conf=0
    print('Please input your download path. For example, E:/Audio/Music/')
    s=input()
    print('Change the default to it? Y/N')
    c=input()
    if c=='Y':
        f=open('download.conf','w')
        f.write('path='+s)
        f.close()
else:
    print('Use the default setting? Y/N')
    c=input()
    if c=='Y':
        f=open('download.conf','r')
        try:
            setting=f.readline()
        except:
            f.close()
            print('The conf is broken! Please Check')
            exit(0)
        p=setting.find('=')
        if p==-1:
            f.close()
            print('The conf is broken! Please Check')
            exit(0)
        else:
            s=setting[p+1:]
        f.close()
    else:
        print('Please input your download path. For example, E:/Audio/Music/')
        s=input()
        print('Change the default to it? Y/N')
        c=input()
        if c=='Y':
            f=open('download.conf','w')
            f.write('path='+s)

download=downloader(s)
print('What do you wanna download?1=Playlist,2=Single Song')
c=input()
if c=='1':
    print('Please input your play list link')
    download.playlistdownload(download.getplaylistid(input()))

elif c=='2':
    print('Please input your song list link')
    download.songdownload(download.getsongid(input()))
