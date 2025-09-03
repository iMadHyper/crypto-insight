from celery import Celery
import asyncio
from scripts.fetch_cryptos_market_data import fetch_cryptos_market_data, save_to_db


app = Celery(
    'tasks', 
    broker='redis://redis:6379', 
    backend='redis://redis:6379'
)

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'fetch_market_data_every_hour': {
        'task': 'tasks.fetch_and_save_market_data',
        'schedule': 30,
    }
}


@app.task
def fetch_and_save_market_data():
    asyncio.run(marker_data_task())


async def marker_data_task():
    data = await fetch_cryptos_market_data()
    await save_to_db(data)