# 🤖 Multi-Agent AI Assistant

A Streamlit-powered multi-agent AI system that combines web search and financial analysis capabilities using open-source tools. Built with PhiData framework and Groq's LLaMA models for lightning-fast responses without breaking the bank!
![image](https://github.com/user-attachments/assets/10722a1d-8472-40c1-8567-c95d20528c8d)

## ✨ Features

- **Multi-Agent Collaboration**: Three specialized AI agents working together
- **Real-time Stock Analysis**: Get live stock prices, analyst recommendations, and fundamentals
- **Web Search Integration**: Search for current news and information
- **Natural Language Queries**: Ask questions in plain English
- **Interactive UI**: Clean Streamlit interface with quick-action buttons
- **Budget-Friendly**: Uses free/open-source APIs (Groq, YFinance, DuckDuckGo)

## 🏗️ Architecture

### AI Agents
1. **🌐 Web Search Agent**
   - Powered by DuckDuckGo API
   - Searches for real-time information
   - Always includes sources

2. **📊 Finance Agent**
   - Integrated with Yahoo Finance
   - Provides stock prices, fundamentals, analyst recommendations
   - Company news and market data

3. **🧠 Multi-Agent Coordinator**
   - Orchestrates agent collaboration
   - Routes queries to appropriate agents
   - Combines results for comprehensive responses

## 🛠️ Tech Stack

- **Framework**: [PhiData](https://docs.phidata.com/) for agent orchestration
- **LLM**: Groq's LLaMA3-70B-8192 (free tier)
- **Frontend**: Streamlit for web interface
- **APIs**: 
  - Yahoo Finance (stock data)
  - DuckDuckGo (web search)
- **Language**: Python 3.8+

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key (free at [groq.com](https://groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-ai-assistant.git
   cd multi-agent-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📦 Project Structure

```
multi-agent-ai-assistant/
├── simple_streamlit.py     # Main Streamlit application
├── Financial_Agent.py     # python code without UI
├── playground.py          # integrating with phidata
├── streamlit.py           # enhanced version of simple_streamlit.py using better AI prompting
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 📋 Dependencies

Create a `requirements.txt` file with these dependencies:

```
streamlit
phidata
groq
yfinance
duckduckgo-search
python-dotenv
openai
```

## 🎯 Usage Examples

### Stock Analysis Queries
```python
# Examples of what you can ask:
"Get the latest analyst recommendations for NVDA"
"What's Tesla's stock price and recent news?"
"Show me Apple's fundamental analysis"
"Compare Microsoft and Google stock performance"
```

### Web Search Queries
```python
# Examples of web search capabilities:
"Search for recent AI industry trends"
"What's happening with cryptocurrency today?"
"Latest news about electric vehicles"
"Recent developments in quantum computing"
```

### Combined Queries
```python
# Multi-agent collaboration examples:
"Get NVIDIA's stock data and recent AI chip news"
"Tesla's financial performance and EV market trends"
"Apple's stock analysis and latest product announcements"
```

## 🔧 Configuration

The system uses three main agents configured as follows:

```python
# Web Search Agent
web_search_engine = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id='Llama3-70b-8192'),
    tools=[DuckDuckGo()],
    instructions=['Always include sources'],
    show_tool_calls=True,
    markdown=True
)

# Finance Agent
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

# Multi-Agent System
multi_ai_agent = Agent(
    model=Groq(id="Llama3-70b-8192"),
    team=[web_search_engine, finance_agent],
    instructions=['Always include sources', 'Use tables to display the data'],
    show_tool_calls=True,
    markdown=True,
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Groq API Key Error**
   ```bash
   Error: Invalid API key
   Solution: Check your .env file and ensure GROQ_API_KEY is set correctly
   ```

2. **Module Not Found**
   ```bash
   Error: No module named 'phi'
   Solution: Install dependencies with pip install -r requirements.txt
   ```

3. **Streamlit Connection Error**
   ```bash
   Error: Failed to connect to localhost:8501
   Solution: Ensure no other applications are using port 8501
   ```

## 📈 Features in Detail

### Agent Capabilities

| Agent | Tools | Capabilities |
|-------|-------|-------------|
| Web Search | DuckDuckGo | Real-time web search, news, general information |
| Finance | YFinance | Stock prices, analyst recommendations, fundamentals, company news |
| Multi-Agent | Both | Coordinated responses, complex queries, data synthesis |

### Supported Stock Operations

- ✅ Real-time stock prices
- ✅ Analyst recommendations
- ✅ Company fundamentals
- ✅ Historical data
- ✅ Company news
- ✅ Market trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PhiData](https://docs.phidata.com/) for the amazing agent framework
- [Groq](https://groq.com/) for providing free LLaMA model access
- [Streamlit](https://streamlit.io/) for the easy-to-use web framework
- Open source community for making this possible

## 📞 Contact

- GitHub: [Khushi](https://github.com/kraj2003)
- LinkedIn: [Khushi](https://www.linkedin.com/in/khushi-rajpurohit-240476260/)
- Email: khushirajpurohit2021@gmail.com

---

⭐ If you found this project helpful, please give it a star!
