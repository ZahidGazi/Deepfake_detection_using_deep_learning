from groq import Groq
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API keys from environment variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def analyze_news_with_llm(news):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an assistant skilled in analyzing news for credibility."},
            {"role": "user", "content": f"Analyze the following news headline and tell me if it's likely real or fake, and why:\n\n'{news}'"}
        ]
    )
    return response.choices[0].message.content.strip()

def fetch_from_google_news(query):
    URL = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return None

def verify_sources(news):
    sources = fetch_from_google_news(news)
    if not sources:
        return "No sources found."

    verified_sources = []
    for source in sources[:5]:
        verified_sources.append(f"- {source['title']} ({source['source']['name']})")
    return "\n".join(verified_sources)

def detect_fake_news(news):
    llm_analysis = analyze_news_with_llm(news)
    verification_results = verify_sources(news)
    return f"LLM Analysis:\n{llm_analysis}\n\nVerification Sources:\n{verification_results}"
