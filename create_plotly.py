import plotly.express as px
import pandas as pd
from db_session import engine
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/create_plotly/")
def create_plotly():
    df = pd.read_sql("""
        SELECT  category_id, AVG(view_count) AS avg_views
        FROM videos
        GROUP BY category_id
        ORDER BY avg_views DESC;
    """, engine)

    fig = px.bar(df, x='category_id', y='avg_views', title="Average Views per CategoryId")
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"avg_views_per_category_id_{date_str}.png"
    if not os.path.exists(file_name):
        fig.write_image(file_name)
    return FileResponse(path=file_name, media_type='image/png', filename=file_name)
