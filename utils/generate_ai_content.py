# utils.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_content(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        content = response.choices[0].text.strip()
        return content
    except Exception as e:
        # Log the error
        print(f"Error generating AI content: {e}")
        return None
