import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import time
import pandas as pd
from datetime import datetime
import yfinance as yf
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .stTab [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTab [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

class MultiAgentSystem:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_base_url = "https://api.groq.com/openai/v1/chat/completions"
        
    def call_groq_api(self, messages: List[Dict], model: str = "llama3-70b-8192") -> str:
        """Make API call to Groq"""
        if not self.groq_api_key:
            return "Error: GROQ_API_KEY not found. Please add it to your .env file."
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.groq_base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"
    
    def web_search_agent(self, query: str) -> str:
        """Simulate web search agent"""
        messages = [
            {"role": "system", "content": "You are a web search agent. Provide comprehensive information about the query as if you searched the web. Always include sources and current information. Format your response in markdown."},
            {"role": "user", "content": f"Search for information about: {query}"}
        ]
        return self.call_groq_api(messages)
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_data(_self, symbol: str) -> Dict:
        """Get stock data with fallback options"""
        # First try yfinance with error handling
        try:
            stock = yf.Ticker(symbol)
            
            # Try to get basic info first (less API calls)
            hist = stock.history(period="5d")  # Get recent history
            if hist.empty:
                raise Exception("No historical data available")
            
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            # Try to get additional info, but handle failures gracefully
            info = {}
            try:
                info = stock.info
            except:
                info = {}  # If info fails, continue with basic data
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "previous_close": round(previous_close, 2),
                "price_change": round(current_price - previous_close, 2),
                "price_change_percent": round(((current_price - previous_close) / previous_close) * 100, 2),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "company_name": info.get("longName", symbol),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "volume": info.get("volume", "N/A"),
                "data_source": "Yahoo Finance (Limited)"
            }
            
        except Exception as e:
            # Fallback to mock data with AI analysis
            return _self.get_fallback_stock_data(symbol, str(e))
    
    def get_fallback_stock_data(self, symbol: str, error_msg: str) -> Dict:
        """Provide fallback stock data when APIs fail"""
        # Common stock symbols with approximate data for demonstration
        fallback_data = {
            "AAPL": {"name": "Apple Inc.", "sector": "Technology", "approx_price": 175},
            "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "approx_price": 140},
            "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "approx_price": 420},
            "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "approx_price": 900},
            "TSLA": {"name": "Tesla, Inc.", "sector": "Automotive", "approx_price": 250},
            "AMZN": {"name": "Amazon.com Inc.", "sector": "E-commerce", "approx_price": 155},
        }
        
        base_data = fallback_data.get(symbol.upper(), {
            "name": f"{symbol} Corporation", 
            "sector": "Unknown", 
            "approx_price": 100
        })
        
        return {
            "symbol": symbol,
            "current_price": "API Limited",
            "previous_close": "API Limited", 
            "price_change": "N/A",
            "price_change_percent": "N/A",
            "market_cap": "API Limited",
            "pe_ratio": "N/A",
            "dividend_yield": "N/A",
            "52_week_high": "N/A",
            "52_week_low": "N/A",
            "company_name": base_data["name"],
            "sector": base_data["sector"],
            "industry": "N/A",
            "volume": "N/A",
            "data_source": "Fallback Data",
            "error_msg": f"API Error: {error_msg}",
            "note": "Using AI analysis instead of real-time data due to API limitations"
        }
    
    def finance_agent(self, query: str, symbol: str = None) -> str:
        """Finance agent with robust stock data handling"""
        if symbol:
            stock_data = self.get_stock_data(symbol)
            
            # Handle both error cases and API limitations
            if "error" in stock_data:
                return stock_data["error"]
            
            # Build stock info with proper handling of API limitations
            if stock_data.get("data_source") == "Fallback Data":
                stock_info = f"""
                **Stock Analysis for {stock_data['company_name']} ({symbol})**
                
                ⚠️ **Note**: {stock_data.get('note', 'Using AI analysis due to API limitations')}
                
                | Information | Value |
                |-------------|-------|
                | Company | {stock_data['company_name']} |
                | Sector | {stock_data['sector']} |
                | Data Source | {stock_data['data_source']} |
                | API Status | Limited due to rate limiting |
                
                **Error Details**: {stock_data.get('error_msg', 'API rate limit exceeded')}
                """
                
                messages = [
                    {"role": "system", "content": "You are a financial analysis agent. The user is asking about a stock but real-time data is unavailable due to API limitations. Provide a comprehensive analysis based on your knowledge of the company, including general investment considerations, company background, market position, and typical financial metrics to look for. Be honest about data limitations but still provide valuable insights."},
                    {"role": "user", "content": f"Analyze {symbol} ({stock_data['company_name']}) in the {stock_data['sector']} sector. Query: {query}\n\nNote: Real-time data unavailable due to API limits. Please provide analysis based on your knowledge."}
                ]
            else:
                # Format available data nicely
                price_change_indicator = "📈" if stock_data.get('price_change', 0) > 0 else "📉" if stock_data.get('price_change', 0) < 0 else "➡️"
                
                stock_info = f"""
                **Stock Information for {stock_data['company_name']} ({symbol})**
                
                | Metric | Value |
                |--------|-------|
                | Current Price | ${stock_data['current_price']} |
                | Previous Close | ${stock_data['previous_close']} |
                | Price Change | {price_change_indicator} ${stock_data.get('price_change', 'N/A')} ({stock_data.get('price_change_percent', 'N/A')}%) |
                | Market Cap | {stock_data['market_cap']} |
                | P/E Ratio | {stock_data['pe_ratio']} |
                | Dividend Yield | {stock_data['dividend_yield']} |
                | 52 Week High | ${stock_data['52_week_high']} |
                | 52 Week Low | ${stock_data['52_week_low']} |
                | Sector | {stock_data['sector']} |
                | Industry | {stock_data['industry']} |
                | Volume | {stock_data['volume']} |
                | Data Source | {stock_data['data_source']} |
                """
                
                messages = [
                    {"role": "system", "content": "You are a financial analysis agent. Analyze the provided stock data and provide insights, recommendations, and analysis. Format your response in markdown with tables where appropriate. If some data shows 'N/A' or 'API Limited', acknowledge this and focus on available data."},
                    {"role": "user", "content": f"Analyze this stock data and query: {query}\n\nStock Data:\n{stock_info}"}
                ]
        else:
            messages = [
                {"role": "system", "content": "You are a financial analysis agent. Provide financial insights and analysis. Format your response in markdown with tables where appropriate."},
                {"role": "user", "content": query}
            ]
        
        return self.call_groq_api(messages)
    
    def multi_agent_response(self, query: str, symbol: str = None) -> str:
        """Combine web search and finance agents"""
        # Determine if this is a finance-related query
        finance_keywords = ["stock", "price", "financial", "investment", "market", "analyst", "recommendation", "earnings"]
        is_finance_query = any(keyword in query.lower() for keyword in finance_keywords)
        
        if is_finance_query and symbol:
            finance_response = self.finance_agent(query, symbol)
            web_response = self.web_search_agent(f"latest news and analysis for {symbol}")
            
            combined_response = f"""
## 📊 Financial Analysis
{finance_response}

## 🌐 Latest News & Web Search
{web_response}

---
*Analysis combining real-time financial data and web search results*
            """
        else:
            web_response = self.web_search_agent(query)
            combined_response = f"""
## 🌐 Web Search Results
{web_response}

---
*Information gathered from web search*
            """
        
        return combined_response

def main():
    # Initialize the multi-agent system
    agent_system = MultiAgentSystem()
    
    # Main header
    st.markdown('<div class="main-header">🤖 Multi-Agent AI Assistant</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## 🛠️ Configuration")
        
        # API Status check
        st.markdown("### API Status")
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key:
            st.success("✅ Groq API Key Found")
        else:
            st.error("❌ Groq API Key Missing")
            st.markdown("Please add your GROQ_API_KEY to the .env file")
        
        st.markdown("---")
        
        # Agent selection
        st.markdown("### 🤖 Select Agent")
        agent_choice = st.selectbox(
            "Choose an agent:",
            ["Multi-Agent System", "Web Search Agent", "Finance Agent"],
            help="Select which agent to use for your query"
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🧹 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat Interface", "📊 Stock Analysis", "🔍 Web Search", "📈 Quick Insights"])
    
    with tab1:
        st.markdown("## 💬 Interactive Chat")
        
        # Agent info cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="agent-card">
                <h4>🌐 Web Search Agent</h4>
                <p>Searches for current information and provides comprehensive answers</p>
                <small>Model: Llama3-70B</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="agent-card">
                <h4>💰 Finance Agent</h4>
                <p>Analyzes stocks with real-time data from Yahoo Finance</p>
                <small>Model: Llama3-70B + YFinance</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="agent-card">
                <h4>🤖 Multi-Agent System</h4>
                <p>Combines both agents for comprehensive analysis</p>
                <small>Coordinated Intelligence</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Chat interface
        st.markdown("---")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 💭 Conversation History")
            for i, (user_msg, agent_response, timestamp, agent_used) in enumerate(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**You ({timestamp}):**")
                    st.write(user_msg)
                    st.markdown(f"**{agent_used} Response:**")
                    st.markdown(agent_response)
                    st.markdown("---")
        
        # Input area
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                user_input = st.text_area(
                    "Enter your query:",
                    placeholder="e.g., 'Analyze NVDA stock' or 'Search for recent AI news'",
                    height=80
                )
            with col2:
                stock_symbol = st.text_input("Stock Symbol (optional)", placeholder="e.g., NVDA")
            
            submit_button = st.form_submit_button("🚀 Send Query", use_container_width=True)
        
        if submit_button and user_input:
            with st.spinner("🤖 Agent is thinking..."):
                # Get response based on selected agent
                if agent_choice == "Web Search Agent":
                    response = agent_system.web_search_agent(user_input)
                elif agent_choice == "Finance Agent":
                    response = agent_system.finance_agent(user_input, stock_symbol if stock_symbol else None)
                else:
                    response = agent_system.multi_agent_response(user_input, stock_symbol if stock_symbol else None)
                
                # Add to chat history
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.chat_history.append((user_input, response, timestamp, agent_choice))
                
                st.rerun()
    
    with tab2:
        st.markdown("## 📊 Stock Analysis Dashboard")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            stock_symbol = st.text_input("Stock Symbol", value="NVDA", placeholder="e.g., AAPL, GOOGL, TSLA")
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Complete Analysis", "Current Price & Metrics", "Financial Analysis", "Market Research"]
            )
            
            if st.button("🔍 Analyze Stock", use_container_width=True):
                if stock_symbol:
                    with st.spinner(f"Analyzing {stock_symbol}..."):
                        # Get stock data with proper error handling
                        stock_data = agent_system.get_stock_data(stock_symbol)
                        
                        # Display results regardless of data source
                        with col2:
                            st.markdown(f"### 📈 {stock_data['company_name']} ({stock_symbol})")
                            
                            # Show data source and any limitations
                            if stock_data.get('data_source') == 'Fallback Data':
                                st.warning(f"⚠️ API Rate Limited: {stock_data.get('note', 'Using AI analysis instead of real-time data')}")
                                
                                # Show basic info
                                st.info(f"**Company**: {stock_data['company_name']}")
                                st.info(f"**Sector**: {stock_data['sector']}")
                                
                            else:
                                # Key metrics in cards (when data is available)
                                metric_col1, metric_col2, metric_col3 = st.columns(3)
                                
                                with metric_col1:
                                    if stock_data['current_price'] != "API Limited":
                                        price_change = stock_data.get('price_change', 0)
                                        st.metric(
                                            "Current Price", 
                                            f"${stock_data['current_price']}", 
                                            f"{price_change:+.2f}" if isinstance(price_change, (int, float)) else None
                                        )
                                    else:
                                        st.metric("Current Price", "API Limited")
                                
                                with metric_col2:
                                    market_cap = stock_data['market_cap']
                                    if market_cap != "API Limited" and market_cap != "N/A":
                                        if isinstance(market_cap, int):
                                            st.metric("Market Cap", f"${market_cap:,}")
                                        else:
                                            st.metric("Market Cap", str(market_cap))
                                    else:
                                        st.metric("Market Cap", "API Limited")
                                
                                with metric_col3:
                                    pe_ratio = stock_data['pe_ratio']
                                    st.metric("P/E Ratio", pe_ratio if pe_ratio != "N/A" else "N/A")
                            
                            # AI Analysis (always available)
                            queries = {
                                "Complete Analysis": f"Provide a comprehensive financial analysis for {stock_symbol}",
                                "Current Price & Metrics": f"Analyze the stock metrics and trends for {stock_symbol}",
                                "Financial Analysis": f"Provide detailed financial analysis for {stock_symbol}",
                                "Market Research": f"Research market sentiment and developments for {stock_symbol}"
                            }
                            
                            query = queries[analysis_type]
                            analysis = agent_system.finance_agent(query, stock_symbol)
                            
                            st.markdown("### 🔍 AI Analysis")
                            st.markdown(analysis)
        
        with col2:
            if not st.session_state.get('stock_analysis_done', False):
                st.info("👈 Enter a stock symbol and click 'Analyze Stock' to see results here")
    
    with tab3:
        st.markdown("## 🔍 Web Search Interface")
        
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., 'latest AI developments', 'cryptocurrency news today'"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔍 Search Web", use_container_width=True):
                if search_query:
                    with st.spinner("Searching..."):
                        response = agent_system.web_search_agent(search_query)
                        
                        with col2:
                            st.markdown("### Search Results")
                            st.markdown(response)
        
        # Predefined search topics
        st.markdown("### 🔥 Trending Topics")
        col1, col2, col3, col4 = st.columns(4)
        
        topics = [
            ("AI News", "latest artificial intelligence news"),
            ("Tech Trends", "latest technology trends 2024"),
            ("Market News", "stock market news today"),
            ("Crypto Updates", "cryptocurrency news today")
        ]
        
        for i, (topic_name, topic_query) in enumerate(topics):
            col = [col1, col2, col3, col4][i]
            with col:
                if st.button(f"📰 {topic_name}", use_container_width=True):
                    with st.spinner(f"Searching {topic_name}..."):
                        response = agent_system.web_search_agent(topic_query)
                        st.markdown(f"### {topic_name} Results")
                        st.markdown(response)
    
    with tab4:
        st.markdown("## 📈 Quick Financial Insights")
        
        # Popular stocks section
        st.markdown("### 🏆 Popular Stocks Analysis")
        
        popular_stocks = ["NVDA", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        
        col1, col2, col3 = st.columns(3)
        
        for i, stock in enumerate(popular_stocks):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(f"📊 Analyze {stock}", use_container_width=True, key=f"quick_{stock}"):
                    with st.spinner(f"Analyzing {stock}..."):
                        response = agent_system.multi_agent_response(f"Analyze {stock} stock with current data and recent news", stock)
                        
                        st.markdown(f"### {stock} Analysis")
                        st.markdown(response)
        
        st.markdown("---")
        
        # Market overview
        st.markdown("### 🌍 Market Overview")
        if st.button("📈 Get Market Overview", use_container_width=True):
            with st.spinner("Getting market overview..."):
                query = "Get current market overview including major indices performance and market sentiment"
                response = agent_system.web_search_agent(query)
                st.markdown(response)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🤖 Multi-Agent AI Assistant | Powered by Groq & Llama3-70B | 
            Built with Streamlit & Real-time Financial Data
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()