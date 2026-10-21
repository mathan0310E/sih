# Install once:  pip install google-genai
# Set the key:  export GOOGLE_API_KEY="your-key"
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
MODEL = "gemini-2.0-flash"
PROMPT = ("Write a 120-word introduction to generative artificial "
          "intelligence for a first-year engineering student.")

for temp in (0.0, 0.7, 1.0):
    resp = client.models.generate_content(
        model=MODEL,
        contents=PROMPT,
        config=types.GenerateContentConfig(temperature=temp),
    )
    print("=" * 70)
    print(f"temperature={temp}")
    print(resp.text.strip()[:400])
