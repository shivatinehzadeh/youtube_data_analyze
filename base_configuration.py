from fastapi import FastAPI
from youtube_data import create_csv_youtube_trend
import data_store, create_plotly

app = FastAPI()

   
create_csv_youtube_trend()

app.include_router(data_store.router)  
app.include_router(create_plotly.router)  
