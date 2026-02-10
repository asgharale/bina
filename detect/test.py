from google import genai
from PIL import Image
import os

# Use your real key or from settings
api_key = "AIzaSyBaLoES2J6QYpYVggqIhu4ZPwGKtlTT7OQ"  # or os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Dummy small image or use a real one
img = Image.new('RGB', (100, 100), color = 'red')

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Describe this red square image in Persian.", img],
)

print(response.text)