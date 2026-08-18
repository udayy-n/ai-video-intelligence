import os
import hashlib
from urllib.parse import urlparse, parse_qs

CACHE_DIR = "cache"

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)


def get_video_id(url):

    if "/live/" in url:
        return url.split("/live/")[1].split("?")[0]

    if "youtu.be/" in url:
        return url.split("/")[-1].split("?")[0]

    parsed = urlparse(url)

    return parse_qs(
        parsed.query
    ).get(
        "v",
        ["unknown"]
    )[0]


def get_cache_key(url):

    video_id = get_video_id(url)

    return hashlib.md5(
        video_id.encode()
    ).hexdigest()


def cache_exists(url):

    cache_file = os.path.join(
        CACHE_DIR,
        f"{get_cache_key(url)}.txt"
    )

    return os.path.exists(cache_file)


def save_cache(
    url,
    transcript
):

    cache_file = os.path.join(
        CACHE_DIR,
        f"{get_cache_key(url)}.txt"
    )

    with open(
        cache_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(transcript)


def load_cache(url):

    cache_file = os.path.join(
        CACHE_DIR,
        f"{get_cache_key(url)}.txt"
    )

    with open(
        cache_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()