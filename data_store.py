import pandas as pd
from db_models import Video
from db_session import get_db
from fastapi import APIRouter

router = APIRouter()

db=next(get_db())
@router.post("/add_data/")
def add_data():
    db.query(Video).delete()
    db.commit()
    df = pd.read_csv("youtube_trending_us.csv")
    for _, row in df.iterrows():
        crate_video_data_for_sql = Video(video_id = row["video_id"],
            title = row["title"],
            channel_title = row["channel_title"],
            category_id = row["category_id"],
            view_count = row["view_count"],
            like_count = row["like_count"],
            comment_count = row["comment_count"],
            title_polarity = row["title_polarity"],
            title_subjectivity = row["title_subjectivity"]
            )
        db.add(crate_video_data_for_sql)
    db.commit()
                
    return {"message": "CSV added in table successfully"}
