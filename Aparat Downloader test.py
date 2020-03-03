import telepot
import telepot.namedtuple
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
import time
import requests
from bs4 import BeautifulSoup
import re

token = ""
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
        videos_soup = soupp.find_all('div', class_="vide-item__info", limit=10)
        videoslinks = []
        videostitles = []
        for i in videos_soup:
            findlinks = i.find('h2', class_="video-item__title")
            videos_links = re.findall(r'(https.+?)\"', str(findlinks))
            videos_links = videos_links[0]
            videoslinks.append(videos_links)
            videos_titles = re.findall(r'title\=\"(.+?)\"', str(findlinks))
            videos_titles = videos_titles[0]
            videostitles.append(videos_titles)
        
        #add thumbnail to search results
        thumbnails_soup = soupp.find_all('div', class_="video-item__thumb-wrapper", limit=10)
        thumbnailslinks = []
        for i in thumbnails_soup:
            find_thumbnails_links = i.find('a', class_="video-item__thumb")
            thumnail_links = re.findall(r'url\((.+?)\)', str(find_thumbnails_links))
            thumnail_links = thumnail_links[0]
            thumbnailslinks.append(thumnail_links)

        articles = [InlineQueryResultArticle(
                        id='1',
                        title=videostitles[0],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[0]
                        ),
                        thumb_url=thumbnailslinks[0]    
                ),
                InlineQueryResultArticle(
                        id='2',
                        title=videostitles[1],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[1]
                        ),
                        thumb_url=thumbnailslinks[1]    
                ),
                InlineQueryResultArticle(
                        id='3',
                        title=videostitles[2],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[2]
                        ),
                        thumb_url=thumbnailslinks[2]    
                ),
                InlineQueryResultArticle(
                        id='4',
                        title=videostitles[3],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[3]
                        ),
                        thumb_url=thumbnailslinks[3]    
                ),
                InlineQueryResultArticle(
                        id='5',
                        title=videostitles[4],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[4]
                        ),
                        thumb_url=thumbnailslinks[4]    
                ),
                InlineQueryResultArticle(
                        id='6',
                        title=videostitles[5],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[5]
                        ),
                        thumb_url=thumbnailslinks[5]    
                ),
                InlineQueryResultArticle(
                        id='7',
                        title=videostitles[6],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[6]
                        ),
                        thumb_url=thumbnailslinks[6]    
                ),
                InlineQueryResultArticle(
                        id='8',
                        title=videostitles[7],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[7]
                        ),
                        thumb_url=thumbnailslinks[7]    
                ),
                InlineQueryResultArticle(
                        id='9',
                        title=videostitles[8],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[8]
                        ),
                        thumb_url=thumbnailslinks[8]    
                ),
                InlineQueryResultArticle(
                        id='10',
                        title=videostitles[9],
                        input_message_content=InputTextMessageContent(
                            message_text=videoslinks[9]
                        ),
                        thumb_url=thumbnailslinks[9]
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
