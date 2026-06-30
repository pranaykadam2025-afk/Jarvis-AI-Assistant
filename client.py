from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant."
    },
    contents="What is coding?"
)

print(response.text)