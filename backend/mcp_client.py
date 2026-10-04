import os
import sys
import certifi

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq


# =========================================================
# SSL
# =========================================================

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv(override=True)


# =========================================================
# ENV
# =========================================================

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


print("\n========== API KEY CHECK ==========")
print("TAVILY:", bool(TAVILY_API_KEY))
print("AVIATIONSTACK:", bool(AVIATIONSTACK_API_KEY))
print("OPENWEATHER:", bool(OPENWEATHER_API_KEY))
print("GROQ:", bool(GROQ_API_KEY))
print("===================================\n")


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)


# =========================================================
# TAVILY CLIENT
# =========================================================

tavily_client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": (
                f"https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={TAVILY_API_KEY}"
            ),
        }
    }
)


# =========================================================
# AVIATION CLIENT
# =========================================================

aviation_client = MultiServerMCPClient(
    {
        "aviationstack": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "aviationstack-mcp"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATIONSTACK_API_KEY
            },
        }
    }
)


# =========================================================
# WEATHER CLIENT
# =========================================================

weather_client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                r"E:\Projects 2\Multi-Agent AI System\Part 2 MCP\custom_weather_mcp.py"
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            },
        }
    }
)


# =========================================================
# GLOBAL TOOLS
# =========================================================

search_tool = None
aviation_tools = {}

weather_tool = None
forecast_tool = None


# =========================================================
# TAVILY
# =========================================================

async def initialize_tavily():

    global search_tool

    if search_tool is not None:
        return

    print("\n========== INITIALIZING TAVILY ==========")

    tools = await tavily_client.get_tools()

    for tool in tools:
        print("Tavily tool:", tool.name)

    search_tool = next(
        (
            tool
            for tool in tools
            if tool.name == "tavily_search"
        ),
        None
    )

    if search_tool is None:
        raise RuntimeError(
            "tavily_search tool not found"
        )

    print("Tavily initialized successfully.")


async def tavily_mcp_search(query: str):

    await initialize_tavily()

    print("\nINSIDE TAVILY MCP")
    print("Query:", query)

    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )

    return result


# =========================================================
# AVIATION
# =========================================================

async def initialize_aviation():

    global aviation_tools

    if aviation_tools:
        return

    print("\n========== INITIALIZING AVIATION MCP ==========")

    tools = await aviation_client.get_tools()

    for tool in tools:
        print("Aviation tool:", tool.name)

    aviation_tools = {
        tool.name: tool
        for tool in tools
    }

    print("Aviation initialized successfully.")


async def aviation_mcp_call(
    tool_name: str,
    tool_args: dict = None
):

    await initialize_aviation()

    if tool_name not in aviation_tools:

        raise RuntimeError(
            f"Aviation tool '{tool_name}' not found. "
            f"Available: {list(aviation_tools.keys())}"
        )

    tool = aviation_tools[tool_name]

    return await tool.ainvoke(
        tool_args or {}
    )


# =========================================================
# WEATHER
# =========================================================

async def initialize_weather():

    global weather_tool
    global forecast_tool

    if weather_tool is not None:
        return

    print("\n========== INITIALIZING WEATHER MCP ==========")

    tools = await weather_client.get_tools()

    for tool in tools:
        print("Weather tool:", tool.name)

    weather_tool = next(
        (
            tool
            for tool in tools
            if tool.name == "get_current_weather"
        ),
        None
    )

    forecast_tool = next(
        (
            tool
            for tool in tools
            if tool.name == "get_forecast"
        ),
        None
    )

    print("Weather initialized successfully.")


async def weather_mcp_search(city: str):

    await initialize_weather()

    if weather_tool is None:
        raise RuntimeError(
            "get_current_weather tool not found"
        )

    return await weather_tool.ainvoke(
        {
            "city": city
        }
    )


async def forecast_mcp_search(city: str):

    await initialize_weather()

    if forecast_tool is None:
        raise RuntimeError(
            "get_forecast tool not found"
        )

    return await forecast_tool.ainvoke(
        {
            "city": city
        }
    )


# =========================================================
# DESTINATION EXTRACTOR
# =========================================================

def extract_destination(query: str):

    prompt = f"""
Extract only the destination city or country.

Query:
{query}

Return only destination name.
"""

    response = llm.invoke(prompt)

    return response.content.strip()