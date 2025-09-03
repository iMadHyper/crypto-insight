import asyncio
import aiohttp
from sqlalchemy.future import select
from db import AsyncSessionLocal
from models import Crypto
from decimal import Decimal
from datetime import datetime

import os
from dotenv import load_dotenv


load_dotenv()

    
async def fetch_crypto_data(id: str):
    '''
    Return crypto data
    '''
    API_URL = f'https://api.coingecko.com/api/v3/coins/{id}'
    headers = {
        'x-cg-pro-api-key' : os.getenv("COINGECKO_API_KEY")
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f'Error fetching data: {response.status} - {text}')
            return await response.json()

async def update_cryptos():
    '''
    Updates db crypto info
    '''
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Crypto)
            .offset(27) # First 27 cryptos doesn't have a devo API request
            .limit(2)
        )
        cryptos = result.scalars().all()
        
        for index, crypto in enumerate(cryptos):
            try:
                print(index+1)
                print(crypto.id)
                crypto_info = await fetch_crypto_data(str(crypto.id))
                crypto.genesis_date = datetime.fromisoformat(crypto_info['genesis_date']).date() if crypto_info.get('genesis_date') else None
                crypto.hashing_algorithm = crypto_info.get('hashing_algorithm', None)
                crypto.max_supply = Decimal(crypto_info['max_supply']) if crypto_info.get('max_supply') else None
                crypto.market_cap_rank = int(crypto_info.get('market_cap_rank'))
                await session.commit()
            except Exception as ex:
                print(ex)
                


async def main():
    await update_cryptos()
    
    
if __name__ == '__main__':
    asyncio.run(main())