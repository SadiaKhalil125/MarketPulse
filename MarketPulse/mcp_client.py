import asyncio
import os
import logging
from dotenv import load_dotenv

from fastmcp import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool  # updated import

async def client_code(query:str):
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    client = Client("mcp_server.py")
    async with client:
        tools_list = await client.list_tools()
        logger.info(f"Available tools: {[t.name for t in tools_list]}")

        @tool
        async def get_crypto_price(symbol: str) -> dict:
            """Fetch the current cryptocurrency price by symbol."""
            return await client.call_tool("get_crypto_price", {"symbol": symbol})

        @tool
        async def get_stock_price(symbol: str) -> dict:
            """Fetch the current stock price by ticker symbol."""
            return await client.call_tool("get_stock_price", {"symbol": symbol})

        @tool
        async def get_stock_news(query:str) -> dict:
            """Fetch the latest stock market news."""
            return await client.call_tool("get_stock_news", {})

        tools = [get_crypto_price, get_stock_price, get_stock_news]

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
        )

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        logger.info("MCP client ready — ask your query (type 'exit'):")
        while True:
            # query = input("> ")
            if query.lower() in {"exit", "quit"}:
                break
            try:
                result = await agent.arun(query)
                return result
                print("🤖", result)
            except Exception as e:
                logger.error("Error during agent execution:", exc_info=e)

if __name__ == "__main__":
    asyncio.run(client_code("What is the current price of Bitcoin and Apple stock?"))  # Example query
