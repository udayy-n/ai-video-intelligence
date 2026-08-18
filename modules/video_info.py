import yt_dlp


def get_video_info(url):

    ydl_opts = {
        "quiet": True,
        "extract_flat": False
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    return {
        "title": info.get(
            "title"
        ),

        "channel": info.get(
            "uploader"
        ),

        "duration": info.get(
            "duration"
        ),

        "views": info.get(
            "view_count"
        ),

        "thumbnail": info.get(
            "thumbnail"
        )
    }