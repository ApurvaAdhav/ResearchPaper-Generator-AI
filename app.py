import streamlit as st
import generator as gen_module
from generator import PaperGenerator
from exporter import DocumentExporter
import importlib

# Reload generator for dev
importlib.reload(gen_module)

# Page Config
st.set_page_config(
    page_title="ResearchDraft AI - NextGen",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# RESEARCHDRAFT AI - HIGH IMPACT / VIBRANT UI
# ==============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary: #4f46e5;
        --secondary: #ec4899;
        --accent: #06b6d4;
        --bg-color: #f8fafc;
        --card-bg: rgba(255, 255, 255, 0.65);
        --text-color: #0f172a;
    }


    /* --- ANIMATIONS --- */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* --- GLOBAL LAYOUT --- */
    .stApp {
        background-color: #f0f2f5;
        font-family: 'Times New Roman', serif; /* Academic feel starts here */
        color: #1a1a1a;
    }

    /* --- SIDEBAR (Deep Professional Navy) --- */
    section[data-testid="stSidebar"] {
        background-color: #001f3f; /* Navy Blue */
        border-right: 1px solid #001f3f;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #003366 !important;
        border: 1px solid #004080;
        color: white;
    }

    /* --- HERO & HEADERS --- */
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #001f3f;
        font-weight: 700;
    }
    .hero-text {
        font-family: 'Georgia', serif;
        font-size: 3rem;
        color: #001f3f;
        text-align: center;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #bfa15f; /* Gold underline */
        display: inline-block;
        padding-bottom: 10px;
    }
    
    /* --- CARDS (Minimalist White) --- */
    .glass-card {
        background: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* --- INPUTS --- */
    .stTextInput input, .stTextArea textarea {
        border-radius: 2px;
        border: 1px solid #9ca3af;
        padding: 10px;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #001f3f;
        box-shadow: 0 0 0 1px #001f3f;
    }

    /* --- BUTTONS (Gold/Navy) --- */
    button[kind="primary"] {
        background-color: #001f3f;
        color: #bfa15f; /* Gold Text */
        border: 1px solid #bfa15f;
        border-radius: 2px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s;
    }
    button[kind="primary"]:hover {
        background-color: #003366;
        color: #fff;
    }

    /* --- A4 PREVIEW (Realism) --- */
    .paper-preview {
        width: 210mm;
        min-height: 297mm;
        padding: 25mm;
        margin: 20px auto;
        background: white;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
        font-family: 'Times New Roman', serif;
        font-size: 11pt; /* Standard IEEE size */
        line-height: 1.2;
        color: #000;
        text-align: justify;
    }
    .paper-preview h1 {
        font-size: 24pt;
        text-align: center;
        margin-bottom: 10pt;
    }
    .paper-preview p {
        margin-bottom: 10pt;
    }


    /* --- A4 PAPER FORMAT (STRICT) --- */
    .paper-preview {
        width: 210mm;
        min-height: 297mm;
        padding: 25mm; /* 2.5cm Margin */
        margin: 40px auto;
        background: #ffffff;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1), 0 0 5px rgba(0,0,0,0.05); /* Realistic Paper Drop Shadow */
        border: none;
        
        /* Typography for Paper */
        font-family: 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.5;
        color: #000;
        text-align: justify;
    }
    .paper-preview h1 {
        font-family: 'Times New Roman', serif;
        font-size: 24pt;
        text-align: center;
        color: #000;
        margin-bottom: 12pt;
    }
    .paper-preview h3 {
        font-family: 'Times New Roman', serif;
        font-size: 14pt;
        text-transform: uppercase;
        margin-top: 18pt;
        border-bottom: 1px solid #000;
        padding-bottom: 4pt;
        color: #000;
    }

</style>
""", unsafe_allow_html=True)

# Session Manager
if 'paper_data' not in st.session_state: st.session_state.paper_data = {}
if 'generated' not in st.session_state: st.session_state.generated = False

def main():
    
    # --- MODERN SIDEBAR ---
    with st.sidebar:
        st.title("ResearchDraft")
        st.markdown("**AI-Powered Academic Engine**")
        st.markdown("---")
        
        st.caption("Settings")
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        
        st.caption("Model Configuration")
        model = st.selectbox("Select Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"], index=0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Writing Style")
        venue = st.selectbox("Target Venue", ["IEEE Access", "Nature", "NeurIPS", "CVPR"])
        style = st.slider("Creativity Index", 0.0, 1.0, 0.5)

    # --- HERO SECTION ---
    if not st.session_state.generated:
        st.markdown('<div class="hero-text">ResearchDraft AI</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:left; color:#64748b; font-size:1.2rem; margin-bottom:40px;">Craft journal-ready research papers with the power of modern LLMs.</p>', unsafe_allow_html=True)

        # --- WIZARD LAYOUT ---
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">✨ Project Initialization</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            title = st.text_input("Research Title", placeholder="e.g. Self-Supervised Learning for Medical Imaging")
        with c2:
            domain = st.text_input("Domain", placeholder="e.g. Computer Vision")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            authors = st.text_area("Author Metadata", placeholder="Name | Affiliation | Email", height=100)
        with c4:
            references = st.text_area("Reference Context", placeholder="Paste existing citations here...", height=100)
            
        st.markdown("<br>", unsafe_allow_html=True)
        problem = st.text_area("Problem Statement & Objectives", placeholder="Define the core research gap...", height=120)
        
        st.markdown("</div>", unsafe_allow_html=True) # End Card

        # --- GENERATE BUTTON ---
        col_center_1, col_center_2, col_center_3 = st.columns([1, 2, 1])
        with col_center_2:
            generate = st.button("🚀 IGNITE GENERATION ENGINE", type="primary", use_container_width=True)

        if generate:
            if not api_key:
                st.toast("⚠️ Please provide a valid API Key provided!", icon="🔒")
            else:
                with st.status("🧠 **Orchestrating AI Agents...**", expanded=True) as status:
                    st.write("Initializing Llama-3 Inference...")
                    gen = PaperGenerator(api_key, model)
                    
                    inputs = {"title": title, "domain": domain, "problem": problem, "style": "Academic", "venue": venue, "references": references}
                    sections = ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results and Discussion', 'Future Work', 'Conclusion', 'References']
                    
                    st.session_state.paper_data = {"Title": title, "Authors": authors}
                    
                    progress_bar = st.progress(0)
                    for i, sec in enumerate(sections):
                        status.write(f"✍️ **Drafting {sec}...**")
                        res = gen.generate_section(sec, inputs, "")
                        st.session_state.paper_data[sec] = res
                        progress_bar.progress((i + 1) / len(sections))
                    
                    st.session_state.generated = True
                    status.update(label="✅ Manuscript Compiled Successfully!", state="complete", expanded=False)
                    st.rerun()

    else:
        # --- DASHBOARD LAYOUT ---
        st.markdown('<div class="glass-card" style="padding: 20px; border-left: 5px solid #001f3f;">'
                    '<h2 style="margin:0; font-family: \'Georgia\', serif; color: #001f3f;">Manuscript Composition</h2>'
                    '<p style="margin:0; color:#555; font-size: 14px;">Professional Academic Editor</p>'
                    '</div>', unsafe_allow_html=True)
        
        tabs = st.tabs(["📝 Editor Studio", "📄 Print Preview", "💾 Export Hub"])
        
        with tabs[0]:
            st.markdown("### ✍️ Content Editor")
            st.caption("Edit each section individually. Changes update the preview automatically.")
            
            for section in ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results and Discussion', 'Future Work', 'Conclusion', 'References']:
                # Icon mapping
                icons = {
                    "Abstract": "📝", "Introduction": "🚀", "Literature Review": "📚",
                    "Methodology": "⚙️", "Results and Discussion": "📊", "Future Work": "🔮",
                    "Conclusion": "🏁", "References": "🔗"
                }
                icon = icons.get(section, "📄")
                
                with st.expander(f"{icon} {section}", expanded=(section == "Abstract")):
                    current_val = st.session_state.paper_data.get(section, "")
                    st.session_state.paper_data[section] = st.text_area(
                        f"Edit {section}", 
                        current_val, 
                        height=250, 
                        key=f"text_{section}",
                        label_visibility="collapsed"
                    )

        with tabs[1]:
            # Construct the entire paper HTML to ensure CSS wrapper applies correctly
            # NOTE: We use strict left-alignment to avoid Markdown interpreting indented blocks as code.
            title = st.session_state.paper_data.get('Title', 'Untitled Manuscript')
            authors = st.session_state.paper_data.get('Authors', 'Author Details Not Provided')
            
            paper_html = f"""<div class="paper-preview">
<h1 style="text-align:center;">{title}</h1>
<p style="text-align:center; font-style:italic; margin-bottom: 24px;">{authors}</p>
<hr style="border: 0; border-top: 1px solid #000; margin: 20px 0;">"""
            
            for s in ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results and Discussion', 'Future Work', 'Conclusion', 'References']:
                content = st.session_state.paper_data.get(s, "")
                if content:
                    # Convert newlines to breaks for HTML rendering
                    formatted_content = content.replace("\n", "<br>")
                    paper_html += f"""
<div class="paper-section">
<h3>{s}</h3>
<p>{formatted_content}</p>
</div>"""
            
            # --- PAGE NUMBERS ---
            paper_html += """
<div style="margin-top: 40px; text-align: center; border-top: 1px solid #ccc; padding-top: 10px; color: #666; font-size: 10pt;">
    Page 1
</div>
</div>"""
            st.markdown(paper_html, unsafe_allow_html=True)

        with tabs[2]:
            st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown("### 📥 Download Manuscript")
            c1, c2 = st.columns(2)
            c1.download_button("Word Document (.docx)", DocumentExporter.export_docx(st.session_state.paper_data), "research_paper.docx", "application/docx", use_container_width=True)
            c2.download_button("PDF Document (.pdf)", DocumentExporter.export_pdf(st.session_state.paper_data), "research_paper.pdf", "application/pdf", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
