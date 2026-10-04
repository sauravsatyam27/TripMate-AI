# ✈️ TripMate AI — Multi-Agent AI Travel Planner

TripMate AI is an AI-powered travel planning application that creates personalized travel plans from natural-language requests.

Users can simply ask:

> "Plan a 5-day trip from Delhi to Jaipur with flights, hotels, weather and a complete itinerary."

The system uses **LangGraph multi-agent orchestration** to handle different travel tasks and combines the results into a complete travel plan.

---

## 🚀 Features

- 🤖 **Multi-Agent AI Travel Planning**
- ✈️ Flight information using **AviationStack**
- 🏨 Hotel & travel search using **Tavily**
- 🌤️ Weather information using **OpenWeather**
- 🧠 LLM-powered reasoning using **Groq**
- 🔄 Stateful conversations with **LangGraph**
- 💾 PostgreSQL-based checkpoint persistence
- 🆔 Thread-based conversation memory
- ⚛️ Modern **React + Vite + Tailwind CSS** frontend
- 📋 Copy generated travel plans
- 📄 Download travel plans as PDF
- 🔌 MCP-based external tool integration

---

## 🏗️ Architecture

```text
                    User
                     |
                     v
             React + Tailwind
                     |
                /api/travel
                     |
                     v
                  FastAPI
                     |
                     v
                LangGraph
                     |
        +------------+------------+
        |            |            |
        v            v            v
   Flight Agent  Hotel Agent  Weather Agent
        |            |            |
        +------------+------------+
                     |
                     v
              Itinerary Agent
                     |
                     v
                Final Agent
                     |
                     v
              Travel Plan
```

---

## 🤖 Agents

| Agent | Responsibility |
|---|---|
| ✈️ Flight Agent | Searches flight information |
| 🏨 Hotel Agent | Finds accommodation/travel information |
| 🌤️ Weather Agent | Retrieves destination weather |
| 🗺️ Itinerary Agent | Creates a day-by-day itinerary |
| ✨ Final Agent | Generates the final user-friendly response |

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- JavaScript
- Marked.js
- html2pdf.js

### Backend
- Python
- FastAPI
- LangChain
- LangGraph
- Groq
- PostgreSQL
- Psycopg

### External Services
- AviationStack
- Tavily
- OpenWeather
- MCP

---

## 📁 Project Structure

```text
Multi_Agent_traveller/
│
├── backend/
│   ├── app.py
│   ├── backend.py
│   └── mcp_client.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Background.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── Planner.jsx
│   │   │   └── Result.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Multi_Agent_traveller
```

### 2. Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
AVIATIONSTACK_API_KEY=your_aviationstack_key
OPENWEATHER_API_KEY=your_openweather_key

DATABASE_URL=your_postgresql_connection_string
```

> Never commit your `.env` file to GitHub.

### 4. Start Backend

Run from the project root:

```bash
python -m uvicorn backend.app:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

### 5. Start Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 💬 Example Prompts

### Basic Trip

```text
Plan a 3-day trip from Delhi to Jaipur.
```

### Complete Trip

```text
Plan a 5-day trip from Delhi to Mumbai with flights,
hotels, weather and a complete itinerary.
```

### Budget Trip

```text
Plan a budget trip from Delhi to Goa for 4 days
under ₹30,000.
```

### Follow-up

```text
Add one more day to the trip.
```

```text
Make the itinerary more relaxed.
```

```text
Reduce the hotel budget.
```

---

## 🧠
