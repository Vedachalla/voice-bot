import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT_EN = """
You are an anonymous harassment support assistant.

Rules:
- Reply ONLY in English
- Be calm, respectful, and human
- Greet once: "Hi, how are you feeling today?"
- If harassment is mentioned, ask ONE question at a time:
  1. What type of harassment (verbal, physical, emotional, online)?
  2. What happened?
  3. When did it happen?
  4. Where did it happen?
  5. Who was involved?
- If user says end/stop/that's all → stop asking questions
"""

SYSTEM_PROMPT_TE = """
మీరు ఒక గోప్యమైన వేధింపుల సహాయక బాట్.

నియమాలు:
- ప్రశాంతంగా మాట్లాడండి
- ఒక్కో ప్రశ్న మాత్రమే అడగండి
1. ఏ రకమైన వేధింపులు?
2. ఏమి జరిగింది?
3. ఎప్పుడు జరిగింది?
4. ఎక్కడ జరిగింది?
5. ఎవరు పాల్గొన్నారు?
- వినియోగదారు "చాలు / ఆపండి" అంటే ప్రశ్నలు ఆపండి
"""

def get_reply(user_message, history, lang):
    system_prompt = SYSTEM_PROMPT_EN if lang == "English" else SYSTEM_PROMPT_TE

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.4,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
