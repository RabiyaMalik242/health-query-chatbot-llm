# 🤖 General Health Query Chatbot

A conversational AI chatbot that answers general health-related questions using a Large Language Model (LLM) with prompt engineering and two-layer safety filters. Built as part of an AI/ML Internship.

---

## 📌 Objective

Build a health query chatbot using the Groq API (LLaMA 3.3 70B) that responds to general health questions in a friendly, clear, and safe manner using prompt engineering techniques.

---

## 🛠️ Tools & Libraries

- Python 3
- [Groq API](https://console.groq.com) — LLaMA 3.3 70B (free tier)
- Jupyter Notebook
- IPython Display (Markdown rendering)

---

## ⚙️ Project Pipeline

1. **API Setup** — Groq client initialization with LLaMA 3.3 70B
2. **Prompt Engineering** — Designed a detailed system prompt giving the model a medical assistant persona with strict rules
3. **Safety Filters** — Two-layer safety system:
   - Pre-filter: keyword-based blocklist for harmful queries
   - LLM-level: system prompt guardrails
4. **Single Query Demo** — 4 test health questions
5. **Prompt Engineering Comparison** — Same question answered with 3 different system prompts to demonstrate the impact of prompt design
6. **Safety Filter Demo** — Normal, emergency, and blocked query handling
7. **Multi-Turn Conversation** — Chatbot maintains context across multiple exchanges
8. **Interactive Chat Loop** — Live chat interface inside the notebook
9. **Token Usage Tracking** — Monitors prompt/completion/total tokens per API call

---

## 🔑 Key Features

- **MediBot Persona** — Friendly, knowledgeable health assistant with clear rules and boundaries
- **Emergency Detection** — Redirects life-threatening queries (chest pain, stroke, seizure) to emergency services immediately
- **Blocked Query Handling** — Politely refuses harmful or inappropriate requests
- **Conversation Memory** — Full history passed with each API call for context-aware responses
- **Token Tracking** — Monitors API usage per query for production awareness

---

## 🛡️ Safety Design

| Layer | Method |
|---|---|
| Pre-filter | Keyword blocklist — catches harmful queries before hitting the API |
| LLM-level | System prompt rules — controls tone, scope, and refusal behavior |
| Emergency | Detected keywords trigger immediate redirect to emergency services |

---

## 💬 Example Queries

```
"What causes a sore throat?"
"Is paracetamol safe for children?"
"What are common symptoms of dehydration?"
"How can I improve my sleep quality?"
"What is hypertension?"
```

---

## 🧠 Prompt Engineering

A key focus of this project is demonstrating how system prompt design changes model behavior. Three prompt styles are compared in the notebook:

| Prompt Style | Result |
|---|---|
| ❌ Generic (`You are a helpful assistant`) | Unstructured, no medical safety |
| ⚠️ Too vague (`Answer health questions briefly`) | Incomplete, no disclaimers |
| ✅ Engineered MediBot prompt | Structured, safe, empathetic, with doctor referral |

---

## 🚀 How to Run

1. Clone the repository
```bash
   git clone https://github.com/RabiyaMalik242/health-query-chatbot-llm.git
```
2. Install dependencies
```bash
   pip install groq
```
3. Get a free Groq API key at [console.groq.com](https://console.groq.com)
4. Open `health_chatbot.ipynb` and paste your API key in Section 2
5. Run all cells — the interactive chat starts at Section 10

---

## 📁 Repository Structure

```
health-query-chatbot-llm/
│
├── health_chatbot.ipynb   # Main notebook
└── README.md
```

---

## ⚠️ Limitations

- Keyword-based safety filter can be bypassed with creative phrasing — a production app would use an LLM-based content moderation layer
- The model can hallucinate medical facts — always verify with a qualified doctor
- No persistent memory across sessions — conversation history resets when the notebook restarts
- Token usage grows with conversation length — history should be trimmed in long sessions

---

## ⚕️ Disclaimer

MediBot is a demonstration project for educational purposes only. It does not provide medical advice and is not a substitute for professional healthcare. Always consult a qualified healthcare professional for medical concerns.

---

## 👩‍💻 Author

Rabiya Malik BS Software Engineering — AI/ML Internship Project
