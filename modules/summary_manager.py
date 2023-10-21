import openai  # Assuming you're using the OpenAI Python package
from modules.config_manager import OPENAI_API_KEY


def get_weekly_summary(question, answers):
    # Combine all answers into a single string
    text_to_summarize = "\n".join(answers)

    # API call to GPT-3 for summarization (replace with actual API call)
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following journal entries:\n{text_to_summarize}\n"
               f"Made for the following question: f{question}",
        max_tokens=500
    )
    summary = response.choices[0].text.strip()

    return summary


def get_monthly_summary(weekly_summaries):
    # Combine all answers into a single string
    text_to_summarize = "\n".join(weekly_summaries)

    # API call to GPT-3 for summarization (replace with actual API call)
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following journal entries:\n{text_to_summarize}",
        max_tokens=500
    )
    summary = response.choices[0].text.strip()

    return summary


def get_yearly_summary(monthly_summaries):
    # Combine all answers into a single string
    text_to_summarize = "\n".join(monthly_summaries)

    # API call to GPT-3 for summarization (replace with actual API call)
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following journal entries:\n{text_to_summarize}",
        max_tokens=500
    )
    summary = response.choices[0].text.strip()

    return summary
