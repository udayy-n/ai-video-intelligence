import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv(
    "GEMINI_API_KEY"
)

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_report(
    transcript
):

    prompt = f"""
You are NoteGPT.

Analyze the transcript and return ONLY markdown.

# Executive Summary

# Main Topics

# Topic Breakdown

For each topic provide:

## Topic Name

### Discussion

### Important Points

### Outcome

# Key Insights

Provide 5 key insights.

# Action Items

Provide action items.

# Frequently Asked Questions

Generate useful questions and answers.

# Conclusion

Transcript:

{transcript[:20000]}
"""

    response = model.generate_content(
        prompt
    )

    return response.text