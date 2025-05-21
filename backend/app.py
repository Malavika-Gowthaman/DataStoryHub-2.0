import streamlit as st
import time
from modules.vanna_helper import prompt_from_template, vn
# from modules.base import VannaBase, vn
from modules.db_selector import determine_database
import uuid

# Apply custom UI styles
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #1e293b;
        }
        .sidebar .sidebar-content {
            width: 300px;
        }
        .chat-history-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .chat-history-item:hover {
            background-color: #334155;
        }
        .chat-history-item.active {
            background-color: #4db8ff;
            color: white;
        }
        .stTextInput textarea {
            color: white !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.current_conversation = str(uuid.uuid4())
    st.session_state.conversations[st.session_state.current_conversation] = {
        "title": "New conversation",
        "messages": [],
        "context": ""
    }

if "input_key" not in st.session_state:
    st.session_state.input_key = str(uuid.uuid4())

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")
    
    # Button to start new conversation
    if st.button("+ New chat", use_container_width=True):
        new_convo_id = str(uuid.uuid4())
        st.session_state.current_conversation = new_convo_id
        st.session_state.conversations[new_convo_id] = {
            "title": "New conversation",
            "messages": [],
            "context": ""
        }
        st.session_state.input_key = str(uuid.uuid4())
        st.rerun()
    
    st.divider()
    
    # Display conversation history
    for convo_id in list(st.session_state.conversations.keys())[::-1]:
        convo = st.session_state.conversations[convo_id]
        is_active = convo_id == st.session_state.current_conversation
        emoji = "🗨️" if is_active else "💬"
        title = convo["title"]
        
        if st.button(
            f"{emoji} {title}",
            key=f"convo_{convo_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_conversation = convo_id
            st.session_state.input_key = str(uuid.uuid4())
            st.rerun()

# Main chat area
current_convo = st.session_state.conversations[st.session_state.current_conversation]

st.title("DataStoryHub 2.0")

# Display chat messages
for message in current_convo["messages"]:
    with st.chat_message(message["role"]):
        if "sql_query" in message:
            st.markdown("**Generated SQL Query:**")
            st.code(message["sql_query"], language="sql")
            if "results" in message and not message["results"].empty:
                st.markdown("**Query Results:**")
                st.dataframe(message["results"])
            st.markdown(f"**Execution Time:** {message['time']:.2f} seconds")
            st.markdown(f"**Summary:**\n{message['summary']}")
            if message["followup_questions"]:
                st.markdown("**Follow-up Questions:**")
                for q in message["followup_questions"]:
                    st.markdown(f"- {q}")
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your data...", key=st.session_state.input_key):
    # Add user message to chat history
    current_convo["messages"].append({"role": "user", "content": prompt})
    
    # Update conversation title if first message
    if len(current_convo["messages"]) == 1:
        current_convo["title"] = prompt[:30] + ("..." if len(prompt) > 30 else "")
    
    # Build context from previous messages
    def build_context(messages):
        context = []
        for msg in messages[-6:]:  # Use last 6 messages for context (3 exchanges)
        # for msg in messages:  # Use last 6 messages for context (3 exchanges)
            if msg["role"] == "user":
                context.append(f"User: {msg['content']}")
            else:
                if "summary" in msg:
                    context.append(f"Assistant: {msg['summary']}")
                else:
                    context.append(f"Assistant: {msg['content']}")
        return "\n".join(context)
    
    context = build_context(current_convo["messages"])
    current_convo["context"] = context
    
    database_option = determine_database(prompt, context)
    
    # Generate assistant response with full context
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()
            
            # Include context in the question
            contextual_question = f"Context:\n{context}\n\nQuestion: {prompt}"
            sql_query, result_df = prompt_from_template(database_option, contextual_question)
            
            execution_time = time.time() - start_time
            
            summary = vn.generate_summary(prompt, result_df)
            followup_qs = vn.generate_followup_questions(prompt, sql_query, result_df, n_questions=3)
            
            # Display response
            st.markdown("**Generated SQL Query:**")
            st.code(sql_query, language="sql")
            
            if not result_df.empty:
                st.markdown("**Query Results:**")
                st.dataframe(result_df)
            else:
                st.warning("No results found.")
            
            st.markdown(f"**Execution Time:** {execution_time:.2f} seconds")
            st.markdown(f"**Summary:**\n{summary}")
            
            if followup_qs:
                st.markdown("**Follow-up Questions:**")
                for q in followup_qs:
                    st.markdown(f"- {q}")
    
    # Add assistant response to chat history
    current_convo["messages"].append({
        "role": "assistant",
        "content": f"Answered question about {database_option} data",
        "sql_query": sql_query,
        "results": result_df,
        "time": execution_time,
        "summary": summary,
        "followup_questions": followup_qs
    })
    
    # Rerun to update the display
    st.rerun()