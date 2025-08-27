import asyncio
import aiohttp

import os
from dotenv import load_dotenv


load_dotenv()

API_URL = 'https://api.coingecko.com/api/v3/coins/list'
API_KEY = str(os.getenv("COINGECKO_API_KEY"))


async def fetch_all_cryptos():
    headers = {
        'x-cg-pro-api-key' : API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f'Error fetching data: {response.status} - {text}')
            return await response.json()
        

async def main():
    data = await fetch_all_cryptos()
    print(len(data))
    
    
if __name__ == '__main__':
    asyncio.run(main())