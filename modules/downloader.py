import yt_dlp
import os
import shutil

def download_audio(youtube_url):

    audio_folder = "audio"

    os.makedirs(
        audio_folder,
        exist_ok=True
    )

    # delete old audio files
    for file in os.listdir(audio_folder):

        file_path = os.path.join(
            audio_folder,
            file
        )

        try:
            os.remove(file_path)
        except:
            pass

    output_path = os.path.join(
        audio_folder,
        "audio.%(ext)s"
    )

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    "quiet": True,
    "noplaylist": True,
    "extractaudio": True,
    "geo_bypass": True,
    "nocheckcertificate": True
}

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        ydl.download(
            [youtube_url]
        )

    for file in os.listdir(audio_folder):

        if file.endswith(
            (
                ".webm",
                ".m4a",
                ".mp3"
            )
        ):

            return os.path.join(
                audio_folder,
                file
            )

    raise Exception(
        "Audio download failed"
    )