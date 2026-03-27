import os
from openai import OpenAI

# 🔑 API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 Simple memory (optional improvement)
conversation_memory = []


# 🔹 Intent detection (improved)
def detect_intent(query: str) -> str:
    query = query.lower()

    intent_keywords = {
        "crop_issue": [
            "leaf", "yellow", "disease", "spots", "fungus",
            "pest", "dry", "wilting", "rot", "infection"
        ],
        "weather": [
            "rain", "weather", "temperature", "forecast",
            "climate", "heat", "humidity"
        ],
        "farming_advice": [
            "fertilizer", "growth", "yield", "soil",
            "water", "irrigation", "nutrients"
        ],
        "market": [
            "price", "market", "sell", "rate", "demand"
        ]
    }

    for intent, keywords in intent_keywords.items():
        if any(word in query for word in keywords):
            return intent

    return "general"


# 🔹 Rule-based fallback (crop-specific + smart)
def rule_based_advice(intent, crop):
    if intent == "weather":
        return "Check weather updates. Avoid watering if rain is expected."

    if intent == "crop_issue" and crop:
        crop = crop.lower()

        if crop == "rice":
            return "Check water level. Avoid too much water. Use fungicide."
        elif crop == "tomato":
            return "Spray neem oil. Remove infected leaves."
        else:
            return f"Check {crop} plants daily. Remove affected leaves and use pesticide."

    if intent == "farming_advice":
        return "Use fertilizer properly and maintain water level. Monitor crop growth."

    if intent == "market":
        return "Check local market rates before selling. Choose best time."

    return None


# 🔹 Main AI function
def generate_response(query: str, location: str = None, crop: str = None) -> str:

    # ⚠️ Handle empty query
    if not query or query.strip() == "":
        return "Please ask a farming question."

    try:
        # 🔹 Store memory
        conversation_memory.append(query)
        previous = conversation_memory[-2] if len(conversation_memory) > 1 else ""

        intent = detect_intent(query)

        fallback = rule_based_advice(intent, crop)

        prompt = f"""
You are an AI agriculture assistant helping rural farmers.

Previous Query: {previous}
Current Query: {query}
Location: {location or "Not provided"}
Crop: {crop or "Not provided"}
Intent: {intent}

IMPORTANT RULES:
- Use very simple English
- OR respond in local language if needed
- If farmer uses local words, respond in same language
- STRICTLY 2–3 lines only
- Each line max 10 words
- No technical words
- Give direct solution
- Be friendly and clear

ALSO:
- Add one preventive tip for future problems

Example:
"Spray neem oil on leaves.
Check plants daily.
Avoid too much water."
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You help farmers in simple and clear language."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.4
        )

        ai_response = response.choices[0].message.content.strip()

        # 🔹 Clean formatting
        ai_response = ai_response.replace("\n\n", "\n")

        # 🔹 Add location-based tip
        if location and "karnataka" in location.lower():
            ai_response += "\nFollow local weather conditions."

        # 🔥 Combine AI + fallback
        if fallback:
            final_response = ai_response + "\n" + fallback
        else:
            final_response = ai_response

        return final_response

    except Exception as e:
        print("AI Error:", e)

        # 🔥 Smart fallback if API fails
        if fallback:
            return fallback

        return "Check crop condition. Use fertilizer and maintain water level."