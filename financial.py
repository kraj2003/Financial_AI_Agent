import openai
from phi.agent import Agent
import phi.api  
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

load_dotenv()

# web search agent
web_search_engine=Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id='Llama3-70b-8192'),
    tools=[DuckDuckGo()],
    instructions=['Always include sources'],
    show_tools_calls=True,
    markdown=True
)

# financial agent
finance_agent=Agent(
    name="Finance AI Agent",
    model=Groq(id="Llama3-70b-8192"),
    tools=[
        YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True,
                       company_news=True)
    ],
    instructions=['Use tables to display the data'],
    show_tool_calls=True,
    markdown=True

)

multi_ai_agent=Agent(
    model=Groq(id="Llama3-70b-8192"),
    team=[web_search_engine,finance_agent],
    instructions=['Always include sources','Use tableto display the data'],
    show_tool_calls=True,
    markdown=True,
)
multi_ai_agent.print_response("Get the latest analyst recommendation for NVDA", stream=True)
multi_ai_agent.print_response("Get the most recent news about NVDA", stream=True)