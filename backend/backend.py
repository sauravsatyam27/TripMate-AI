import os
import certifi
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


# =========================================================
# IMPORTS
# =========================================================

from typing import TypedDict, Annotated
import operator
import uuid

import psycopg
from psycopg.rows import dict_row

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_groq import ChatGroq

from backend.mcp_client import (
    aviation_mcp_call,
    tavily_mcp_search,
    extract_destination,
    forecast_mcp_search,
    weather_mcp_search
)


# =========================================================
# DATABASE
# =========================================================

def get_database_url():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. "
            "Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:

        separator = "&" if "?" in database_url else "?"

        database_url = (
            f"{database_url}{separator}sslmode=require"
        )

    return database_url


DATABASE_URL = get_database_url()


# =========================================================
# GROQ
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    max_tokens=700
)


# =========================================================
# TEXT LIMIT HELPER
# =========================================================

def limit_text(text, max_chars=3000):

    if text is None:
        return ""

    text = str(text)

    if len(text) > max_chars:

        return (
            text[:max_chars]
            + "\n...[truncated]..."
        )

    return text


# =========================================================
# STATE
# =========================================================

class TravelState(TypedDict):

    messages: Annotated[
        list[AnyMessage],
        operator.add
    ]

    user_query: str

    flight_results: str

    hotel_results: str

    itinerary: str

    llm_calls: int

    weather_results: str


# =========================================================
# FLIGHT AGENT PROMPT
# =========================================================

FLIGHT_AGENT_PROMPT = """
You are a travel flight expert.

User Query:
{query}

Airport Information:
{airport_data}

Airline Information:
{airline_data}

Generate:

1. Likely departure airport
2. Likely arrival airport
3. Airlines serving this route
4. Typical flight duration
5. Estimated airfare range
6. Peak season pricing warning
7. Booking advice

Return concise travel guidance.
"""


# =========================================================
# FLIGHT AGENT
# =========================================================

def flight_agent(state: TravelState):

    print("\nINSIDE FLIGHT AGENT\n")

    query = state["user_query"]

    try:

        # ---------------------------------------------
        # Airports
        # ---------------------------------------------

        airports = asyncio.run(
            aviation_mcp_call(
                "list_airports"
            )
        )

        # ---------------------------------------------
        # Airlines
        # ---------------------------------------------

        airlines = asyncio.run(
            aviation_mcp_call(
                "list_airlines"
            )
        )

        print("\nAIRPORTS:", airports)
        print("\nAIRLINES:", airlines)

        # ---------------------------------------------
        # Limit MCP data before sending to LLM
        # ---------------------------------------------

        airport_data = limit_text(
            airports,
            2000
        )

        airline_data = limit_text(
            airlines,
            2000
        )

        # ---------------------------------------------
        # Prompt
        # ---------------------------------------------

        prompt = FLIGHT_AGENT_PROMPT.format(
            query=query,
            airport_data=airport_data,
            airline_data=airline_data
        )

        # ---------------------------------------------
        # LLM
        # ---------------------------------------------

        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are an expert travel "
                        "flight planner."
                    )
                ),
                HumanMessage(
                    content=prompt
                )
            ]
        )

        flight_data = response.content

    except Exception as e:

        print(
            "\nFLIGHT AGENT ERROR:",
            repr(e)
        )

        flight_data = (
            f"Flight information unavailable: {str(e)}"
        )

    return {

        "flight_results": flight_data,

        "messages": [
            AIMessage(
                content=(
                    "Flight recommendations generated"
                )
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# =========================================================
# HOTEL AGENT
# =========================================================

def hotel_agent(state: TravelState):

    print("\nINSIDE HOTEL AGENT\n")

    query = (
        f"Best hotels for "
        f"{state['user_query']}"
    )

    try:

        hotel_results = asyncio.run(
            tavily_mcp_search(query)
        )

        # ---------------------------------------------
        # Limit Tavily output
        # ---------------------------------------------

        hotel_results = limit_text(
            hotel_results,
            4000
        )

    except Exception as e:

        print(
            "\nHOTEL AGENT ERROR:",
            repr(e)
        )

        hotel_results = (
            f"Hotel information unavailable: {str(e)}"
        )

    return {

        "hotel_results": hotel_results,

        "messages": [
            AIMessage(
                content=(
                    "Hotel information fetched."
                )
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# =========================================================
# WEATHER AGENT
# =========================================================

def weather_agent(state: TravelState):

    print("\nINSIDE WEATHER AGENT\n")

    try:

        # ---------------------------------------------
        # Extract destination
        # ---------------------------------------------

        city = extract_destination(
            state["user_query"]
        )

        print("Destination:", city)

        # ---------------------------------------------
        # Current Weather
        # ---------------------------------------------

        weather_data = asyncio.run(
            weather_mcp_search(city)
        )

        # ---------------------------------------------
        # Forecast
        # ---------------------------------------------

        forecast_data = asyncio.run(
            forecast_mcp_search(city)
        )

        # ---------------------------------------------
        # Limit data
        # ---------------------------------------------

        weather_data = limit_text(
            weather_data,
            1500
        )

        forecast_data = limit_text(
            forecast_data,
            2000
        )

        weather_results = f"""
Current Weather:
{weather_data}

Forecast:
{forecast_data}
"""

    except Exception as e:

        print(
            "\nWEATHER AGENT ERROR:",
            repr(e)
        )

        weather_results = (
            f"Weather information unavailable: {str(e)}"
        )

    return {

        "weather_results": weather_results,

        "messages": [
            AIMessage(
                content=(
                    "Weather information fetched"
                )
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# =========================================================
# ITINERARY AGENT
# =========================================================

def itinerary_agent(state: TravelState):

    print("\nINSIDE ITINERARY AGENT\n")

    prompt = f"""
User Query:
{state['user_query']}

Flight Results:
{limit_text(state['flight_results'], 2500)}

Hotel Results:
{limit_text(state['hotel_results'], 3000)}

Weather Results:
{limit_text(state['weather_results'], 2000)}

Make the itinerary practical,
budget-aware, and easy to follow.
"""

    try:

        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are an expert "
                        "travel planner."
                    )
                ),
                HumanMessage(
                    content=prompt
                )
            ]
        )

        itinerary = response.content

    except Exception as e:

        print(
            "\nITINERARY AGENT ERROR:",
            repr(e)
        )

        itinerary = (
            f"Itinerary unavailable: {str(e)}"
        )

    return {

        "itinerary": itinerary,

        "messages": [
            AIMessage(
                content=itinerary
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# =========================================================
# FINAL AGENT
# =========================================================

def final_agent(state: TravelState):

    print("\nINSIDE FINAL AGENT\n")

    final_prompt = f"""
Generate the final travel response for the user.

User Request:
{state['user_query']}

Flights:
{limit_text(state['flight_results'], 1800)}

Hotels:
{limit_text(state['hotel_results'], 2500)}

Weather Results:
{limit_text(state['weather_results'], 1500)}

Itinerary:
{limit_text(state['itinerary'], 3000)}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Weather Information
5. Day-by-Day Itinerary
6. Estimated Budget
7. Final Recommendations

Important:

- Be clear and practical.
- Mention that live flight API may not provide
  ticket prices if pricing is unavailable.
- Include weather-based travel advice.
- Keep the response useful for real travel planning.
"""

    try:

        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are a professional AI "
                        "travel booking assistant."
                    )
                ),
                HumanMessage(
                    content=final_prompt
                )
            ]
        )

    except Exception as e:

        print(
            "\nFINAL AGENT ERROR:",
            repr(e)
        )

        response = AIMessage(
            content=(
                "Unable to generate final response: "
                f"{str(e)}"
            )
        )

    return {

        "messages": [
            response
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# =========================================================
# BUILD GRAPH
# =========================================================

graph = StateGraph(TravelState)


graph.add_node(
    "flight_agent",
    flight_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "weather_agent",
    weather_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)


# =========================================================
# EDGES
# =========================================================

graph.add_edge(
    START,
    "flight_agent"
)

graph.add_edge(
    "flight_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "weather_agent"
)

graph.add_edge(
    "weather_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)


# =========================================================
# POSTGRES CHECKPOINTER
# =========================================================

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(
    _conn
)

checkpointer.setup()


travel_graph = graph.compile(
    checkpointer=checkpointer
)


# =========================================================
# RUN TRAVEL AGENT
# =========================================================

def run_travel_agent(
    user_input: str,
    thread_id: str | None = None
):

    if not thread_id:

        thread_id = (
            f"user_{uuid.uuid4().hex}"
        )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = travel_graph.invoke(

        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ],

            "user_query": user_input,

            "flight_results": "",

            "hotel_results": "",

            "weather_results": "",

            "itinerary": "",

            "llm_calls": 0
        },

        config=config
    )

    final_answer = (
        result["messages"][-1].content
    )

    return {

        "thread_id": thread_id,

        "answer": final_answer,

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