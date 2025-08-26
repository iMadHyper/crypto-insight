from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Numeric, Date
from sqlalchemy.orm import relationship
from db import Base


class Crypto(Base):
    __tablename__ = 'cryptos'
    
    id = Column(String, primary_key=True, index=True)
    symbol =  Column(String)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    market_cap_rank = Column(Integer) # capitalization rank
    genesis_date = Column(Date)
    hashing_algorithm = Column(String)
    max_supply = Column(Numeric(20, 2))
    
    prices = relationship("Price", back_populates="crypto")
    
    
class Price(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True, index=True)
    crypto_id = Column(String, ForeignKey('cryptos.id'))
    date = Column(TIMESTAMP(timezone=True), nullable=False)
    price = Column(Numeric(18, 8), nullable=False)
    market_cap = Column(Numeric(20, 2)) # capitalization
    market_cap_change_24h = Column(Numeric(20, 2))
    market_cap_change_percentage_24h = Column(Numeric(5, 2))
    price_change_24h = Column(Numeric(20, 2))
    price_change_percentage_24h = Column(Numeric(5, 2))
    ath = Column(Numeric(18, 8)) # all time high
    ath_date = Column(TIMESTAMP(timezone=True))
    atl = Column(Numeric(18, 8)) # all time low
    atl_date = Column(TIMESTAMP(timezone=True))
    circulating_supply = Column(Numeric(20, 2))
    total_supply = Column(Numeric(20, 2))
    
    crypto = relationship("Crypto", back_populates="prices")