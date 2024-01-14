from typing import Union
from random import randint

import requests

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    media_endpoint_url: str
    media_default_category: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
app = FastAPI()

@app.get("/")
def read_root():

    api_request = requests.get(settings.media_endpoint_url + settings.media_default_category + '?ls', timeout=1)
    media = api_request.json()

    num_media = len(media['files'])
    num_rand = randint(0,num_media-1)

    rand_media_ext = media['files'][num_rand]['ext']

    if rand_media_ext in ['jpg','png','webp','gif']:
        rand_media_type = 'image'
    else:
        rand_media_type = 'video'

    rand_media_url = settings.media_endpoint_url + settings.media_default_category + '/' + media['files'][num_rand]['href']

    # return render_template('home.html', categories=categories['dirs'],media_type=rand_media_type,media_url=rand_media_url)
    return {"media_type": rand_media_type, "media_url": rand_media_url}


@app.get("/{category}")
def read_category(category: str):

    api_request = requests.get(settings.media_endpoint_url + category + '?ls', timeout=1)
    media = api_request.json()

    num_media = len(media['files'])
    num_rand = randint(0,num_media-1)

    rand_media_ext = media['files'][num_rand]['ext']

    if rand_media_ext in ['jpg','png','webp','gif']:
        rand_media_type = 'image'
    else:
        rand_media_type = 'video'

    rand_media_url = settings.media_endpoint_url + category + '/' + media['files'][num_rand]['href']

    return {"media_type": rand_media_type, "media_url": rand_media_url}

@app.get("/categories")
def read_categories():

    category_request = api_request = requests.get(settings.media_endpoint_url + '?ls', timeout=1)
    categories = category_request.json()

    return { "categories": categories }
