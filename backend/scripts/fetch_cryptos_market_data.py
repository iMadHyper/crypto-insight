import asyncio
import aiohttp
from db import AsyncSessionLocal
from models import Crypto, Price
from decimal import Decimal
from datetime import datetime

import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = str(os.getenv("COINGECKO_API_KEY"))
VS_CURRENCY = 'usd'


async def fetch_cryptos_market_data():
    '''
    Returns cryptos market data from CoinGecko
    '''
    API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency' : VS_CURRENCY
    }
    headers = {
        'x-cg-pro-api-key' : API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f'Error fetching data: {response.status} - {text}')
            return await response.json()

async def save_to_db(data):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            count = 0
            for item in data:
                crypto = await session.get(Crypto, item['id'])
                if not crypto:
                    crypto = Crypto(
                        id=item['id'],
                        symbol=item['symbol'],
                        name=item['name'],
                        image=item['image'],
                        market_cap_rank=int(item['market_cap_rank']),
                        genesis_date=None,
                        hashing_algorithm=None,
                        max_supply=Decimal(item['max_supply']) if item.get('max_supply') else None
                    )
                    session.add(crypto)
                    
                price = Price(
                    crypto_id=item['id'],
                    date=datetime.now(),
                    price=Decimal(item['current_price']),
                    market_cap=Decimal(item['market_cap']) if item.get('market_cap') else None,
                    price_change_24h=Decimal(item['price_change_24h']),
                    price_change_percentage_24h=Decimal(item['price_change_percentage_24h']),
                    market_cap_change_24h=Decimal(item['market_cap_change_24h']),
                    market_cap_change_percentage_24h=Decimal(item['market_cap_change_percentage_24h']),
                    ath=Decimal(item['ath']),
                    ath_date=datetime.fromisoformat(item['ath_date'].replace("Z", "+00:00")),
                    atl=Decimal(item['atl']),
                    atl_date=datetime.fromisoformat(item['atl_date'].replace("Z", "+00:00")),
                    circulating_supply=Decimal(item['circulating_supply']) if item.get('circulating_supply') else None,
                    total_supply=Decimal(item['total_supply']) if item.get('total_supply') else None
                )
                session.add(price)
                
                count += 1
                if count == 50:
                    break
                
                
async def main():
    data = await fetch_cryptos_market_data()
    await save_to_db(data)
    
    
if __name__ == '__main__':
    asyncio.run(main())