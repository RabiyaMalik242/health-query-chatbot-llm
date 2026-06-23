# 🤖 General Health Query Chatbot

A conversational AI chatbot that answers general health-related questions using a Large Language Model (LLM) with prompt engineering and two-layer safety filters. Features a polished Streamlit web interface. Built as part of an AI/ML Internship.

---

## 📌 Objective

Build a health query chatbot using the Groq API (LLaMA 3.3 70B) that responds to general health questions in a friendly, clear, and safe manner using prompt engineering techniques.

---

## 📂 Project Structure

```
health-query-chatbot-llm/
│
├── health_chatbot.ipynb   # Full project notebook — pipeline, demos, analysis
├── chatbot.py             # Core logic — single source of truth
├── app.py                 # Streamlit web interface
├── requirements.txt
└── README.md
```

**How the files connect:**
- `chatbot.py` contains all the core logic — API setup, system prompt, safety filters, and chat functions
- `health_chatbot.ipynb` imports from `chatbot.py` to demonstrate and explain the pipeline
- `app.py` imports from `chatbot.py` to power the web interface
- Change anything in `chatbot.py` once — both the notebook and app reflect it instantly

---

## 🛠️ Tools & Libraries

- Python 3
- [Groq API](https://console.groq.com) — LLaMA 3.3 70B (free tier)
- Streamlit — web interface
- Jupyter Notebook — project documentation and pipeline demo

---

## ⚙️ Project Pipeline (Notebook)

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

## 🖥️ Streamlit Interface Features

- Dark medical-themed UI
- Chat bubbles with **👤 You** and **🤖 MediBot** labels
- Quick question chips — click to instantly ask common questions
- Auto-scrolls to latest message after every response
- Input box clears automatically after sending
- Enter key or Send button both submit messages
- Emergency banner (red) for life-threatening queries with Pakistan + international numbers
- Blocked banner (yellow) for unsafe queries
- Session stats — query count and total tokens used
- Clear conversation button
- Safety filter status badges in sidebar

---

## 🛡️ Safety Design

| Layer | Method |
|---|---|
| Pre-filter | Keyword blocklist — catches harmful and emergency queries before hitting the API |
| LLM-level | System prompt rules — controls tone, scope, and refusal behavior |
| Emergency | Detected keywords trigger immediate redirect to emergency services with specific numbers |
| Mental health | Suicidal/self-harm keywords trigger empathetic response with Pakistani and international crisis numbers |

**Emergency numbers shown in the app:**
- 🇵🇰 Pakistan: **115** (Rescue), **1122** (Edhi), Umang Helpline **0317-4288665**
- 🌍 International: **112**

---

## 🧠 Prompt Engineering

A key focus of this project is demonstrating how system prompt design changes model behavior. Three prompt styles are compared in the notebook:

| Prompt Style | Result |
|---|---|
| ❌ Generic (`You are a helpful assistant`) | Unstructured, no medical safety |
| ⚠️ Too vague (`Answer health questions briefly`) | Incomplete, no disclaimers |
| ✅ Engineered MediBot prompt | Structured, safe, empathetic, with doctor referral |

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

## 🚀 How to Run

1. Clone the repository
```bash
   git clone https://github.com/RabiyaMalik242/health-query-chatbot-llm.git
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Get a free Groq API key at [console.groq.com](https://console.groq.com)

4. Open `chatbot.py` and paste your API key on line 20:
```python
   GROQ_API_KEY = "your_groq_api_key_here"
```

5. Run the Streamlit interface
```bash
   streamlit run app.py
```

6. Or open `health_chatbot.ipynb` to explore the full project pipeline

---

## ⚠️ Limitations

- Keyword-based safety filter can be bypassed with creative phrasing — a production app would use an LLM-based content moderation layer
- The model can hallucinate medical facts — always verify with a qualified doctor
- No persistent memory across sessions — conversation history resets when the app restarts
- Token usage grows with conversation length — history should be trimmed in long sessions

---

## ⚕️ Disclaimer

MediBot is a demonstration project for educational purposes only. It does not provide medical advice and is not a substitute for professional healthcare. Always consult a qualified healthcare professional for medical concerns.

---

## 👩‍💻 Author

Rabiya Malik BS Software Engineering — AI/ML Internship Project
