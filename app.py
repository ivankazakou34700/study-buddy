import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langsmith import Client
from langchain_core.tracers.context import tracing_v2_enabled
from rag_utils import extract_text_from_pdf, get_qa_chain
from agents import plan_task, agent_map

load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

api_key = os.getenv("OPENAI_API_KEY")

st.title("🧠 Study Buddy")
st.write("Paste your text below, and I’ll analyze it for you.")

user_input = st.text_area("Enter text here:", height=300)
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Analyze Text"):
    if user_input.strip() == "":
        st.warning("Please paste some text.")
    else:
        try:
            with tracing_v2_enabled():
                with st.spinner("Analyzing..."):
                    task = plan_task(user_input, api_key).lstrip("- ").strip()
                    st.write(f"🧠 Detected task: {task}")  
                    result = agent_map.get(task)
                    if result:
                        output = result(user_input, api_key)
                        st.success("Done!")
                        st.subheader(f"Task: {task.capitalize()}")
                        st.markdown(output)
                    else:
                        st.error(f"Unsupported task: {task}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# result = agent_map.get(task)
# if result:
#     output = result(user_input, api_key)
#     st.success("Done!")
#     st.subheader(f"Task: {task.capitalize()}")
#     st.markdown(output)
# else:
#     st.error(f"Unsupported task: {task}")


                    # if task == "lookup":
                    #     response = requests.get("http://localhost:8000/wikipedia", params={"query": user_input})
                    #     if response.status_code == 200:
                    #         data = response.json()
                    #         summary = data.get("summary", "No summary available.")
                    #         url = data.get("url", "#")
                    #         st.success("Wikipedia summary fetched successfully!")
                    #         st.subheader(f"Task: {task.capitalize()}")
                    #         st.markdown(f"**[{data['title']}]({url})**")
                    #         st.write(summary)
                    #     else:
                    #         st.error(f"Wikipedia tool error: {response.json().get('error')}")
                    # elif task in agent_map:
                    #     result = agent_map[task](user_input, api_key)
                    #     st.success("Done!")
                    #     st.subheader(f"Task: {task.capitalize()}")
                    #     st.write(result)
                    # else:
                    #     st.error(f"Unsupported task: {task}")

        # except Exception as e:
        #     st.error(f"Something went wrong: {e}")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.text_area("📄 Extracted PDF Text", pdf_text, height=300)

    if st.button("Ask a question about the PDF"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Answering with RAG..."):
                    qa_chain = get_qa_chain(pdf_text, api_key)
                    answer = qa_chain.run(user_input)
                    st.success(answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
