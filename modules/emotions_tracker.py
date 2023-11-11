import streamlit as st
from typing import Tuple, Optional

emotions_structure = {
    "Happy": {
        "Playful": ["Aroused", "Cheeky"],
        "Content": ["Free", "Joyful"],
        "Interested": ["Curious", "Inquisitive"],
        "Proud": ["Successful", "Confident"],
        "Accepted": ["Respected", "Valued"],
        "Powerful": ["Courageous", "Creative"],
        "Peaceful": ["Loving", "Thankful"],
        "Trusting": ["Intimate", "Sensitive"]
    },
    "Sad": {
        "Lonely": ["Isolated", "Abandoned"],
        "Vulnerable": ["Victimized", "Fragile"],
        "Despair": ["Grief", "Powerless"],
        "Guilty": ["Ashamed", "Remorseful"],
        "Depressed": ["Inferior", "Empty"],
        "Hurt": ["Embarrassed", "Disappointed"]
    },
    "Disgusted": {
        "Disapproving": ["Judgmental", "Embarrassed"],
        "Disappointed": ["Appalled", "Revolted"],
        "Awful": ["Nauseated", "Detestable"],
        "Repelled": ["Horrified", "Hesitant"]
    },
    "Angry": {
        "Let Down": ["Betrayed", "Resentful"],
        "Humiliated": ["Disrespected", "Ridiculed"],
        "Bitter": ["Indignant", "Violated"],
        "Mad": ["Furious", "Jealous"],
        "Aggressive": ["Provoked", "Hostile"],
        "Frustrated": ["Infuriated", "Annoyed"],
        "Distant": ["Withdrawn", "Numb"],
        "Critical": ["Skeptical", "Dismissive"]
    },
    "Fearful": {
        "Scared": ["Helpless", "Frightened"],
        "Anxious": ["Overwhelmed", "Worried"],
        "Insecure": ["Inadequate", "Inferior"],
        "Weak": ["Worthless", "Insignificant"],
        "Rejected": ["Excluded", "Persecuted"],
        "Threatened": ["Nervous", "Exposed"]
    },
    "Bad": {
        "Bored": ["Indifferent", "Apathetic"],
        "Busy": ["Pressured", "Rushed"],
        "Stressed": ["Overwhelmed", "Out of control"],
        "Tired": ["Sleepy", "Unfocused"]
    },
    "Surprised": {
        "Startled": ["Shocked", "Dismayed"],
        "Confused": ["Disillusioned", "Perplexed"],
        "Amazed": ["Astonished", "Awe"],
        "Excited": ["Eager", "Energetic"]
    }
}


def emotion_picker(label: str = "", key=None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    base_emotion = st.selectbox(
        f"{label}",
        [''] + list(emotions_structure.keys()),
        index=None,
        placeholder="Choose an emotion",
        key=key + "1",
    )

    secondary_emotion = None
    tertiary_emotion = None

    if base_emotion:
        secondary_emotions = list(emotions_structure[base_emotion].keys())
        secondary_emotion = st.selectbox(
            f"Can you further define your emotion? (Optional)",
            [''] + secondary_emotions,
            index=None,
            placeholder="Choose a secondary emotion",
            key=key + "2",
        )

    if secondary_emotion:
        tertiary_emotions = emotions_structure[base_emotion][secondary_emotion]
        tertiary_emotion = st.selectbox(
            f"Is your emotion a variation of one of these (Optional)",
            [''] + tertiary_emotions,
            index=None,
            placeholder="Choose a tertiary emotion",
            key=key + "3",
        )

    return base_emotion, secondary_emotion, tertiary_emotion
