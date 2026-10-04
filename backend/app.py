import traceback
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.backend import run_travel_agent

import nest_asyncio

nest_asyncio.apply()


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="TripMate AI",
    description="LangGraph Multi-Agent Travel Planner API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trip-mate-ai-woad.vercel.app",
        "https://trip-mate-ai-git-main-sauravsatyam27s-projects.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class TravelRequest(BaseModel):
    message: str
    thread_id: str | None = None


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Travel Planner API is running"
    }


# =========================================================
# TRAVEL API
# =========================================================

@app.post("/api/travel")
def travel_planner(request_data: TravelRequest):

    print("\n" + "=" * 70)
    print("TRIPMATE REQUEST START")
    print("=" * 70)

    try:

        user_message = request_data.message.strip()

        print("MESSAGE:", user_message)
        print("THREAD:", request_data.thread_id)

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty."
                }
            )

        print("\nStarting run_travel_agent()...")

        # =====================================================
        # RUN AGENT
        # =====================================================

        result = run_travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id
        )

        print("\nrun_travel_agent() completed successfully.")

        print("RESULT TYPE:", type(result))

        # =====================================================
        # RESPONSE
        # =====================================================

        response_data = {
            "success": True,
            "thread_id": result.get("thread_id"),
            "answer": result.get("answer", ""),
            "flight_results": result.get("flight_results", ""),
            "hotel_results": result.get("hotel_results", ""),
            "weather_results": result.get("weather_results", ""),
            "itinerary": result.get("itinerary", ""),
            "llm_calls": result.get("llm_calls", 0)
        }

        print("Sending successful response.")

        return JSONResponse(
            status_code=200,
            content=response_data
        )

    except Exception as e:

        print("\n" + "=" * 70)
        print("TRIPMATE BACKEND ERROR")
        print("=" * 70)

        print("ERROR TYPE:", type(e).__name__)
        print("ERROR:", str(e))

        traceback.print_exc()

        print("=" * 70)

        # TEMPORARY DEBUG RESPONSE
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_type": type(e).__name__,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


# =========================================================
# FAVICON
# =========================================================

@app.get("/favicon.ico")
def favicon():
    return JSONResponse(content={})


# =========================================================
# LOCAL
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )