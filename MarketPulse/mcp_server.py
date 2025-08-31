import asyncio
import os
import sys
import logging
from firecrawl import Firecrawl
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
# Set up logging for debugging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Initialize MCP Server
mcp = FastMCP("crypto-stock-price-tracker")

# Initialize Firecrawl
try:
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    logger.info("Firecrawl initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firecrawl: {e}")
    sys.exit(1)

@mcp.tool()
def get_crypto_price(symbol: str) -> dict:
    """
    Get the current price of a cryptocurrency from CoinGecko using Firecrawl.
    Example: get_crypto_price("bitcoin")
    """
    try:
        logger.info(f"Getting crypto price for: {symbol}")
        url = f"https://www.coingecko.com/en/coins/{symbol.lower()}"

        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "string"},
                "market_cap": {"type": "string"},
                "change_24h": {"type": "string"}
            },
            "required": ["price"]
        }

        res = firecrawl.extract(
            urls=[url],
            prompt=f"Extract the current price, 24h change, and market cap of {symbol} in USD.",
            schema=schema,
        )

        logger.info(f"Successfully got crypto data for {symbol}")
        return res.data
    except Exception as e:
        logger.error(f"Error getting crypto price for {symbol}: {e}")
        return {"error": str(e), "price": "N/A", "market_cap": "N/A", "change_24h": "N/A"}

@mcp.tool()
def get_stock_price(symbol: str) -> dict:
    """
    Get the current stock price of a company from Yahoo Finance using Firecrawl.
    Example: get_stock_price("AAPL") or get_stock_price("^DJI")
    """
    try:
        logger.info(f"Getting stock price for: {symbol}")
        url = f"https://finance.yahoo.com/quote/{symbol.upper()}"

        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "string"},
                "change": {"type": "string"},
                "change_percent": {"type": "string"}
            },
            "required": ["price"]
        }

        res = firecrawl.extract(
            urls=[url],
            prompt=f"Extract the current stock price, price change, percentage change, previous close, open price, volume, and market cap for {symbol}.",
            schema=schema,
        )

        logger.info(f"Successfully got stock data for {symbol}")
        return res.data
    except Exception as e:
        logger.error(f"Error getting stock price for {symbol}: {e}")
        return {"error": str(e), "price": "N/A", "change": "N/A", "change_percent": "N/A"}

@mcp.tool()
def get_stock_news() -> dict:
    """
    Get the latest news about a stock from Yahoo Finance using Firecrawl.
    Example: get_stock_news("AAPL", 3) or get_stock_news("TSLA")
    """
    try:
        logger.info(f"Getting latest stock news")
        url = f"https://finance.yahoo.com/"

        schema = {
        "type": "object",
        "properties": {
            "news_articles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "summary": {"type": "string"}
                    }
                }
            }
        },
        "required": ["news_articles"]
        }


        res = firecrawl.extract(
            urls=[url],
            prompt=f"Extract the latest 1-3 news articles related to stock market.",
            schema=schema,
        )

        logger.info(f"Successfully got news")
        return res.data
    except Exception as e:
        logger.error(f"Error getting stock news")
        return {"error": str(e), "news_articles": []}

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    try:
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)