import requests
import pandas as pd
from textblob import TextBlob
import os 


API_KEY = os.getenv('API_KEY')
url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    'part': 'snippet,statistics',
    'chart': 'mostPopular',
    'regionCode': 'US',
    'maxResults': 25,
    'key': API_KEY
}


def analyze_sentiment(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def create_csv_youtube_trend():
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        videos = []
        for item in data.get('items', []):
            snippet = item['snippet']
            stats = item['statistics']
            video = {
                'video_id': item['id'],
                'title': snippet['title'],
                'channel_title': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'category_id': snippet['categoryId'],
                'view_count': stats.get('viewCount'),
                'like_count': stats.get('likeCount'),
                'comment_count': stats.get('commentCount')
            }
            videos.append(video)

        df = pd.DataFrame(videos)
        df['title_polarity'], df['title_subjectivity'] = zip(*df['title'].apply(analyze_sentiment))
        df.drop_duplicates(subset='video_id', keep='first', inplace=True)
        for data in df:
            if data == 'view_count' or data == 'like_count' or data == 'comment_count':
                df[data] = pd.to_numeric( df[data], errors='coerce').fillna(0).astype(int)
            if data in ['channel_title','title']:
                df[data] =  df[data].str.strip().str.lower()
            if data == 'published_at':
                df[data] = pd.to_datetime(data, errors='coerce')
        df.dropna(axis=1, how='all', inplace=True)
        df.to_csv("youtube_trending_us.csv", index=False)
        print("Trending videos saved to 'youtube_trending_us.csv'")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


