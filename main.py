from pytube import *
from youtubesearchpython import VideosSearch, Playlist, playlist_from_channel_id, ChannelsSearch, Comments
import pyfzf.pyfzf, os
import re

def replacesym(basestr,a):
    for char in a:
        if char not in basestr:
            a = a.replace(char, '-')
    return a

def updatechannels():
    global basestr, channellist, channelnames, channellinks
    basestr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяИАБВГДЕЁЖЗЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890.!?-()[]{}:; "
    channellist = []
    channelnames = []
    channellinks = {}
    id = 1
    channelnames.append("-1. Выход")
    channelnames.append("0. Подписаться")
    if os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") != 0:
        file = open("channels.txt", "r")
        channellist = file.read().split("\n")
        file.close()
    else:
        channellist = []
    for i in channellist:
        if i != "":
            channel = Channel(i)
            chname = channel.channel_name
            bit = replacesym(basestr, chname).lower()
            channelnames.append(str(id) + ". " + bit)
            channellinks.update({id: i})
            id = id + 1
        else:
            continue
    channelnames.append("1000. Обновить список")
    channelnames.append("1001. Поиск видео")
    channelnames.append("1002. Поиск каналов")
    channelnames.append("1003. Отписаться")

fzf = pyfzf.pyfzf.FzfPrompt()
updatechannels()
while True:
    channel_id = fzf.prompt(channelnames)
    channelid = channel_id[0].split(". ")[0]
    if channelid == "-1":
        print("Спасибо что используешь Pyyt!")
        exit()
    elif channelid == "0":
        u = input("Ссылка на канал: ")
        file = open("channels.txt", "a")
        if os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") != 0:
            file.write("\n" + u)
        elif os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") == 0:
            file.write(u)
        file.close()
        updatechannels()
    elif channelid == "1003":
        print("Загрузка...")
        unsubnames = []
        unsublinks = {}
        id = 1
        if os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") != 0:
            file = open("channels.txt", "r")
            unsublist = file.read().split("\n")
            file.close()
        else:
            channellist = []
        for i in channellist:
            if i != "":
                channel = Channel(i)
                chname = channel.channel_name
                bit = replacesym(basestr, chname).lower()
                unsubnames.append(str(id) + ". " + bit)
                unsublinks.update({id: i})
                id = id + 1
            else:
                continue
        unsub = fzf.prompt(unsubnames)[0].split(". ")[0]
        unsuburl = unsublinks[int(unsub)]
        with open('channels.txt') as f:
            lines = f.readlines()
        pattern = re.compile(re.escape(unsuburl))
        with open('channels.txt', 'w') as f:
            for line in lines:
                result = pattern.search(line)
                if result is None:
                    f.write(line)
        updatechannels()
    elif channelid == "1000":
        print("Загрузка...")
        updatechannels()
    elif channelid == "1002":
        u = input("Поисковой запрос: ")
        csearch = ChannelsSearch(u, limit = 1000)
        id = 1
        channelnames = []
        channellinks = {}
        for i in csearch.result()["result"]:
            channel = Channel(i["link"])
            channelnames.append(str(id) + ". " + channel.channel_name)
            channellinks.update({id: i["link"]})
            id = id + 1
        newchnames = []
        for i in channelnames:
            bit = replacesym(basestr, i).lower()
            newchnames.append(bit)
        channelnames = newchnames
        prompt = fzf.prompt(channelnames)
        c = Channel(channellinks[int(prompt[0].split(". ")[0])])
        allname = []
        links = {}
        id = 1
        actions = ["1. Смотреть видео с этого канала", "2. Подписаться на этот канал"]
        actprompt = fzf.prompt(actions)
        if actprompt[0].split(". ")[0] == "1":
            playlist = Playlist(playlist_from_channel_id(c.channel_id))
            while playlist.hasMoreVideos:
                playlist.getNextVideos()
            for i in playlist.videos:
                v = YouTube(i["link"])
                allname.append(str(id) + ". " + i["title"])
                links.update({id: [i["link"], i["title"]]})
                id = id + 1
            newallname = []
            for i in allname:
                bit = replacesym(basestr, i).lower()
                newallname.append(bit)
            allname = newallname
            vid = fzf.prompt(allname)
            vidid = int(vid[0].split(". ")[0])
            actions = ["1. Посмотреть", "2. Описание", "3. Превью", "4. Комментарии"]
            actprompt = fzf.prompt(actions)
            videolink = links.get(vidid)[0].split("&list=")[0]
            video = YouTube(videolink)
            if actprompt[0].split(". ")[0] == "1":
                os.system("mpv " + str(videolink))
            elif actprompt[0].split(". ")[0] == "2":
                print(video.description)
                u = input("\nНажмите Enter...")
            elif actprompt[0].split(". ")[0] == "3":
                print("Ссылка: " + video.thumbnail_url)
                u = input("\nНажмите Enter...")
            elif actprompt[0].split(". ")[0] == "4":
                comments = Comments(videolink)
                while comments.hasMoreComments:
                    comments.getNextComments()
                allcomments = []
                for i in comments.comments["result"]:
                    allcomments.append(i["author"]["name"] + ": " + i["content"])
                fzf.prompt(allcomments)
            updatechannels()
        if actprompt[0].split(". ")[0] == "2":
            u = c.channel_url
            file = open("channels.txt", "a")
            if os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") != 0:
                file.write("\n" + u)
            elif os.path.isfile("channels.txt") == True and os.path.getsize("channels.txt") == 0:
                file.write(u)
            file.close()
        updatechannels()
    elif channelid == "1001":
        allname = []
        links = {}
        id = 0
        u = input("Поисковой запрос: ")
        srx = VideosSearch(u, limit=1000)
        for i in srx.result()["result"]:
            v = YouTube(i["link"])
            allname.append(str(id) + ". " + i["title"])
            links.update({id: [i["link"], i["title"]]})
            id = id + 1
        newallname = []
        for i in allname:
            bit = replacesym(basestr, i).lower()
            newallname.append(bit)
        allname = newallname
        vid = fzf.prompt(allname)
        vidid = int(vid[0].split(". ")[0])
        actions = ["1. Посмотреть", "2. Описание", "3. Превью", "4. Комментарии"]
        actprompt = fzf.prompt(actions)
        videolink = links.get(vidid)[0].split("&list=")[0]
        video = YouTube(videolink)
        if actprompt[0].split(". ")[0] == "1":
            os.system("mpv " + str(videolink))
        elif actprompt[0].split(". ")[0] == "2":
            print(video.description)
            u = input("\nНажмите Enter...")
        elif actprompt[0].split(". ")[0] == "3":
            print("Ссылка: " + video.thumbnail_url)
            u = input("\nНажмите Enter...")
        elif actprompt[0].split(". ")[0] == "4":
            comments = Comments(videolink)
            while comments.hasMoreComments:
                comments.getNextComments()
            allcomments = []
            for i in comments.comments["result"]:
                allcomments.append(i["author"]["name"] + ": " + i["content"])
            fzf.prompt(allcomments)
    else:
        print("Загрузка...")
        c = Channel(channellinks[int(channelid)])
        allname = []
        links = {}
        id = 1
        playlist = Playlist(playlist_from_channel_id(c.channel_id))
        while playlist.hasMoreVideos:
            playlist.getNextVideos()
        for i in playlist.videos:
            v = YouTube(i["link"])
            allname.append(str(id) + ". " + i["title"])
            links.update({id: [i["link"], i["title"]]})
            id = id + 1
        newallname = []
        for i in allname:
            bit = replacesym(basestr, i).lower()
            newallname.append(bit)
        allname = newallname
        vid = fzf.prompt(allname)
        vidid = int(vid[0].split(". ")[0])
        actions = ["1. Посмотреть", "2. Описание", "3. Превью", "4. Комментарии"]
        actprompt = fzf.prompt(actions)
        videolink = links.get(vidid)[0].split("&list=")[0]
        video = YouTube(videolink)
        if actprompt[0].split(". ")[0] == "1":
            os.system("mpv " + str(videolink))
        elif actprompt[0].split(". ")[0] == "2":
            print(video.description)
            u = input("\nНажмите Enter...")
        elif actprompt[0].split(". ")[0] == "3":
            print("Ссылка: " + video.thumbnail_url)
            u = input("\nНажмите Enter...")
        elif actprompt[0].split(". ")[0] == "4":
            comments = Comments(videolink)
            while comments.hasMoreComments:
                comments.getNextComments()
            allcomments = []
            for i in comments.comments["result"]:
                allcomments.append(i["author"]["name"] + ": " + i["content"])
            fzf.prompt(allcomments)
