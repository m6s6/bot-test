

import requests
import telebot
import config


from keyboa import keyboa_maker
from bs4 import BeautifulSoup
import dtworker

bot = telebot.TeleBot(config.token)

url = config.URL
mbox = requests.get(url).text
soup = BeautifulSoup(mbox, 'html')
names = []
urls = {}
try:
    for i in range(len(soup.find('ul').find_all('li'))):
        if 0 < i < 13:
            names.append(soup.find('ul').find_all('li')[i].find('a').text)
            urls[soup.find('ul').find_all('li')[i].find('a').text] = str(
                url + soup.find('ul').find_all('li')[i].find('a').get('href'))
except:
    pass



@bot.message_handler (commands=["info"])
def cmd_info(message):
    bot.send_message(message.chat.id, "Асисстент бот формирует новостную подборку на 'Сегодня' \n сообщения кроме "
                                      "команд он не принимает\nДля выбора свежих новостей набери или нажми /news")


@bot.message_handler(commands=["start"])
def cmd_start(message):
    # print(dtworker.get_name(message.from_user.id))
    if dtworker.get_name(message.from_user.id)[0] != None:
        bot.send_message(message.chat.id, f"Добрый день, {dtworker.get_name(message.from_user.id)[1]}!:) "
                                          f"\n Рады снова тебя видеть, \nпоследний раз ты смотрел новости в категории "
                                          f"{dtworker.get_name(message.from_user.id)[2]}!\nДля выбора свежих новостей "
                                          f"набери или нажми /news \nДля более подробной информации по данному продукту"
                                          f"нажми /info")
    else:
        dtworker.insert_user(message.from_user.id, message.from_user.first_name)
        bot.send_message(message.chat.id, f"Добрый день, {message.from_user.first_name}!:) \nМы рады, что ты "
                                          f"присоединился к новостному чат Боту!\nДля выбора свежих новостей набери "
                                          f"или нажми /news \nДля более подробной информации по данному продукту "
                                          f"нажми /info")
    # print(message)



@bot.message_handler(commands=["news"])
def info(message):
    kb_news = keyboa_maker(items=names, copy_text_to_callback=True)
    bot.send_message(message.chat.id, reply_markup=kb_news, text="Пожалуйста выберите новостную категорию:")


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data in names:
        bot.send_message(c.message.chat.id, c.data)
        print(c.message)
        print(c.message.from_user.id, c.data)
        dtworker.update_table(c.message.chat.id, c.data)
        try:
            mbox_news = requests.get(urls[c.data]).text
            soup_news = BeautifulSoup(mbox_news, 'html')
            n = soup_news.find_all('section')[1].find_all('div', class_='item')
            bot.send_photo(c.message.chat.id, soup_news.find_all('img', class_='g-picture')[1].get('src'))
            for new_item in range(len(n)):
                items = n[new_item - 1].find("span", class_="item__date").text

                if items[-7:].lower() == 'сегодня':
                    bot.send_message(c.message.chat.id, str(n[new_item - 1].text)[:15] + ' '
                                     + str(n[new_item - 1].text)[15:] +
                                     "\n" + str(url + n[new_item - 1].find('h3').find('a').get('href')))


        except:
            pass

        bot.send_message(c.message.chat.id, f'Это все новости на сегодня в разделе {c.data} \nЧтобы выбрать другую категорию нажмите /news')


@bot.message_handler(func=lambda message: message.text.strip().lower() not in ('/info', '/start', '/news'))
def cmd_msg(message):
    bot.send_message(message.chat.id, "Асисстент бот не знает Ваш язык \nи сообщения кроме команд он не принимает \nДля выбора свежих новостей набери или нажми /news \nДля более подробной информации по данному продукту нажми /info")


if __name__ == '__main__':
    bot.infinity_polling()
