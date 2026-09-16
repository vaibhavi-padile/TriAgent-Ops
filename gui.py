import streamlit as st
import os
import json
from app import app  # Imports your working LangGraph system

# Force clean, minimalist page configuration
st.set_page_config(page_title="OpsIntel Analytics", page_icon="🏢", layout="wide")

# --- CUSTOM CSS: Total Color Contrast & Size Normalization Control ---
st.markdown("""
    <style>
        /* 1. Global Light Background Base Group */
        .stApp {
            background-color: #F5F5F7 !important;
        }
        
        /* 2. Lock High-Contrast Text Scales Globally */
        h1, h2, h3, p, span, label {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            color: #111111 !important;
        }
        
        .muted-text {
            color: #6E6E73 !important;
            font-size: 0.95rem;
            margin-bottom: 20px;
        }
        
        /* 3. Sleek Metric Block Frames */
        .pod-card {
            background-color: #FFFFFF !important;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #D2D2D7;
            text-align: center;
            margin-bottom: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.01);
        }
        
        .pod-number {
            font-size: 2.2rem;
            font-weight: 700;
            color: #111111 !important;
            line-height: 1.1;
            margin-bottom: 4px;
        }
        
        .pod-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #6E6E73 !important;
            font-weight: 500;
        }
        
        /* 4. Index Heading Elements (Wove Layout Style) */
        .wove-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        .wove-index {
            font-size: 2rem;
            font-weight: 300;
            color: #8E8E93 !important;
            font-family: monospace !important;
        }
        
        .wove-title {
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        
        /* 5. PERFECT CONTRAST FIX: Deep Gray Slate Console Blocks */
        .json-wrapper {
            background-color: #E8E8ED !important; /* Premium light slate box */
            padding: 18px;
            border-radius: 10px;
            border: 1px solid #D2D2D7;
            white-space: pre-wrap;
            overflow-x: auto;
            margin-top: 0px;
        }
        
        /* Deep force override targeting native browser styling inside code tags */
        .json-wrapper text, .json-wrapper code, .json-wrapper span, .json-wrapper pre {
            color: #111111 !important; 
            font-family: 'Courier New', Courier, monospace !important;
            font-size: 14px !important; 
            font-weight: 600 !important;
        }
        
        /* 6. PERFECT SIZE FIX: Crisp Document Page Frameworks */
        .audit-log-wrapper {
            background-color: #FFFFFF !important; /* Clean corporate sheet */
            padding: 22px;
            border-radius: 10px;
            border: 1px solid #D2D2D7;
            color: #111111 !important; /* Perfect jet black contrast tracking */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 15px !important; /* Normalized readable scale */
            line-height: 1.6 !important;
        }
        
        /* Normalizing nested title headers produced inside the HTML replacements */
        .audit-log-wrapper h3, .audit-log-wrapper h4 {
            font-size: 16px !important;
            font-weight: 700 !important;
            margin-top: 15px !important;
            margin-bottom: 8px !important;
            color: #111111 !important;
        }
        
        /* Native layout adjustments */
        .stFileUploader section {
            background-color: #FFFFFF !important;
            border: 1px dashed #8E8E93 !important;
            border-radius: 12px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER TITLE VIEW ---
st.markdown("<h1>OpsIntel Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p class='muted-text'>A subtle, multi-agent framework auditing unstructured enterprise documents in real-time.</p>", unsafe_allow_html=True)

# --- FILE MANAGER COMPONENT ---
uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file is not None:
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    initial_state = {
        "raw_document_path": temp_filename,
        "extracted_data": None,
        "validation_errors": [],
        "validation_attempts": 0,
        "requires_human_review": False,
        "confidence_score": 1.0,
        "final_report_path": None
    }
    
    with st.spinner("Executing system workflow graph..."):
        final_output = app.invoke(initial_state)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- SECTION 01: PERFORMANCE METRICS ---
    st.markdown("""
        <div class='wove-header'>
            <span class='wove-index'>01</span>
            <span class='wove-title'>Pipeline Analytics Telemetry</span>
        </div>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        score = f"{final_output.get('confidence_score', 0.0) * 100:.0f}%"
        st.markdown(f"<div class='pod-card'><div class='pod-number'>{score}</div><div class='pod-label'>Confidence Rating</div></div>", unsafe_allow_html=True)
        
    with m_col2:
        attempts = final_output.get("validation_attempts", 0)
        st.markdown(f"<div class='pod-card'><div class='pod-number'>{attempts}</div><div class='pod-label'>Validation Iterations</div></div>", unsafe_allow_html=True)
        
    with m_col3:
        review_state = "True" if final_output.get("requires_human_review") else "False"
        st.markdown(f"<div class='pod-card'><div class='pod-number'>{review_state}</div><div class='pod-label'>Human Intervention Flag</div></div>", unsafe_allow_html=True)

    # --- SECTION 02: STRUCTURAL CONTEXT BLOCKS ---
    st.markdown("""
        <div class='wove-header'>
            <span class='wove-index'>02</span>
            <span class='wove-title'>Structured Metadata Outputs</span>
        </div>
    """, unsafe_allow_html=True)
    
    data_col1, data_col2 = st.columns(2)
    
    with data_col1:
        st.markdown("<p style='font-weight: 600; font-size: 14px; margin-bottom: 10px;'>🤖 Machine-Readable JSON Contract</p>", unsafe_allow_html=True)
        json_string = json.dumps(final_output.get("extracted_data", {}), indent=4)
        # We explicitly wrap the string context within a text block inside our styled layout container
        st.markdown(f"<div class='json-wrapper'><text>{json_string}</text></div>", unsafe_allow_html=True)
        
    with data_col2:
        st.markdown("<p style='font-weight: 600; font-size: 14px; margin-bottom: 10px;'>📄 Human-Readable System Audit Log</p>", unsafe_allow_html=True)
        if final_output["final_report_path"] and os.path.exists(final_output["final_report_path"]):
            with open(final_output["final_report_path"], "r") as report_file:
                report_content = report_file.read()
                
                # Format header markers securely for crisp display
                html_formatted_report = report_content.replace("# Operations Audit Report", "<h3>Operations Audit Report</h3>")
                html_formatted_report = html_formatted_report.replace("## System Ingestion Data Metrics", "<h4>System Ingestion Data Metrics</h4>")
                html_formatted_report = html_formatted_report.replace("\n", "<br>").replace("**", "")
                
                st.markdown(f"<div class='audit-log-wrapper'>{html_formatted_report}</div>", unsafe_allow_html=True)

    if os.path.exists(temp_filename):
        os.remove(temp_filename)
else:
    st.markdown("""
        <div style='text-align: center; margin-top: 60px; padding: 40px; border-radius: 12px; background-color: #E8E8ED; border: 1px solid #D2D2D7;'>
            <p style='font-size: 1.1rem; font-weight: 500; color: #111111;'>System Idle Status</p>
            <p style='font-size: 0.85rem; color: #6E6E73;'>Drop an unstructured corporate contract document (.pdf) above to run your multi-agent architecture.</p>
        </div>
    """, unsafe_allow_html=True)
