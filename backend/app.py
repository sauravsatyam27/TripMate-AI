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
# FASTAPI APP
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
        # Main Vercel production URL
        "https://trip-mate-ai-woad.vercel.app",

        # Vercel deployment URL
        "https://trip-mate-ai-git-main-sauravsatyam27s-projects.vercel.app",

        # Local frontend
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
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health_check():

    return {
        "status": "ok",
        "message": "AI Travel Planner API is running"
    }


# =========================================================
# TRAVEL API
# =========================================================

@app.post("/api/travel")
def travel_planner(request_data: TravelRequest):

    try:

        # -------------------------------------------------
        # Get user message
        # -------------------------------------------------

        user_message = request_data.message.strip()

        # -------------------------------------------------
        # Validate message
        # -------------------------------------------------

        if not user_message:

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty."
                }
            )

        # -------------------------------------------------
        # Logs
        # -------------------------------------------------

        print("\n" + "=" * 70)
        print("TRIPMATE AI - TRAVEL REQUEST")
        print("=" * 70)

        print("Message:", user_message)
        print("Thread ID:", request_data.thread_id)

        # -------------------------------------------------
        # Run LangGraph Travel Agent
        # -------------------------------------------------

        result = run_travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id
        )

        # -------------------------------------------------
        # Success Response
        # -------------------------------------------------

        return JSONResponse(
            status_code=200,
            content={
                "success": True,

                "thread_id": result.get(
                    "thread_id"
                ),

                "answer": result.get(
                    "answer",
                    ""
                ),

                "flight_results": result.get(
                    "flight_results",
                    ""
                ),

                "hotel_results": result.get(
                    "hotel_results",
                    ""
                ),

                "weather_results": result.get(
                    "weather_results",
                    ""
                ),

                "itinerary": result.get(
                    "itinerary",
                    ""
                ),

                "llm_calls": result.get(
                    "llm_calls",
                    0
                )
            }
        )

    except Exception as e:

        # -------------------------------------------------
        # Error Logs
        # -------------------------------------------------

        print("\n" + "=" * 70)
        print("TRIPMATE AI - TRAVEL API ERROR")
        print("=" * 70)

        print("ERROR:", str(e))

        traceback.print_exc()

        # -------------------------------------------------
        # Error Response
        # -------------------------------------------------

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# =========================================================
# FAVICON
# =========================================================

@app.get("/favicon.ico")
async def favicon():

    return JSONResponse(
        content={}
    )


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )