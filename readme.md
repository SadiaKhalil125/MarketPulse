# MarketPulse 🤖

An AI-powered financial assistant that provides real-time information about stocks, cryptocurrencies, and market news using Streamlit and LangChain.

## Features

- 📈 Real-time stock price lookups
- 💰 Cryptocurrency price tracking
- 📰 Latest market news updates
- 🤖 AI-powered natural language interactions
- 💬 Chat interface with message history
- 🚀 Quick action shortcuts

## Prerequisites

- Python 3.11 or higher
- Google API key for Gemini AI
- Firecrawl API key

## Installation

1. Clone the repository
2. Install dependencies:
```sh
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
GOOGLE_API_KEY="your-google-api-key"
FIRECRAWL_API_KEY="your-firecrawl-api-key"
```

## Usage

1. Start the MCP server:
```sh
python mcp_server.py
```

2. In a new terminal, launch the Streamlit app:
```sh
streamlit run streamlit_app.py
```

3. Open your browser and navigate to the displayed URL (typically http://localhost:8501)

## Features

### Quick Actions
- Get BTC price
- Get ETH price
- View latest stock market news

### Query Templates
- Look up any stock price by symbol (e.g., AAPL, GOOG)
- Check any cryptocurrency price (e.g., SOL, XRP)

### Chat Interface
- Ask natural language questions about stocks, crypto, or market news
- View conversation history
- Real-time responses powered by Gemini AI

## Project Structure

- `streamlit_app.py`: Main Streamlit web interface
- `mcp_server.py`: Backend server handling financial data requests
- `mcp_client.py`: Client code for AI agent and tool integration
- `requirements.txt`: Project dependencies
- `.env`: Configuration file for API keys

## Dependencies

- streamlit: Web interface
- langchain: AI agent framework
- firecrawl-py: Web scraping and data extraction
- python-dotenv: Environment variable management
- asyncio-mqtt: Asynchronous MQTT support
- fastmcp: Message Communication Protocol

## License

This project is licensed under the MIT License - see the LICENSE file for details.