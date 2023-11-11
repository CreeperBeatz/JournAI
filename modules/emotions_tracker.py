import streamlit as st
from typing import Tuple, Optional

base_emotions = ["Bad", "Surprised", "Fearful", "Angry", "Disgusted", "Sad", "Happy"]

# Example secondary emotions (you can expand or modify these)
secondary_emotions = {
    "Bad": ["Stressed", "Tense", "Bored"],
    "Surprised": ["Amazed", "Startled", "Confused"],
    "Fearful": ["Anxious", "Scared", "Worried"],
    "Angry": ["Irritated", "Furious", "Annoyed"],
    "Disgusted": ["Revolted", "Repelled", "Offended"],
    "Sad": ["Gloomy", "Disheartened", "Mournful"],
    "Happy": ["Joyful", "Content", "Pleased"]
}

# Example tertiary emotions (you can expand or modify these)
tertiary_emotions = {
    "Stressed": ["Overwhelmed", "Pressured"],
    "Tense": ["Nervous", "On edge"],
    "Bored": ["Indifferent", "Apathetic"],
    # ... continue for other secondary emotions
}


def emotion_picker(label: str = "") -> Tuple[Optional[str], Optional[str], Optional[str]]:
    main_emotion = st.selectbox(
        f"{label} - Main Emotion",
        [''] + base_emotions,
        index=0,
        placeholder="Choose an emotion",
    )

    secondary_emotion = None
    tertiary_emotion = None

    if main_emotion:
        secondary_emotion_options = [''] + secondary_emotions.get(main_emotion, [])
        secondary_emotion = st.selectbox(
            f"Can you further define your emotion? (Optional)",
            secondary_emotion_options,
            index=0,
            placeholder="Choose a secondary emotion",
        )

    if secondary_emotion:
        tertiary_emotion_options = [''] + tertiary_emotions.get(secondary_emotion, [])
        tertiary_emotion = st.selectbox(
            f"Is your emotion a variation of one of these (Optional)",
            tertiary_emotion_options,
            index=0,
            placeholder="Choose a tertiary emotion"
        )

    return main_emotion, secondary_emotion, tertiary_emotion
