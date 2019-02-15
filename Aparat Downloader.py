import telepot
import telepot.namedtuple
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.loop import MessageLoop
import time
import requests
from bs4 import BeautifulSoup
import re

token = "754136717:AAGCusr6Bf_q08mp3BQ8KWlun8zuZptUtmY"
bot = telepot.Bot(token)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)
    m = telepot.namedtuple.Message(**msg)

    
    aparaturl = m.text.split()
    for i in aparaturl:
        if 'aparat.com' not in i:
            pass
        else:
            res = requests.get(i)
            soup = BeautifulSoup(res.content, 'html.parser')
            down = soup.find_all('li', class_='action download-link')
            title = soup.find('li', class_='action download-link')
            title = re.findall(r'title\=\"(.+?)\"', str(title))
            title = title[0]

            dl = []
            for i in down:
                reg = re.findall(r'(https.+?)\"', str(i))
                dl.append(reg[0])
            for i in dl:
                if '144p' in i:
                    Dl144 = i
                elif '240p' in i:
                    Dl240 = i
                elif '480p' in i:
                    Dl480 = i
                elif '720p' in i:
                    Dl720 = i
                elif '1080p' in i:
                    Dl1080 = i

            bot.sendMessage(chat_id,('''
[%s | 144p](%s)
[%s | 240p](%s)
[%s | 480p](%s)
[%s | 720p](%s)''' % (title, Dl144, title, Dl240, title, Dl480, title, Dl720)) , parse_mode='markdown')


def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print ('Inline Query:', query_id, from_id, query_string)

    if ' ' in query_string:
        searchbar = query_string.strip('')
        searchbar = query_string.replace(" ", "_")
        searchurl = ('https://www.aparat.com/search/%s' % (searchbar))
    else:
        searchurl = ('https://www.aparat.com/search/%s' % (query_string))
    ress = requests.get(searchurl)
    soupp = BeautifulSoup(ress.content, 'html.parser')
    videos = soupp.find_all('div', class_="vide-item__info", limit=10)
    videoslinks = []
    videostitles = []
    for i in videos:
        findlinks = i.find('h2', class_="video-item__title")
        videos_links = re.findall(r'(https.+?)\"', str(findlinks))
        videos_links = videos_links[0]
        videoslinks.append(videos_links)
        videos_titles = re.findall(r'title\=\"(.+?)\"', str(findlinks))
        videos_titles = videos_titles[0]
        videostitles.append(videos_titles)

    

    articles = [InlineQueryResultArticle(
                    id='1',
                    title=videostitles[0],
                    input_message_content=InputTextMessageContent(
                        message_text=videoslinks[0]
                    )    
               ),
               InlineQueryResultArticle(
                    id='2',
                    title=videostitles[1],
                    input_message_content=InputTextMessageContent(
                        message_text=videoslinks[1]
                    )    
               ),
               InlineQueryResultArticle(
                    id='3',
                    title=videostitles[2],
                    input_message_content=InputTextMessageContent(
                        message_text=videoslinks[2]
                    )    
               ),
               InlineQueryResultArticle(
                    id='4',
                    title=videostitles[3],
                    input_message_content=InputTextMessageContent(
                        message_text=videoslinks[3]
                    )    
               ),
               InlineQueryResultArticle(
                    id='5',
                    title=videostitles[4],
                    input_message_content=InputTextMessageContent(
                        message_text=videoslinks[4]
                    )    
               )]

    bot.answerInlineQuery(query_id, articles)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)



MessageLoop(bot, {'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result,
                  'chat': handle}).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
            
            
