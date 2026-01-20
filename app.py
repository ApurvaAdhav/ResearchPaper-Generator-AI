import streamlit as st
import generator as gen_module
from generator import PaperGenerator
from exporter import DocumentExporter
import importlib
import time

# Reload generator logic
importlib.reload(gen_module)

st.set_page_config(
    page_title="ResearchIntelligence AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# STRICT ACADEMIC LIGHT THEME
# ==============================================================================
st.markdown("""
<style>
    /* RESET DRACULA / DARK MODES */
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    :root {
        --bg-white: #ffffff;
        --sidebar-bg: #f8f9fa;
        --text-dark: #2c3e50;
        --accent-teal: #008080;
        --border-light: #e9ecef;
    }

    /* MAIN CONTAINER */
    .stApp {
        background-color: var(--bg-white);
        color: var(--text-dark);
        font-family: 'Roboto', sans-serif;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-light);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #333333 !important;
    }
    
    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ced4da;
    }

    /* HEADERS */
    h1, h2, h3 {
        color: #1a1a1a;
        font-family: 'Times New Roman', serif;
    }

    /* KPIS / METRICS */
    .kpi-card {
        background: #f8f9fa;
        border-left: 4px solid var(--accent-teal);
        padding: 15px;
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .kpi-val { font-size: 1.5rem; font-weight: bold; color: var(--accent-teal); }
    .kpi-lbl { font-size: 0.8rem; text-transform: uppercase; color: #666; }

    /* PAPER VIEW (IEEE STYLE) */
    .paper-preview {
        background: white;
        padding: 40px;
        font-family: 'Times New Roman', serif;
        border: 1px solid #ddd;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: black;
        line-height: 1.2;
        text-align: justify;
    }
    .paper-preview h1 { text-align: center; font-size: 24pt; margin-bottom: 5px; }
    .paper-preview h3 { 
        font-size: 14pt; /* EXACT REQUESTED SIZE */
        text-transform: uppercase; 
        font-weight: bold; 
        margin-top: 15px; 
    }
    .author-block { text-align: center; font-size: 11pt; font-style: italic; margin-bottom: 20px; }

</style>
""", unsafe_allow_html=True)

if 'paper_data' not in st.session_state: st.session_state.paper_data = {}
if 'generated' not in st.session_state: st.session_state.generated = False

def main():
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("ResearchIntelligence")
        st.write("Academic Edition v2.1")
        
        with st.expander("Configuration", expanded=True):
            api_key = st.text_input("Groq API Key", type="password")
            model = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        
        st.header("Parameters")
        type_ = st.selectbox("Paper Type", ["IEEE Conference", "Review Article", "Survey", "Proposal"])
        depth = st.select_slider("Depth", ["Brief", "Standard", "In-Depth"], value="Standard")
        
        st.info("System Ready")

    # --- MAIN AREA ---
    if not st.session_state.generated:
        st.markdown("# 🏛️ Academic Research Workbench")
        st.markdown("Generate IEEE-compliant drafts with citation intelligence.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            title = st.text_input("Title of Research", placeholder="Self-Supervised Learning in Medical Imaging")
            problem = st.text_area("Problem Statement", height=100)
            domain = st.text_input("Domain / Field")
        with col2:
            authors = st.text_area("Author Details", height=100, placeholder="Name\nDept, University")
        
        if st.button("Generate Full Menuscript", type="primary"):
            if not api_key:
                st.error("Please enter API Key.")
            else:
                progress = st.status("⚡ Agent active: Drafting Sections...", expanded=True)
                
                gen = PaperGenerator(api_key, model)
                inputs = {'title': title, 'problem': problem, 'domain': domain, 'type': type_, 'depth': depth}
                
                # Single Call Batch
                result = gen.generate_full_paper(inputs)
                
                if "Error" in result:
                    st.error(result["Error"])
                else:
                    st.session_state.paper_data = result
                    st.session_state.paper_data['Title'] = title
                    st.session_state.paper_data['Authors'] = authors
                    st.session_state.generated = True
                    progress.update(label="Complete!", state="complete", expanded=False)
                    st.rerun()

    else:
        # --- DASHBOARD & VIEW ---
        c1, c2, c3 = st.columns(3)
        
        # Metrics using new generator methods
        full_text = " ".join([v for k,v in st.session_state.paper_data.items() if k not in ['Title', 'Authors']])
        gen = PaperGenerator() 
        qual = gen.analyze_quality(full_text)
        orig = gen.estimate_originality(full_text)
        
        c1.markdown(f'<div class="kpi-card"><div class="kpi-val">{qual["score"]}</div><div class="kpi-lbl">Quality Score</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><div class="kpi-val">{qual["level"]}</div><div class="kpi-lbl">Maturity</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(full_text.split())}</div><div class="kpi-lbl">Words</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📄 Menuscript View", "📥 Export"])
        
        with tab1:
            # IEEE VIEW
            pdata = st.session_state.paper_data
            
            html = f"""
            <div class="paper-preview">
                <h1>{pdata.get('Title')}</h1>
                <div class="author-block">{pdata.get('Authors')}</div>
                <hr>
            """
            
            ordering = ['Abstract', 'Index Terms', 'Introduction', 'Literature Review', 'Methodology', 'Results', 'Conclusion', 'References']
            
            for section in ordering:
                if section in pdata:
                    html += f"<h3><font size=5>{section.upper()}</font></h3>"
                    html += f"<p>{pdata[section]}</p>"
            
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        
        with tab2:
            c_a, c_b = st.columns(2)
            c_a.download_button("Download PDF (Numbered)", DocumentExporter.export_pdf(st.session_state.paper_data), "paper.pdf")
            c_b.download_button("Download DOCX", DocumentExporter.export_docx(st.session_state.paper_data), "paper.docx")
            
            if st.button("Start New Paper"):
                st.session_state.generated = False
                st.session_state.paper_data = {}
                st.rerun()

if __name__ == "__main__":
    main()
