import streamlit as st
import openai
from phi.agent import Agent
import phi.api
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-AI Agent Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize agents
@st.cache_resource
def initialize_agents():
    # Web search agent
    web_search_engine = Agent(
        name="Web Search Agent",
        role="Search the web for the information",
        model=Groq(id='Llama3-70b-8192'),
        tools=[DuckDuckGo()],
        instructions=['Always include sources'],
        show_tool_calls=True,
        markdown=True
    )
    
    # Financial agent
    finance_agent = Agent(
        name="Finance AI Agent",
        model=Groq(id="Llama3-70b-8192"),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                stock_fundamentals=True,
                company_news=True
            )
        ],
        instructions=['Use tables to display the data'],
        show_tool_calls=True,
        markdown=True
    )
    
    # Multi-agent system
    multi_ai_agent = Agent(
        model=Groq(id="Llama3-70b-8192"),
        team=[web_search_engine, finance_agent],
        instructions=['Always include sources', 'Use tables to display the data'],
        show_tool_calls=True,
        markdown=True,
    )
    
    return web_search_engine, finance_agent, multi_ai_agent

# Main UI
def main():
    st.title("🤖 Multi-AI Agent Assistant")
    st.markdown("---")
    
    # Initialize agents
    try:
        web_agent, finance_agent, multi_agent = initialize_agents()
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        st.stop()
    
    # Sidebar for agent selection
    st.sidebar.title("Agent Selection")
    agent_choice = st.sidebar.selectbox(
        "Choose an agent:",
        ["Multi-Agent System", "Web Search Agent", "Finance Agent"]
    )
    
    # Agent descriptions
    agent_descriptions = {
        "Multi-Agent System": "Combines web search and financial analysis capabilities",
        "Web Search Agent": "Searches the web for general information",
        "Finance Agent": "Provides financial data, stock analysis, and market insights"
    }
    
    st.sidebar.markdown(f"**Description:** {agent_descriptions[agent_choice]}")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Chat with {agent_choice}")
        
        # Chat input
        user_query = st.text_area(
            "Enter your query:",
            placeholder="e.g., Get the latest analyst recommendations for NVDA",
            height=100
        )
        
        # Predefined queries for quick access
        st.subheader("Quick Queries")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📈 NVDA Stock Analysis"):
                user_query = "Get the latest analyst recommendations and stock price for NVDA"
            if st.button("📰 Tesla News"):
                user_query = "Get the most recent news about Tesla (TSLA)"
        
        with col_b:
            if st.button("🔍 Market Trends"):
                user_query = "Search for the latest stock market trends and analysis"
            if st.button("💰 Apple Fundamentals"):
                user_query = "Get fundamental analysis for Apple (AAPL) stock"
        
        # Submit button
        if st.button("🚀 Submit Query", type="primary"):
            if user_query.strip():
                process_query(user_query, agent_choice, web_agent, finance_agent, multi_agent)
            else:
                st.warning("Please enter a query before submitting.")
    
    with col2:
        st.subheader("Agent Capabilities")
        
        if agent_choice == "Multi-Agent System":
            st.markdown("""
            **🔧 Tools Available:**
            - 🌐 Web Search (DuckDuckGo)
            - 📊 Financial Data (Yahoo Finance)
            - 📈 Stock Prices & Analysis
            - 📰 Company News
            - 💹 Analyst Recommendations
            """)
        elif agent_choice == "Web Search Agent":
            st.markdown("""
            **🔧 Tools Available:**
            - 🌐 Web Search (DuckDuckGo)
            - 📄 Source Citations
            - 🔍 General Information Retrieval
            """)
        else:  # Finance Agent
            st.markdown("""
            **🔧 Tools Available:**
            - 📊 Stock Prices
            - 📈 Analyst Recommendations
            - 📋 Company Fundamentals
            - 📰 Financial News
            - 💹 Market Data
            """)

def process_query(query, agent_choice, web_agent, finance_agent, multi_agent):
    """Process the user query with the selected agent"""
    
    with st.spinner(f"Processing your query with {agent_choice}..."):
        try:
            # Select the appropriate agent
            if agent_choice == "Multi-Agent System":
                selected_agent = multi_agent
            elif agent_choice == "Web Search Agent":
                selected_agent = web_agent
            else:
                selected_agent = finance_agent
            
            # Create a container for the response
            response_container = st.container()
            
            with response_container:
                st.subheader("🤖 Agent Response")
                
                # Create a placeholder for streaming response
                response_placeholder = st.empty()
                
                # Capture the response
                response_text = ""
                
                # Since we can't easily capture the streamed output, 
                # we'll use a different approach
                with st.expander("View Response", expanded=True):
                    try:
                        # Get response without streaming for display
                        response = selected_agent.run(query)
                        if hasattr(response, 'content'):
                            st.markdown(response.content)
                        else:
                            st.markdown(str(response))
                    except Exception as e:
                        st.error(f"Error getting response: {str(e)}")
                        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.markdown("Please check your API keys and internet connection.")

# Session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Add chat history section
def display_chat_history():
    if st.session_state.chat_history:
        st.subheader("💬 Chat History")
        for i, (query, response) in enumerate(st.session_state.chat_history[-5:]):  # Show last 5
            with st.expander(f"Query {i+1}: {query[:50]}..."):
                st.markdown(f"**Query:** {query}")
                st.markdown(f"**Response:** {response}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("*Powered by Phi Framework & Groq*")

if __name__ == "__main__":
    main()