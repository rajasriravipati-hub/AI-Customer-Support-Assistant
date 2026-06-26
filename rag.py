import streamlit as st
import os
from dotenv import load_dotenv

from utils.pdf_loader import extract_pdf_text
from utils.faq_loader import load_faqs
from utils.text_splitter import split_text
from utils.embeddings import embedding_model
from utils.vector_store import vector_store
from utils.analytics import analytics

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================
# SESSION STATE
# ==========================================

default_states = {
    "knowledge_base_ready": False,
    "documents_uploaded": 0,
    "faqs_uploaded": 0,
    "chat_history": [],
    "vector_created": False,
    "sample_question": ""
}

for key, value in default_states.items():

    if key not in st.session_state:

        st.session_state[key] = value
if "chunks" not in st.session_state:
    st.session_state.chunks=[]

# ==========================================
# HEADER
# ==========================================

st.title("🤖 AI Customer Support Assistant")

st.caption(
    "Enterprise Knowledge Support Platform"
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📊 Dashboard")

    st.success("🟢 System Active")

    st.metric(
        "Documents",
        st.session_state.documents_uploaded
    )

    st.metric(
        "Questions",
        len(st.session_state.chat_history)
    )

    st.markdown("---")

    page = st.radio(
        "📂 Navigation",
        [
            "🏠 Home",
            "📚 Knowledge Center",
            "💬 AI Assistant",
            "📊 Insights",
            "📄 Reports"
        ]
    )

    st.markdown("---")



# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":


    st.write("""
        Upload company policies, FAQs, manuals and guides.

        Build an intelligent knowledge base that helps
        customers get instant answers to common questions.
        """)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        "Documents",
        st.session_state.documents_uploaded
    )
    with col2:
        st.metric(
        "FAQs",
        st.session_state.faqs_uploaded
    )

    with col3:
        st.metric(
        "Questions",
        len(st.session_state.chat_history)
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
        "🚀 Start Chat",
        use_container_width=True
    ):
            st.info(
            "Open the AI Assistant page from the sidebar."
        )

    with col2:

        if st.button(
        "📚 Manage Knowledge Base",
        use_container_width=True
    ):
            st.info(
            "Open the Knowledge Center page from the sidebar."
        )

    st.divider()

    st.success("""
    ✓ Instant customer support

    ✓ AI knowledge retrieval

    ✓ FAQ management

    ✓ Enterprise document search

    ✓ Analytics & reporting
        """)
    st.markdown("### Platform Workflow")

    st.info("""
    Upload Documents
    → Build Knowledge Base
    → Ask Questions
    → Get AI Answers
    → View Insights
    → Download Reports
    """)

# KNOWLEDGE CENTER
# ==========================================

if page == "📚 Knowledge Center":

    st.title("📚 Knowledge Center")
    st.info(
        "Upload company policies, FAQs, manuals and guides to build your AI knowledge base.")

    st.write("""

    Upload company policies, FAQs, manuals and guides
    to build your AI knowledge base.
    """)
  


    pdf_files = st.file_uploader(
        "📄 Upload Company Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    faq_file = st.file_uploader(
        "📋 Upload FAQ CSV",
        type=["csv"]
    )

    st.divider()

    if st.button(
        "🚀 Build Knowledge Base",
        use_container_width=True
    ):

        try:

            all_text = ""

            if pdf_files:

                for pdf in pdf_files:

                    text = extract_pdf_text(pdf)

                    all_text += text + "\n"

                st.session_state.documents_uploaded = len(pdf_files)

            if faq_file:

                faq_text = load_faqs(faq_file)

                all_text += faq_text

                st.session_state.faqs_uploaded = 1

            chunks = split_text(all_text)
            st.session_state.chunks = chunks

            embeddings = embedding_model.generate_embeddings(chunks)

            vector_store.create_index(
                embeddings,
                chunks
            )

            vector_store.save_index()

            st.session_state.vector_created = True
            st.session_state.knowledge_base_ready = True

            

        except Exception as e:

            st.error(f"Error: {e}")
            answer = f"ERROR: {e}"

    st.divider()

    if st.session_state.knowledge_base_ready:

        st.success("✅ Knowledge Base Ready")

        st.markdown("### 📊 Knowledge Base Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
        "Documents",
        st.session_state.documents_uploaded
    )

        with col2:
            st.metric(
        "FAQs",
        st.session_state.faqs_uploaded
    )

        with col3:
            st.metric(
        "Chunks",
        len(st.session_state.get("chunks",[]))
    )

        st.info(
         """
        🟢 Vector Store Active

        🟢 Embeddings Generated

        🟢 FAISS Index Created
        """
        )





# ==========================================
# AI ASSISTANT
# ==========================================

if page == "💬 AI Assistant":

    st.title("💬 AI Assistant")

    st.write("""
Ask questions about company policies,
FAQs, manuals and support documents.
""")

    if not st.session_state.knowledge_base_ready:

        st.warning(
            "Please build the Knowledge Base first."
        )

    else:

        st.markdown("### Suggested Questions")

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💰 Refund Policy"):

                st.session_state.sample_question = (
                    "How can I get a refund?"
                )

            if st.button("🚚 Shipping Time"):

                st.session_state.sample_question = (
                    "How long does shipping take?"
                )

        with col2:

            if st.button("🛡 Warranty Coverage"):

                st.session_state.sample_question = (
                    "What does the warranty cover?"
                )

            if st.button("📞 Contact Support"):

                st.session_state.sample_question = (
                    "How can I contact support?"
                )

        question = st.text_input(
            "Ask a question...",
            value=st.session_state.get(
                "sample_question",
                ""
            )
        )

        ask_btn = st.button(
            "🚀 Get Answer",
            use_container_width=True
        )

        if ask_btn:

            if question.strip() == "":

                st.warning(
                    "Please enter a question."
                )

            else:

                try:

                    from utils.chatbot import CustomerSupportBot

                    bot = CustomerSupportBot(
                        GROQ_API_KEY
                    )


                    answer = ""
                    try:

                        answer = bot.generate_answer(
                            question,
                            vector_store
                        )

                        

                    except Exception as e:
                        st.error(f"Error:(e)")
                        

        
                    if 'answer' in locals() and answer.strip() == "":

                            answer = (
                                "Information not found in the knowledge base."
                            )

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )

        st.divider()

        if len(st.session_state.chat_history) > 0:

            st.subheader("Conversation")

            for item in st.session_state.chat_history:

                with st.chat_message("user"):

                    st.write(
                        item["question"]
                    )

                with st.chat_message("assistant"):

                    st.write(
                        item["answer"]
                    )

        
# ==========================================
# INSIGHTS
# ==========================================

if page == "📊 Insights":

    st.title("📊 Insights")

    st.write("""
Understand customer interactions and
identify common support topics.
""")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Documents",
            st.session_state.documents_uploaded
        )

    with col2:
        st.metric(
            "FAQs",
            st.session_state.faqs_uploaded
        )

    with col3:
        st.metric(
            "Questions",
            len(st.session_state.chat_history)
        )

    st.divider()

    if len(st.session_state.chat_history) > 0:

        import pandas as pd
        import plotly.express as px

        chart_df = pd.DataFrame(
            {
                "Metric": [
                    "Documents",
                    "FAQs",
                    "Questions"
                ],
                "Count": [
                    st.session_state.documents_uploaded,
                    st.session_state.faqs_uploaded,
                    len(st.session_state.chat_history)
                ]
            }
        )

        fig = px.bar(
            chart_df,
            x="Metric",
            y="Count",
            title="System Usage Overview"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            "### 📝 Recent Customer Questions"
        )

        for item in reversed(
            st.session_state.chat_history[-5:]
        ):

            st.write(
                f"• {item['question']}"
            )

    else:

        st.info(
            "No analytics available yet."
        )

# ==========================================
# REPORTS
# ==========================================

if page == "📄 Reports":

    st.header("📄 Reports")

    st.success(
        "✅ Support Report Ready"
    )

    chat_report = ""

    for item in st.session_state.chat_history:

        chat_report += f"""

QUESTION:
{item['question']}

ANSWER:
{item['answer']}

----------------------------------------
"""

    report = f"""
AI CUSTOMER SUPPORT ASSISTANT
================================

DOCUMENTS:
{st.session_state.documents_uploaded}

FAQ FILES:
{st.session_state.faqs_uploaded}

TOTAL QUESTIONS:
{len(st.session_state.chat_history)}

================================
CHAT HISTORY
================================

{chat_report}
"""

    st.download_button(
        label="📥 Download Support Report",
        data=report,
        file_name="Customer_Support_Report.md",
        mime="text/plain",
        use_container_width=True
    )

    st.text_area(
        "Report Preview",
        report,
        height=400
    )
# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Powered by RAG Architecture • FAISS • Groq L1ama3 • Streamlit"
)




