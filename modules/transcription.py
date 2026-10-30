
from faster_whisper import WhisperModel

# Load the multilingual model once
model = None

LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil",
    "te": "Telugu",
    "hi": "Hindi",
    "ml": "Malayalam",
    "kn": "Kannada"
}


def transcribe_audio(audio_path, selected_language=None):
    global model

    if model is None:
        model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    # Automatically detect the spoken language unless specified
    language_code = selected_language if selected_language else None

    segments, info = model.transcribe(
        audio_path,
        language=language_code,
        task="transcribe",
        beam_size=5,
        vad_filter=True
    )

    # Collect the recognized speech in its original language
    transcript = " ".join(
        segment.text.strip() for segment in segments
    ).strip()

    detected_code = info.language
    detected_language = LANGUAGE_NAMES.get(
        detected_code,
        detected_code or "Unknown"
    )

    return transcript, detected_language

