from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = os.getenv("API_ADDRESS")
GREETING = "Приветствую! Здесь ты сможешь просто и быстро оценить различные товары и услуги! Чтобы помочь компаниям в продвижении их продукции, проходя опросы, пожалуйста, запусти наше мини-приложение"
NOTIFICATION_INTERVAL = 30   # интервал запросов для получения уведомлений в секундах
