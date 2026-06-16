import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def _call_openai(system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gbt-40-mini",
            message=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choises[0].message.content.strip()
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"
def generate_content(topic: str) -> str:
    system = "You are a professional digital marketing expert. Your job is to write engaging and short marketing content. Always respond in the exact same language used in the user prompt. Format: Headline + 3 Key Points + CTA."
    user = f"Write marketing content about: {topic}"
    return _call_openai(system, user)
def analyze_data(data_description: str) -> str:
    system = "You are an expert data analyst. Your job is to analyze data and provide actionable insights. Always respond in the exact same language used in the user prompt. Format: Summary + 3 Insights + Recommendation."
    user = f"Analyze this data and give me insights: {data_description}"
    return _call_openai(system, user)
def generate_leads(industry: str, target: str) -> str:
    system = "You are a lead generation expert. Your job is to provide a pratical strategy to find leads. Always respond in the exact same language used in user prompt. Format: Communication Channel + Suggested Message + Immediate Steps."
    user = f"Industry: {industry}/ntarget Audience: {target}/nGive me a leads strategy."
    return _call_openai(system, user)