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


def emotion_picker(label: str = "", key=None, emotion: str = None) -> str:
    # Find the ancestors of the passed emotion
    emotion_ancestors = find_emotion_ancestors(emotion) if emotion else []

    # Determine the indices for the base, secondary, and tertiary emotions
    base_index = 1 + list(emotions_structure.keys()).index(emotion_ancestors[0]) if emotion_ancestors else None
    secondary_index = 1 + list(emotions_structure[emotion_ancestors[0]].keys()).index(emotion_ancestors[1]) if len(emotion_ancestors) > 1 else None
    tertiary_index = 1 + emotions_structure[emotion_ancestors[0]][emotion_ancestors[1]].index(emotion_ancestors[2]) if len(emotion_ancestors) > 2 else None

    # Select base emotion
    base_emotion = st.selectbox(
        f"{label}",
        [''] + list(emotions_structure.keys()),
        index=base_index,
        placeholder="Choose an emotion",
        key=key + "1",
    )

    secondary_emotion = None
    tertiary_emotion = None

    # Select secondary emotion
    if base_emotion:
        secondary_emotions = list(emotions_structure[base_emotion].keys())
        secondary_emotion = st.selectbox(
            f"Can you further define your emotion? (Optional)",
            [''] + secondary_emotions,
            index=secondary_index,
            placeholder="Choose a secondary emotion",
            key=key + "2",
        )

    # Select tertiary emotion
    if secondary_emotion:
        tertiary_emotions = emotions_structure[base_emotion][secondary_emotion]
        tertiary_emotion = st.selectbox(
            f"Is your emotion a variation of one of these (Optional)",
            [''] + tertiary_emotions,
            index=tertiary_index,
            placeholder="Choose a tertiary emotion",
            key=key + "3",
        )

    return tertiary_emotion or secondary_emotion or base_emotion


def find_emotion_ancestors(emotion: str) -> list:
    """
    This function traverses the emotions structure

    Parameters:
    emotion (str): The emotion for which ancestors are to be found.

    Returns:
        list: A list of emotions, OR empty list if emotion not found
    """
    for base_emotion, secondary_emotions in emotions_structure.items():
        if emotion == base_emotion:
            return [emotion]
        for secondary_emotion, tertiary_emotions in secondary_emotions.items():
            if emotion in tertiary_emotions:
                return [base_emotion, secondary_emotion, emotion]
            elif emotion == secondary_emotion:
                return [base_emotion, emotion]
    return []  # Returns an empty list if the emotion is not found
