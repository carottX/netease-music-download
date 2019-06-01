import json
import urllib
import urllib.request
import os
import re

class downloader():

    path='D:/music/'
    searchmin=10
    
    def delinvalid(self,s):
        s=s.replace('/','／')
        s=s.replace('\\','＼')
        s=s.replace(':','：')
        s=s.replace('*','＊')
        s=s.replace('?','？')
        s=s.replace('"','＂')
        s=s.replace('<','＜')
        s=s.replace('>','＞')
        s=s.replace('|','｜')
        return s
    
    def __init__(self,p,mins):
        self.path=p
        self.searchmin=mins
        if not os.path.exists(p):
            print('The dictinary doesn\' exist. Create one? Y/N')
            op=input()
            if(op=='Y'):
                os.makedirs(p)
            else:
                exit(0)

    def song(self,songid):
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
        name=authorname+'-'+songname+'.mp3'
        name=delinvalid(name)
        if os.path.isfile(self.path+name):
            print('Already Exists Song %s. Skipped'%(name))
            return 1
        try:
            urllib.request.urlretrieve(downlink,self.path+name)
            print('Download Success for Song %s'%(name))
            return 1
        except:
            print('Download Failed for Song %s'%(name))
            return 0

    def playlist(self,playlistid):
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
            downloadnum+=self.song(str(j))
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
        songurl='https://music.163.com/#/song?id='
        playlisturl='https://music.163.com/#/playlist?id='
        if url[0:len(songurl)]==songurl and url[len(songurl):].isdigit():
            return 'song'
        elif url[0:len(playlisturl)]==playlisturl and url[len(playlisturl):].isdigit():
            return 'playlist'
        else:
            return None

    def search(self,songname):
        searchurl='https://api.imjad.cn/cloudmusic/?type=search&search_type=1&s='+songname
        searchdata=urllib.request.urlopen(searchurl)
        d=searchdata.read()
        res=json.loads(d)
        p=0
        while(p<len(res['result']['songs'])):
            for i in range(0,min(len(res['result']['songs'])-p,self.searchmin)):
                result=res['result']['songs'][i+p]
                songname=result['name']
                authornames=[]
                authorname=''
                for k in result['ar']:
                    authornames.append(k['name'])
                authorname=''
                for k in range(0,len(authornames)):
                    authorname+=authornames[k]
                    if k<len(authornames)-1:
                        authorname+=','
                print('%d:%s-%s link:%s'%(i+1,authorname,songname,'https://music.163.com/#/song?id='+str(result['id'])))
            p+=self.searchmin
            print('%d:Next Page'%(min(len(res['result']['songs'])-p,self.searchmin)+1))
            print('%d:Exit'%(min(len(res['result']['songs'])-p,self.searchmin)+2))
            print('Input your choice')
            c=input()
            cn=0
            while(True):
                try:
                    cn=int(c)
                    if(0<cn<=min(len(res['result']['songs'])-p,self.searchmin)+2):
                        break
                    else:
                        print('Wrong Input!Try Again')
                        c=input()
                except:
                    print('Wrong Input!Try Again')
                    c=input()
            if(0<cn<=min(len(res['result']['songs'])-p,self.searchmin)):
                print('Choosed.Trying to download...')
                self.song(str(res['result']['songs'][cn-1+p]['id']))
                print('Finished')
                break
            elif cn==min(len(res['result']['songs'])-p,self.searchmin)+1:
                   continue
            else:
                   break

conf=1
s=''
ms=''
mms=0
if not os.path.exists('download.conf'):
    print('Find that config file is missing.')
    conf=0
    print('Please input your download path. For example, E:/Audio/Music/')
    s=input()
    print('Please input your minimum result per page for the search For example:10')
    ms=input()
    try:
        mms=int(ms)
    except:
        print('Invalid input!')
        exit(0)
    print('Change the default to it? Y/N')
    c=input()
    if c=='Y':
        f=open('download.conf','w')
        f.write('path='+s)
        f.write('\n')
        f.write('searchmin='+ms)
        f.close()
else:
    print('Use the default setting? Y/N')
    c=input()
    if c=='Y':
        f=open('download.conf','r')
        for i in range(0,2):
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
                if i==0:
                    s=setting[p+1:]
                    s=s.strip('\n')
                    s=s.strip(' ')
                elif i==1:
                    ms=setting[p+1:]
                    try:
                        mms=int(ms)
                    except:
                        print('The conf is broken! Please Check')
                        f.close()
                        exit(0)
        f.close()
    else:
        print('Please input your download path. For example, E:/Audio/Music/')
        s=input()
        print('Please input your minimum result per page for the search For example:10')
        ms=input()
        try:
            mms=int(ms)
        except:
            print('Invalid input!')
            exit(0)
        print('Change the default to it? Y/N')
        c=input()
        if c=='Y':
            f=open('download.conf','w')
            f.write('path='+s)
            f.write('\n')
            f.write('searchmin='+ms)
            f.close()

#print(s,mms)

download=downloader(s,mms)
print('Search&Download songs=1 Download song/playlist=2')
c=input()
if c=='2':
    print('Please input your playlist/song link')
    link=input()
    if download.isvalidlink(link)=='song':
        download.song(download.getsongid(link))
    elif download.isvalidlink(link)=='playlist':
        download.playlist(download.getplaylistid(link))
    else:
        print('Wrong link!Please check!')
        exit(0)
elif c=='1':
    print('Please input the search content')
    download.search(input())
