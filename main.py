import os
import aiohttp

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from dotenv import load_dotenv


load_dotenv()


class WebAppRequest(BaseModel):
    minPrice: str
    maxPrice: str
    minDays: int
    maxDays: int
    name: str 
    email: str 
    telegram: str
    taskOfGame: str
    shortDescription: str 
    gameAudience: str
    graphicsType: str 
    gameStyle: str 
    isOnline: str 
    otherServices: str 
    hasDevelopments: str 
    priorities: str
    importantThings: str
    otherThings: str


app = FastAPI()

origins = [
    "https://lwich.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


async def send_message(text):
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + text
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            ...


@app.post('/send-message')
async def send_message_endpoint(webapp: WebAppRequest):
    data = webapp.model_dump()

    text = '''
    Пришёл новый заказ%0A
    %0A
    Цена:%0A
    * От: {} ₽%0A
    * До: {} ₽%0A
    %0A
    Сроки:%0A
    * От: {} дней%0A
    * До: {} дней%0A
    %0A
    Контактные данные:%0A
    * Имя: {}%0A
    * Телеграм: @{}%0A
    * Почта: {}%0A
    %0A
    Информация:%0A
    * Задача игры: {}%0A
    * Описание: {}%0A
    * Аудитория: {}%0A
    * Графика: {}%0A
    * Стилистика: {}%0A
    * Планируется ли онлайн-составляющая*: {}%0A
    * Доп. сервисы: {}%0A
    * Наработки: {}%0A
    * Приоритеты: {}%0A
    * Критически важные и приоритетные вещи: {}%0A
    * Другое: {}
    '''.format(data['minPrice'], data['maxPrice'], data['minDays'],
               data['maxDays'], data['name'], data['telegram'], 
               data['email'], data['taskOfGame'], data['shortDescription'],
               data['gameAudience'], data['graphicsType'], data['gameStyle'],
               data['isOnline'], data['otherServices'], data['hasDevelopments'],
               data['priorities'], data['importantThings'], data['otherThings']
               )
    
    await send_message(text)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')