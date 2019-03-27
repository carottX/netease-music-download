import json
import urllib
import urllib.request
import os

print('Please input your playlist link:')
l=input()
#example: https://music.163.com/#/playlist?id=2714194426
print('Please input the path to save the music.There should be a "/" at last \nFor example, D:/music/')
path=input()
if not os.path.exists(path):
    print('The dictinary doesn\' exist. Create one? Y/N')
    op=input()
    if(op=='Y'):
        os.makedirs(path)
    else:
        exit(0)
playlistid=''
p=len(l)-1
while(p>=0 and l[p].isdigit()):
    p-=1
playlistid=l[p+1:]
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
    lk='https://api.imjad.cn/cloudmusic/?type=song&id='+str(j)+'&br=128000'
    song=urllib.request.urlopen(lk)
    songdata=json.loads(song.read())
    downlink=songdata['data'][0]['url']
    detaillk='https://api.imjad.cn/cloudmusic/?type=detail&id='+str(j)
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
        urllib.request.urlretrieve(downlink,path+authorname+'-'+songname+'.mp3')
        print('Download Success for Song %s'%(authorname+'-'+songname))
        downloadnum+=1
    except:
        print('Download Failed for Song %s'%(authorname+'-'+songname))
print('Download Complete! %d/%d Success in total!'%(downloadnum,len(songid)))
