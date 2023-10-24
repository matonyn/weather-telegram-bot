import telebot
import requests
from bs4 import BeautifulSoup
from typing import Final
import time

def parser():
    res = 'Погода сейчас: '
    url = "https://www.meteoprog.com/ru/weather/Astana/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_data = soup.find("div", class_="today-temperature")
        res+=weather_data.text.strip()
        res += '\n'
        feel = soup.find("span", class_="feels-like")
        res+=feel.text.strip()
        res += '\n'
        cur = soup.find_all("td", class_="atmosphere-spec")
        for c in cur:
            t = c.text.strip()
            if " %" in t:
                res+="Вероятность дождя: "
                res+=t
                res+="\n"
                if "0" not in t:
                    res+="\nНе забудьте зонт!\n\n"
                break

        for c in cur:
            t = c.text.strip()
            if " м/с" in t:
                res+="Ветер: "
                res+=t
                res+="\n"
                if "0" not in t:
                    res+="\nНе забудьте шапку!\n"
                break
    
        return res
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")



TOKEN: Final = '6840724695:AAGhM5geBBwICAiYa4FXQvbx5yc4RJYgh-c'
BOT_USERNAME = "@my_astana_weather_bot"

chat_id = "471169971"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш погодный бот Астаны!\nАстана славится своей непредсказуемой погодой, поэтому я сообщу вам, как вам следует одеваться в этот день!\nВведите /weather, чтобы получить актуальную информацию о погоде")

@bot.message_handler(commands=['weather'])
def send_weather(message):
        t = parser()
        if "Прохладно" in t:
            t+="Оденьтесь потеплее!"
        bot.send_message(message.chat.id, t)

bot.infinity_polling()

