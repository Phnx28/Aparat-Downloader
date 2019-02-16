import telepot
import telepot.namedtuple
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
import time
import requests
from bs4 import BeautifulSoup
import re

token = "754136717:AAGCusr6Bf_q08mp3BQ8KWlun8zuZptUtmY"
bot = telepot.Bot(token)

def handle(msg): #تابع گرفتن لینک ویدیو
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
            availableq = [] #لینک دانلود کیفیت های مختلف
            qu = [] #کیفیت های مختلف

            for i in down:
                reg = re.findall(r'(https.+?)\"', str(i))
                dl.append(reg[0])
            for i in dl:
                if '144p' in i:
                    Dl144p = i
                    availableq.append(Dl144p)
                    qu.append('144p')
                elif '240p' in i:
                    Dl240p = i
                    availableq.append(Dl240p)
                    qu.append('240p')
                elif '480p' in i:
                    Dl480p = i
                    availableq.append(Dl480p)
                    qu.append('480p')
                elif '720p' in i:
                    Dl720p = i
                    availableq.append(Dl720p)
                    qu.append('720p')
                elif '1080p' in i:
                    Dl1080p = i
                    availableq.append(Dl1080p)
                    qu.append('1080p')

            if len(availableq) == 1:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=('%s'%(qu[0])) , url=availableq[0], callback_data='1')]
                ])
            elif len(availableq) == 2:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=('%s'%(qu[0])) , url=availableq[0], callback_data='1')],
                    [InlineKeyboardButton(text=('%s'%(qu[1])) , url=availableq[1], callback_data='2')]
                ])
            elif len(availableq) == 3:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=('%s'%(qu[0])) , url=availableq[0], callback_data='1')],
                    [InlineKeyboardButton(text=('%s'%(qu[1])) , url=availableq[1], callback_data='2')],
                    [InlineKeyboardButton(text=('%s'%(qu[2])) , url=availableq[2], callback_data='3')]
                ])
            elif len(availableq) == 4:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=('%s'%(qu[0])) , url=availableq[0], callback_data='1')],
                    [InlineKeyboardButton(text=('%s'%(qu[1])) , url=availableq[1], callback_data='2')],
                    [InlineKeyboardButton(text=('%s'%(qu[2])) , url=availableq[2], callback_data='3')],
                    [InlineKeyboardButton(text=('%s'%(qu[3])) , url=availableq[3], callback_data='4')]
                ])
            elif len(availableq) == 5:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=('%s'%(qu[0])) , url=availableq[0], callback_data='1')],
                    [InlineKeyboardButton(text=('%s'%(qu[1])) , url=availableq[1], callback_data='2')],
                    [InlineKeyboardButton(text=('%s'%(qu[2])) , url=availableq[2], callback_data='3')],
                    [InlineKeyboardButton(text=('%s'%(qu[3])) , url=availableq[3], callback_data='4')],
                    [InlineKeyboardButton(text=('%s'%(qu[4])) , url=availableq[4], callback_data='5')]
                ])
            
            bot.sendMessage(chat_id, ('%s' % title), reply_markup=keyboard)



def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


def on_inline_query(msg): #تابع سرج در آپارات
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print ('Inline Query:', query_id, from_id, query_string)

    query_string = query_string.strip('')
    
    if '-s' not in query_string:
        pass
    else:
        joda_search = query_string.split('-')
        query_string = joda_search[0].strip()
        
        if ' ' in query_string:
            searchbar = query_string.replace(" ", "_")
            searchurl = ('https://www.aparat.com/search/%s' % (searchbar))
        else:
            searchurl = ('https://www.aparat.com/search/%s' % (query_string))
        ress = requests.get(searchurl)
        soupp = BeautifulSoup(ress.content, 'html.parser')
        videos = soupp.find_all('div', class_="vide-item__info", limit=5)
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
                  'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
