import whisper
import os

_model = None


def load_model():

    global _model

    if _model is None:

        _model = whisper.load_model(
            "base"
        )

    return _model


def transcribe_audio(audio_path):

    if not os.path.exists(audio_path):

        raise Exception(
            f"Audio file not found: {audio_path}"
        )

    if os.path.getsize(audio_path) == 0:

        raise Exception(
            f"Audio file is empty: {audio_path}"
        )

    model = load_model()

    result = model.transcribe(
        audio_path,
        fp16=False
    )

    return result["text"]