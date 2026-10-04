import asyncio

from Multi_Agent_traveller.backend.mcp_client import get_all_tools


async def main():

    print("\n======================================")
    print("       ALL MCP TOOLS TEST")
    print("======================================\n")

    await get_all_tools()


if __name__ == "__main__":
    asyncio.run(main())