from fastapi import FastAPI
from routes import router


app = FastAPI(title='Crypto Analisys App')

app.include_router(router)