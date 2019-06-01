from tkinter import *
from tkinter.ttk import *
import os
import urllib.request as urllib2
import json

def getsongid(songurl):
    p=len(songurl)-1
    while(p>=0 and songurl[p].isdigit()):p-=1
    songid=songurl[p+1:]
    return songid

def delinvalid(s):
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

def song(songid):
    global w3
    lk='https://api.imjad.cn/cloudmusic/?type=song&id='+songid+'&br=128000'
    song=urllib2.urlopen(lk)
    songdata=json.loads(song.read())
    downlink=songdata['data'][0]['url']
    detaillk='https://api.imjad.cn/cloudmusic/?type=detail&id='+songid
    detailobj=urllib2.urlopen(detaillk)
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
    print(download_path+name)
    if os.path.isfile(download_path+name):
        w3['text']='Already Exists Song %s. Skipped'%(name)
        return 1
    try:
        urllib2.urlretrieve(downlink,download_path+name)
        w3['text']='Song %s Download Success!'%(songname)
        return 1
    except:
        w3['text']='Download Failed for Song %s'%(songname)
        return 0

def dl_song():
    songurl=e1.get()
    song(getsongid(songurl))


def getplaylistid(playlisturl):
    p=len(playlisturl)-1
    while(p>=0 and playlisturl[p].isdigit()):p-=1
    playlistid=playlisturl[p+1:]
    return playlistid

def playlist():
    global w3
    global download_path
    playlistid=getplaylistid(e2.get())
    url='https://api.imjad.cn/cloudmusic/?type=playlist&id='+playlistid
    playlist=urllib2.urlopen(url)
    d=playlist.read()
    txt=json.loads(d)
    songid=[]
    tdp=download_path
    download_path+=txt['playlist']['name'].replace('/','／')+'/'
    print(download_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    for i in txt['playlist']['trackIds']:
        songid.append(i['id'])
    w3['text']='Downloading...'
    downloadnum=0
    for j in songid:
        downloadnum+=song(str(j))
    download_path=tdp
    w3['text']='Download Complete! %d/%d Success in total!'%(downloadnum,len(songid))

path = os.path.split(os.path.realpath(__file__))
download_path=path[0]+'\\downloads\\'
download_path=download_path.replace('\\','/')
if not os.path.exists(download_path):
    os.makedirs(download_path)
root=Tk()
root.wm_title('Netease GUI Downloader')
w1=Label(root,text='Single Song Link:')
w1.grid(row=0,column=0,sticky=W)
w2=Label(root,text='Playlist Link:')
w2.grid(row=1,column=0,sticky=W)
w3=Label(root,text='')
w3.grid(row=2,column=0,sticky=W)
e1=Entry(root)
e1.grid(row=0,column=1,sticky=W)
e2=Entry(root)
e2.grid(row=1,column=1,sticky=W)
b1=Button(root,text='download!',command=dl_song)
b1.grid(row=0,column=2,sticky=W)
b2=Button(root,text='download!',command=playlist)
b2.grid(row=1,column=2,sticky=W)
root.mainloop()
