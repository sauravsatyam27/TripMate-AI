import traceback
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
async def travel_planner(
    request_data: TravelRequest
):

    try:

        user_message = request_data.message.strip()

        if not user_message:

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty."
                }
            )

        print("\n" + "=" * 60)
        print("TRAVEL REQUEST")
        print("=" * 60)

        print("Message:", user_message)
        print("Thread ID:", request_data.thread_id)

        # ---------------------------------------------
        # RUN LANGGRAPH
        # ---------------------------------------------

        result = run_travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id
        )

        # ---------------------------------------------
        # RESPONSE
        # ---------------------------------------------

        return JSONResponse(
            content={
                "success": True,

                "thread_id": result["thread_id"],

                "answer": result["answer"],

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

        print("\n" + "=" * 60)
        print("TRAVEL API ERROR")
        print("=" * 60)

        print("ERROR:", str(e))

        traceback.print_exc()

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
# RUN
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )