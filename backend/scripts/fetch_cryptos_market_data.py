import asyncio
import aiohttp
from db import AsyncSessionLocal
from sqlalchemy.future import select
from models import Crypto, Price
from decimal import Decimal
from datetime import datetime, timezone

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
        result = await session.execute(select(Crypto))
        cryptos_ids = [c.id for c in result.scalars().all()]
        
        count = 0
        for item in data:
            if item['id'] not in cryptos_ids:
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
                date=datetime.now(timezone.utc),
                price=Decimal(item['current_price']),
                market_cap=Decimal(item['market_cap']) if item.get('market_cap') else None,
                price_change_24h=Decimal(item['price_change_24h']),
                price_change_percentage_24h=Decimal(item['price_change_percentage_24h']),
                market_cap_change_24h=Decimal(item['market_cap_change_24h']),
                market_cap_change_percentage_24h=Decimal(item['market_cap_change_percentage_24h']),
                total_volume=Decimal(item['total_volume']),
                ath=Decimal(item['ath']),
                ath_date=datetime.fromisoformat(item['ath_date'].replace("Z", "+00:00")),
                atl=Decimal(item['atl']),
                atl_date=datetime.fromisoformat(item['atl_date'].replace("Z", "+00:00")),
                circulating_supply=Decimal(item['circulating_supply']) if item.get('circulating_supply') else None,
                total_supply=Decimal(item['total_supply']) if item.get('total_supply') else None
            )
            session.add(price)
                
            count += 1
            print(f'{count}: {price.crypto_id}')
        
        await session.commit()
                
                
async def main():
    data = await fetch_cryptos_market_data()
    await save_to_db(data)
    
    
if __name__ == '__main__':
    asyncio.run(main())