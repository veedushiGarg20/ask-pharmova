import streamlit as st
from dotenv import load_dotenv
from config import BOT_NAME, BOT_TAGLINE, REDIRECT_MESSAGE, TOPIC_CHANGE_MESSAGE
from pipeline.classifier import check_topic_relevance
from pipeline.generator import generate
from pipeline.orchestrator import run_agentic_rag 
from utils.citation_utils import render_citations

load_dotenv()

st.set_page_config(page_title=BOT_NAME, page_icon="🏥")

with st.sidebar:
    st.title("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.context_block = ""
        st.session_state.source_map = {}
        st.session_state.original_query = ""
        st.rerun()

st.title(f"🏥 {BOT_NAME}")
st.caption(BOT_TAGLINE)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_block" not in st.session_state:
    st.session_state.context_block = ""
if "source_map" not in st.session_state:
    st.session_state.source_map = {}
if "original_query" not in st.session_state:
    st.session_state.original_query = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""

        with st.status("Initializing Agentic Clinical Pipeline...", expanded=True) as status:
            
            if st.session_state.original_query == "":
                agent_stream = run_agentic_rag(prompt, max_loops=2)
                
                final_state = None
                for update in agent_stream:
                    status.update(label=f"{update['message']}")
                    
                    print(f"[Orchestrator Stream]: {update['message']}")
                    
                    final_state = update["state"]

                if final_state["redirect"]:
                    response_text = REDIRECT_MESSAGE
                    status.update(label="Policy Violation Detected.", state="error")
                else:
                    st.session_state.context_block = final_state["context_block"]
                    st.session_state.source_map = final_state["source_map"]
                    st.session_state.original_query = prompt
                    
                    status.update(label="Synthesizing clinical response...")
                    raw_response, source_map = generate(
                        query=prompt,
                        context_block=st.session_state.context_block,
                        source_map=st.session_state.source_map
                    )
                    response_text = render_citations(raw_response, source_map)
                    status.update(label="Response Synthesized completely.", state="complete", expanded=False)
            
            else:
                status.update(label="Checking follow-up conversation relevance...")
                is_relevant = check_topic_relevance(prompt, st.session_state.original_query)
                
                if not is_relevant:
                    response_text = TOPIC_CHANGE_MESSAGE
                    status.update(label="New medical topic detected.", state="complete", expanded=False)
                else:
                    status.update(label="Generating grounded follow-up answer...")
                    
                    raw_response, source_map = generate(
                        query=prompt,
                        context_block=st.session_state.context_block,
                        source_map=st.session_state.source_map,
                        conversation_history=st.session_state.messages
                    )
                    response_text = render_citations(raw_response, st.session_state.source_map)
                    status.update(label="Follow-up completed.", state="complete", expanded=False)

        st.markdown(response_text, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response_text})