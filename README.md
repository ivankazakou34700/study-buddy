# Study Buddy

Study Buddy is an interactive educational assistant built with Streamlit and LangChain that helps users:

- Analyze and summarize text  
- Define complex terms  
- Compare concepts  
- Generate quizzes  
- Fetch information from Wikipedia  
- Ask questions about uploaded PDF documents (via RAG)

## Features

- Multi-Agent System (MAS): Classifies user intent and routes to the correct tool  
- RAG (Retrieval-Augmented Generation): Lets users ask questions about content inside PDF files  
- Wikipedia Tool: Sends queries to a local Wikipedia API and returns summaries  
- Streamlit Interface: Intuitive frontend for seamless interactions

## Setup

 1. Clone the repository

```bash
git clone https://github.com/ivankazakou34700/study-buddy.git
cd study-buddy

2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Add environment variables

Create a .env file with your keys

OPENAI_API_KEY=your_openai_key_here  
LANGSMITH_API_KEY=your_langsmith_key_here

5. Run the MCP Server
uvicorn mcp_server:app --reload


6. Run the app

streamlit run app.py


