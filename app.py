import streamlit as st
from dotenv import load_dotenv
from config import BOT_NAME, BOT_TAGLINE, REDIRECT_MESSAGE, TOPIC_CHANGE_MESSAGE
from pipeline.classifier import classify_query
from pipeline.classifier import check_topic_relevance
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from pipeline.assembler import assemble_context
from pipeline.generator import generate
from pipeline.generator import generate_followup
from utils.citation_utils import render_citations

load_dotenv()

st.set_page_config(page_title=BOT_NAME, page_icon="🏥")

# Sidebar
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.context_block = ""
        st.session_state.source_map = {}
        st.session_state.original_query = ""
        st.rerun()

# Main area
st.title(f"🏥 {BOT_NAME}")
st.caption(BOT_TAGLINE)

# Initialise session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_block" not in st.session_state:
    st.session_state.context_block = ""
if "source_map" not in st.session_state:
    st.session_state.source_map = {}
if "original_query" not in st.session_state:
    st.session_state.original_query = ""

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a medical question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Fetching the best information..."):
            print("Classifying query...")
            is_medical = classify_query(prompt)

            if not is_medical:
                print("[Oops!]Query found not medically relevant! Returning redirect message...")
                response_text = REDIRECT_MESSAGE
            elif st.session_state.original_query == "":
                # first query -- full pipline
                print("Reformulating query for search...")
                reformulated = reformulate_query(prompt)
                print("Searching trusted medical sources...")
                results = retrieve(reformulated)
                context_block, source_map = assemble_context(results)
                print("Generating grounded response...")
                raw_response, source_map = generate(prompt, context_block, source_map)
                response_text = render_citations(raw_response, source_map)
                
                # store in session_state
                st.session_state.context_block = context_block
                st.session_state.source_map = source_map
                st.session_state.original_query = prompt
            else:
                # follow-up query
                print("Checking topic relevance...")
                is_relevant = check_topic_relevance(prompt, st.session_state.original_query)
                if not is_relevant:
                    print("[Oops!]Topic change detected! Returning topic change message...")
                    response_text = TOPIC_CHANGE_MESSAGE
                else:
                    print("Generating follow-up response...")
                    raw_response, source_map = generate_followup(
                        prompt,
                        st.session_state.context_block,
                        st.session_state.source_map,
                        st.session_state.messages
                    )
                    response_text = render_citations(raw_response, st.session_state.source_map)

        st.markdown(response_text, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response_text})