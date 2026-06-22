"""
chatbot.py — MediBot Core Logic
================================
Single source of truth for all chatbot logic.
Imported by both health_chatbot.ipynb and app.py.

Extracted from health_chatbot.ipynb:
  - Cell 5  → GROQ_API_KEY, client, MODEL
  - Cell 7  → SYSTEM_PROMPT
  - Cell 9  → BLOCKED_KEYWORDS, EMERGENCY_KEYWORDS, safety_check()
  - Cell 11 → EMERGENCY_MESSAGE, BLOCKED_MESSAGE, chat()
  - Cell 26 → chat_with_stats()
"""

from groq import Groq

# ── Cell 5: API key & model ───────────────────────────────────────────────────
GROQ_API_KEY = "GROQ_API_KEY"   # <-- paste your key here once
MODEL        = "llama-3.3-70b-versatile"
client       = Groq(api_key=GROQ_API_KEY)

# ── Cell 7: System prompt ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a friendly and knowledgeable general health assistant named MediBot.

Your role:
- Answer general health questions clearly, accurately, and in simple language
- Explain medical terms when you use them
- Be empathetic and supportive in your tone
- Keep responses concise (3-5 sentences for simple questions, more for complex ones)
- Use bullet points when listing symptoms, causes, or steps

Your strict rules:
- ALWAYS end responses with a reminder to consult a qualified doctor for personal medical advice
- NEVER diagnose a specific condition for a specific person
- NEVER recommend specific prescription drugs or dosages
- NEVER provide advice that could replace emergency medical care
- If someone describes a medical emergency, immediately direct them to call emergency services

Crisis & Mental Health rules:
- If someone mentions suicidal thoughts, self-harm, or mental health crisis, respond with empathy first
- ALWAYS provide these specific crisis numbers immediately:
  * Pakistan: Umang helpline 0317-4288665, Rozan Counseling 051-2890505
  * International: Befrienders Worldwide +44-20-7553-9157
  * Emergency: 115 (Pakistan Rescue), 1122 (Edhi Foundation)
- Never refuse to share these numbers when someone is in distress
- Encourage the person to reach out immediately

You are NOT a replacement for professional medical advice. You provide general health information only."""

# ── Cell 9: Safety filter ─────────────────────────────────────────────────────
BLOCKED_KEYWORDS = [
    'how to overdose', 'suicide method',
    'how much to overdose', 'lethal dose',
    'get high', 'recreational drugs', 'buy drugs', 'drug dealer',
    'how to get prescription without doctor',
    'avoid going to hospital', 'ignore symptoms', 'stop taking medication',
]

EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'cant breathe', "can't breathe",
    'stroke', 'unconscious', 'not breathing', 'severe bleeding',
    'poisoning', 'overdose', 'seizure',
    # Mental health emergencies
    'suicidal thoughts', 'want to die', 'kill myself', 'end my life',
    'thinking about suicide', 'hurting myself',
]

def safety_check(query: str) -> dict:
    """
    Returns dict with:
      - 'safe'      : bool — whether to proceed
      - 'emergency' : bool — whether to show emergency message
      - 'reason'    : str  — explanation if blocked
    """
    q_lower = query.lower()

    for kw in EMERGENCY_KEYWORDS:
        if kw in q_lower:
            return {'safe': True, 'emergency': True, 'reason': ''}

    for kw in BLOCKED_KEYWORDS:
        if kw in q_lower:
            return {
                'safe'     : False,
                'emergency': False,
                'reason'   : f"Query contains restricted content: '{kw}'"
            }

    if len(query.strip()) < 3:
        return {'safe': False, 'emergency': False, 'reason': 'Query too short.'}

    if len(query.strip()) > 1000:
        return {'safe': False, 'emergency': False, 'reason': 'Query too long (max 1000 chars).'}

    return {'safe': True, 'emergency': False, 'reason': ''}

# ── Cell 11: Messages & chat function ────────────────────────────────────────
EMERGENCY_MESSAGE = """
🚨 **This sounds like a medical emergency.**

**Please call emergency services immediately:**
- 🇵🇰 Pakistan: **115** (Rescue) or **1122** (Edhi)
- 🌍 International: **112** or your local emergency number

Do not wait — get professional help right now.
"""

BLOCKED_MESSAGE = """
⚠️ I'm sorry, I can't help with that request.

MediBot is designed for general health information only.
Please consult a qualified healthcare professional for personal medical advice.
"""

def chat(query: str, history: list, temperature: float = 0.4, max_tokens: int = 512) -> tuple:
    """
    Send a query to the health chatbot.

    Args:
        query       : user's question
        history     : list of previous messages [{'role':..., 'content':...}]
        temperature : controls randomness (default 0.4)
        max_tokens  : max response length (default 512)

    Returns:
        (response_text, updated_history)
    """
    check = safety_check(query)

    if check['emergency']:
        return EMERGENCY_MESSAGE, history

    if not check['safe']:
        return BLOCKED_MESSAGE, history

    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    messages += history
    messages.append({'role': 'user', 'content': query})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    reply = response.choices[0].message.content

    history.append({'role': 'user',      'content': query})
    history.append({'role': 'assistant', 'content': reply})

    return reply, history

# ── Cell 26: chat with token stats ───────────────────────────────────────────
def chat_with_stats(query: str, history: list, temperature: float = 0.4, max_tokens: int = 512) -> dict:
    check = safety_check(query)

    if check['emergency']:
        return {
            'response'         : EMERGENCY_MESSAGE,
            'status'           : 'emergency',
            'history'          : history,
            'prompt_tokens'    : 0,
            'completion_tokens': 0,
            'total_tokens'     : 0
        }

    if not check['safe']:
        return {
            'response'         : BLOCKED_MESSAGE,
            'status'           : 'blocked',
            'history'          : history,
            'prompt_tokens'    : 0,
            'completion_tokens': 0,
            'total_tokens'     : 0
        }

    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    messages += history
    messages.append({'role': 'user', 'content': query})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    reply = response.choices[0].message.content
    usage = response.usage

    history.append({'role': 'user',      'content': query})
    history.append({'role': 'assistant', 'content': reply})

    return {
        'response'         : reply,
        'status'           : 'ok',
        'history'          : history,
        'prompt_tokens'    : usage.prompt_tokens,
        'completion_tokens': usage.completion_tokens,
        'total_tokens'     : usage.total_tokens,
    }