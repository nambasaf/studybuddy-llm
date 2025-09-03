import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Make sure your API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables!")

openai.api_key = api_key

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
    )
    print("✅ Success! Response from OpenAI:")
    print(response.choices[0].message.content)

except openai.error.OpenAIError as e:
    print("❌ OpenAI API error:")
    print(e)
