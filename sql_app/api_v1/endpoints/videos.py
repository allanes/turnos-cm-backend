import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from sql_app.servidor_socketio import sio

video_lists = {
    1: [
        {"title": "a-ha - Take On Me", "url": "https://www.youtube.com/watch?v=3tmd-ClpJxA"},  # a-ha - Take On Me
        {"title": "Zach Nugent's Dead Set - Lebanon, NH - 5.19.2023 (Set 2)", "url": "https://www.youtube.com/watch?v=oSHB4lPl_ew&ab_channel=CotterEllis"},  # Queen - Bohemian Rhapsody
        {"title": "Queen - Bohemian Rhapsody", "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},  # Queen - Bohemian Rhapsody
        {"title": "Paris Cafe ambience", "url": "https://www.youtube.com/watch?v=hUad0qtrsNI"},
        {"title": "Melodic Sunrise", "url": "https://www.youtube.com/watch?v=C3Hpr9oryCY"},
    ],
    2: [
        {"title": "a-ha - Take On Me", "url": "https://www.youtube.com/watch?v=3tmd-ClpJxA"},  # a-ha - Take On Me
        {"title": "Queen -Bohemian Rhapsody", "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},  # Queen - Bohemian Rhapsody
        {"title": "Zach Nugent's Dead Set - Lebanon, NH - 5.19.2023 (Set 2)", "url": "https://www.youtube.com/watch?v=oSHB4lPl_ew&ab_channel=CotterEllis"},  # Queen - Bohemian Rhapsody
        {"title": "Paris Cafe ambience", "url": "https://www.youtube.com/watch?v=hUad0qtrsNI"},
        {"title": "Melodic Sunrise", "url": "https://www.youtube.com/watch?v=C3Hpr9oryCY"},
    ],
}

index_actual = {
    1: 0,
    2: 0,
}

router = APIRouter()

@router.get("/lista-videos-youtube/{sala}")
def read_videos_youtube(sala: int):
    if sala not in video_lists:
        raise HTTPException(status_code=404, detail="Sala not found")
    return video_lists[sala]

@router.get("/carpeta-videos")
def read_videos_carpeta():
    folder_url = "https://drive.google.com/drive/folders/1Nh5g6dpXgtAyIOsbb-IQanFo8qgJoTIY?usp=sharing"
    return folder_url

@router.get("/lista-videos-locales")
def read_videos_locales():
    video_files = os.listdir('videos')
    video_files = ["http://localhost:8000/videos/"+file for file in video_files]
    return video_files

@router.get("/video/{video_id}")
async def get_video(video_id: str):
    video_directory = os.getcwd() + "/videos/"
    video_files = os.listdir(video_directory)
    if video_id not in video_files:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_directory + video_id)

@router.get("/lista-videos-youtube/{sala}/current-state")
async def get_current_video(sala: int):
    if sala not in index_actual:
        raise HTTPException(status_code=404, detail="Sala not found")
    return {"url": video_lists[sala][index_actual[sala]]["url"]}
