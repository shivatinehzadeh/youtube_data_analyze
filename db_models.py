from sqlalchemy import  Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from base import engine
from pydantic import BaseModel

Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String, primary_key=True, index=True)
    title = Column(String)
    channel_title = Column(String)
    published_at = Column(DateTime)
    category_id = Column(Integer)
    view_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    title_polarity = Column(Float)
    title_subjectivity = Column(Float)


class VideoSchema(BaseModel):
    video_id: str
    title: str
    channel_title: str
    published_at: str 
    category_id: int
    view_count: int
    like_count: int
    comment_count: int
    title_polarity: float
    title_subjectivity: float

    class Config:
        orm_mode = True
        
Base.metadata.create_all(bind=engine)