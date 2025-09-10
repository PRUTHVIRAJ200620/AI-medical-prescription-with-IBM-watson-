"""
AI Prescription Verifier - Professional Streamlit Frontend
Enhanced UI/UX with improved theme, navigation, and visibility
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import os
from datetime import datetime

# Load environment variables
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "MediGuard_Hackathon_2024_SecureKey")

# Page configuration
st.set_page_config(
    page_title="AI Prescription Verifier",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/AI_Prescription_Verifier',
        'Report a bug': 'https://github.com/your-repo/AI_Prescription_Verifier/issues',
        'About': "AI Medical Prescription Verification leveraging IBM Watson and Hugging Face Models"
    }
)

# Professional CSS Theme
def apply_professional_theme():
    st.markdown("""
    <style>
        /* Import professional fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables for consistent theming */
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --accent-color: #3b82f6;
            --success-color: #059669;
            --warning-color: #d97706;
            --error-color: #dc2626;
            --background-color: #f8fafc;
            --surface-color: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Base styling */
        .main {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Header styles */
        .main-header {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #1e40af 100%);
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-align: center;
            margin: 2rem 0 1rem 0 !important;
            text-shadow: none !important;
        }
        
        .sub-header {
            font-size: 1.5rem !important;
            color: #64748b !important;
            text-align: center;
            font-weight: 400 !important;
            margin-bottom: 3rem !important;
            line-height: 1.6;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #60a5fa !important;
            font-weight: 600 !important;
        }
        
        /* Navigation radio buttons */
        [data-testid="stSidebar"] .stRadio > div {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            background: rgba(59, 130, 246, 0.1) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            display: block !important;
            width: 100% !important;
        }
        
        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(59, 130, 246, 0.2) !important;
            border-color: rgba(59, 130, 246, 0.5) !important;
            transform: translateX(4px) !important;
        }
        
        /* Sample prescription buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.7rem 1rem !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            width: 100% !important;
            margin: 0.3rem 0 !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 15px rgba(37, 99, 235, 0.4) !important;
        }
        
        /* Main content buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
            color: white !important;
            border: 2px solid #ffffff !important;
            border-radius: 12px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
            min-height: 50px !important;
            display: inline-block !important;
            width: auto !important;
            text-align: center !important;
            margin: 0.5rem 0 !important;
            z-index: 100 !important;
            position: relative !important;
            text-shadow: none !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(30, 64, 175, 0.5) !important;
        }
        
        /* Form inputs */
        .stTextArea textarea,
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox select {
            background-color: white !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            color: #000000 !important;
            font-weight: 500 !important;
            transition: border-color 0.3s ease !important;
        }
        
        .stTextArea textarea:focus,
        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stSelectbox select:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Ensure buttons inside or near text areas are visible */
        .stTextArea ~ .stButton > button,
        .stTextInput ~ .stButton > button {
            margin-top: 1rem !important;
            display: block !important;
            clear: both !important;
        }
        
        /* Ensure text inside text areas is visible */
        .stTextArea textarea {
            color: #000000 !important;
            font-weight: 500 !important;
        }
        
        /* Ensure text inside text inputs is visible */
        .stTextInput input {
            color: #000000 !important;
            font-weight: 500 !important;
        }
        
        /* Cards and containers */
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border: 1px solid #f1f5f9;
            transition: all 0.3s ease;
            height: 100%;
            margin-bottom: 1.5rem;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            border-color: #3b82f6;
        }
        
        .feature-card h3 {
            color: #1e293b !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 0.5rem;
        }
        
        .feature-card ul {
            color: #64748b !important;
            line-height: 1.8;
        }
        
        .feature-card li {
            margin-bottom: 0.5rem;
            position: relative;
            padding-left: 1.5rem;
        }
        
        .feature-card li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #059669;
            font-weight: bold;
        }
        
        /* Hero section */
        .hero-section {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1e40af 100%);
            color: white !important;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 3rem;
            text-align: center;
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
        }
        
        .hero-section h1 {
            color: white !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin-bottom: 1rem !important;
        }
        
        .hero-section p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1.3rem !important;
            line-height: 1.6;
        }
        
        /* Alert styles */
        .stAlert {
            border-radius: 10px !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
            margin: 1rem 0 !important;
        }
        
        .stSuccess {
            background: linear-gradient(135deg, #d1fae5, #a7f3d0) !important;
            color: #065f46 !important;
            border-left: 4px solid #059669 !important;
        }
        
        .stError {
            background: linear-gradient(135deg, #fee2e2, #fecaca) !important;
            color: #991b1b !important;
            border-left: 4px solid #dc2626 !important;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
            color: #92400e !important;
            border-left: 4px solid #d97706 !important;
        }
        
        .stInfo {
            background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
            color: #1e40af !important;
            border-left: 4px solid #2563eb !important;
        }
        
        /* Expanders */
        .streamlit-expander {
            background: white !important;
            border: 2px solid #f1f5f9 !important;
            border-radius: 12px !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        }
        
        .streamlit-expander:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0 8px 15px rgba(59, 130, 246, 0.1) !important;
        }
        
        .streamlit-expanderHeader {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        .streamlit-expanderContent {
            color: #64748b !important;
            padding: 1.5rem !important;
        }
        
        /* Tables */
        table {
            background: white !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        }
        
        th {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
            text-transform: uppercase !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.5px !important;
        }
        
        td {
            color: #1e293b !important;
            padding: 1rem !important;
            border-bottom: 1px solid #f1f5f9 !important;
        }
        
        tr:hover {
            background: #f8fafc !important;
        }
        
        /* Metrics */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #f1f5f9;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Ensure all text is properly colored and visible */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: #1e293b !important;
            font-weight: 600 !important;
        }
        
        .main p, .main div, .main span {
            color: #1e293b !important;
        }
        
        /* Fix column layout for buttons */
        .row-widget.stButton {
            width: 100% !important;
            display: block !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Improve placeholder text visibility */
        ::placeholder {
            color: #475569 !important;
            opacity: 1 !important;
        }
        
        /* Ensure buttons in columns are visible */
        [data-testid="column"] .stButton > button {
            width: 100% !important;
            display: block !important;
            margin: 0.5rem 0 !important;
            z-index: 10 !important;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-top-color: #3b82f6 !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply the theme
apply_professional_theme()

class PrescriptionVerifierApp:
    """Main application class for Streamlit interface"""
    
    def __init__(self):
        self.api_headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # Initialize session state
        if 'prescription_text' not in st.session_state:
            st.session_state.prescription_text = ""
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
    
    def check_api_connection(self) -> bool:
        """Check if FastAPI backend is accessible"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def call_interaction_endpoint(self, prescription_text: str) -> Dict[str, Any]:
        """Call the /check_interactions endpoint"""
        try:
            payload = {"prescription_text": prescription_text}
            
            response = requests.post(
                f"{API_BASE_URL}/check_interactions",
                headers=self.api_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"API Error {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Connection Error: {str(e)}"}
    
    def call_dosage_endpoint(self, prescription_text: str, patient_age: Optional[int] = None) -> Dict[str, Any]:
        """Call the /check_dosage endpoint"""
        try:
            payload = {
                "prescription_text": prescription_text,
                "patient_age": patient_age
            }
            
            response = requests.post(
                f"{API_BASE_URL}/check_dosage",
                headers=self.api_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"API Error {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Connection Error: {str(e)}"}

def render_header():
    """Render the main application header"""
    st.markdown('<h1 class="main-header">🏥 AI Prescription Verifier</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI Medical Prescription Verification leveraging IBM Watson and Hugging Face Posos/ClinicalNER Model</p>', unsafe_allow_html=True)

def render_sidebar(app: PrescriptionVerifierApp):
    """Render the sidebar with navigation and samples"""
    st.sidebar.title("🧭 Navigation")
    
    # API Status with better styling
    api_status = app.check_api_connection()
    if api_status:
        st.sidebar.success("✅ Backend Connected")
    else:
        st.sidebar.error("❌ Backend Disconnected")
        st.sidebar.warning("⚠️ Start FastAPI server on localhost:8000")
    
    st.sidebar.markdown("---")
    
    # Enhanced navigation with radio buttons
    selected_page = st.sidebar.radio(
        "📱 **Select Page**",
        ["🏠 Home", "🔍 Drug Interaction Checker", "💊 Dosage & Alternatives", "📊 Analysis History"],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Sample prescriptions
    st.sidebar.title("📝 Sample Prescriptions")
    st.sidebar.markdown("*Click to load sample data:*")
    
    sample_prescriptions = {
        "Critical Interaction": "Rx: Atorvastatin 10mg daily for cholesterol, Clarithromycin 500mg twice daily for 7 days for bacterial infection. Patient is 68 years old.",
        "Multiple Drugs": "Prescription: Metformin 500mg twice daily, Lisinopril 10mg once daily, Atorvastatin 20mg at bedtime. Patient age 55 years, Type 2 diabetes and hypertension.",
        "Geriatric Case": "Medications: Aspirin 325mg daily, Ibuprofen 600mg three times daily for arthritis pain. Patient is 75 years old female.",
        "Pediatric Warning": "Rx: Aspirin 81mg daily for fever, Acetaminophen 250mg every 6 hours as needed. Child is 8 years old, weight 25kg.",
        "Complex Case": "Current medications: Warfarin 5mg daily, Aspirin 81mg daily, Cimetidine 400mg twice daily, Furosemide 40mg daily. Patient age 70, multiple comorbidities."
    }
    
    for name, prescription in sample_prescriptions.items():
        if st.sidebar.button(f"📋 {name}", key=f"sample_{name}"):
            st.session_state.prescription_text = prescription
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Information section
    st.sidebar.markdown("### 🔬 **AI Technologies**")
    st.sidebar.info("""
    **🧠 Models Used:**
    - Hugging Face samant/medical-ner
    - IBM Watson NLU
    - RxNorm/RxNav APIs
    - FastAPI Backend
    
    **💡 Features:**
    - Real-time drug extraction
    - Context-aware alerts  
    - Age-based recommendations
    """)
    
    return selected_page

def render_home_page():
    """Render the home page with overview and quick test"""
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>Welcome to AI Prescription Verifier</h1>
        <p>Advanced AI-powered system for detecting drug interactions, verifying dosages, and ensuring medication safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Drug Interaction Analysis</h3>
            <ul>
                <li>Hugging Face Posos/ClinicalNER for drug extraction</li>
                <li>IBM Watson NLU for context analysis</li>
                <li>Comprehensive DDI dataset validation</li>
                <li>Real-time interaction detection</li>
                <li>Evidence-based recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💊 Dosage Verification</h3>
            <ul>
                <li>RxNorm API integration</li>
                <li>Age-based dosage recommendations</li>
                <li>Pediatric & geriatric considerations</li>
                <li>Alternative drug suggestions</li>
                <li>Safety threshold monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Key Features</h3>
            <ul>
                <li>Real-time prescription analysis</li>
                <li>Scientific drug mapping (RxCUI)</li>
                <li>Context-aware safety alerts</li>
                <li>Comprehensive reporting</li>
                <li>Export functionality</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick test section
    st.markdown("---")
    st.markdown("## 🚀 Quick Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        test_text = st.text_area(
            "**Enter prescription text for quick analysis:**",
            value=st.session_state.get('prescription_text', ''),
            placeholder="Example: Atorvastatin 10mg daily, Clarithromycin 500mg BD for 5 days. Patient age 68.",
            height=120,
            key="quick_test_text"
        )
        # Keep session state in sync with quick analysis input
        st.session_state.prescription_text = test_text
    
    with col2:
        st.markdown("**Quick Actions:**")
        if st.button("🔍 Check Interactions", type="primary", use_container_width=True):
            if test_text.strip():
                with st.spinner("🔄 Analyzing interactions..."):
                    app = PrescriptionVerifierApp()
                    result = app.call_interaction_endpoint(test_text)
                    
                    if result["success"]:
                        data = result["data"]
                        total_interactions = data.get("total_interactions", 0)
                        
                        # Store in analysis history
                        if 'analysis_history' not in st.session_state:
                            st.session_state.analysis_history = []
                        
                        # Add current analysis to history
                        st.session_state.analysis_history.append({
                            'prescription': test_text,
                            'type': 'Quick Interaction Check',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'results': data
                        })
                        
                        if total_interactions > 0:
                            st.error(f"🚨 Found {total_interactions} potential interaction(s)")
                            
                            for interaction in data.get("interactions", []):
                                with st.expander(f"⚠️ {interaction.get('drug_a', 'Unknown')} + {interaction.get('drug_b', 'Unknown')}"):
                                    severity = interaction.get('severity', 'Unknown')
                                    if severity == 'CRITICAL':
                                        st.error(f"**🔴 Severity:** {severity}")
                                    elif severity == 'WARNING':
                                        st.warning(f"**🟡 Severity:** {severity}")
                                    else:
                                        st.info(f"**🔵 Severity:** {severity}")
                                    
                                    st.write(f"**🔧 Mechanism:** {interaction.get('mechanism', 'Not specified')}")
                                    st.write(f"**📄 Description:** {interaction.get('description', 'No description available')}")
                                    
                                    # Show Watson NLU alerts if available
                                    alerts = data.get('alerts', [])
                                    matching_alert = None
                                    for alert in alerts:
                                        if alert.get('interaction_pair') == f"{interaction.get('drug_a')} ↔ {interaction.get('drug_b')}":
                                            matching_alert = alert
                                            break
                                    
                                    if matching_alert:
                                        st.info(f"**🧠 AI Alert:** {matching_alert.get('alert_message', 'Potential risk detected')}")
                                        st.success(f"**💡 Recommendation:** {matching_alert.get('recommendation', 'Consult healthcare provider')}")
                        else:
                            st.success("✅ No potential drug interactions detected")
                            
                        # Show extracted medicines
                        if data.get('extracted_medicines'):
                            st.subheader("💊 **Extracted Medicines**")
                            medicines_df = pd.DataFrame([{"Medicine": med} for med in data.get('extracted_medicines', [])])
                            st.dataframe(medicines_df, use_container_width=True)
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Failed to analyze interactions')}")
            else:
                st.warning("⚠️ Please enter prescription text to analyze")
        
        if st.button("💊 Check Dosage", type="secondary", use_container_width=True):
            if test_text.strip():
                with st.spinner("🔄 Verifying dosage..."):
                    app = PrescriptionVerifierApp()
                    result = app.call_dosage_endpoint(test_text, 45)  # Default age
                    
                    if result["success"]:
                        data = result["data"]
                        
                        # Store in analysis history
                        if 'analysis_history' not in st.session_state:
                            st.session_state.analysis_history = []
                        
                        # Add current analysis to history
                        st.session_state.analysis_history.append({
                            'prescription': test_text,
                            'type': 'Quick Dosage Check',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'results': data
                        })
                        
                        st.success(f"✅ Analyzed {len(data.get('extracted_medicines', []))} medicines")
                        
                        if data.get('dosage_recommendations'):
                            st.subheader("⚠️ **Dosage Recommendations**")
                            for rec in data['dosage_recommendations']:
                                st.warning(f"**{rec.get('medicine', 'Unknown')}:** {rec.get('recommendation', 'No recommendation')}")
                        
                        if data.get('alternatives'):
                            st.subheader("🔄 **Alternative Medications**")
                            alternatives_df = pd.DataFrame(data['alternatives'])
                            st.dataframe(alternatives_df, use_container_width=True)
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Failed to analyze dosage')}")
            else:
                st.warning("⚠️ Please enter prescription text to analyze")

def render_interaction_checker(app: PrescriptionVerifierApp):
    """Render drug interaction checker page"""
    st.markdown("# 🔍 Drug Interaction Checker")
    st.markdown("**Analyze prescription text for potential drug-drug interactions using advanced AI**")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prescription_text = st.text_area(
            "**Enter Prescription Text:**",
            value=st.session_state.get('prescription_text', ''),
            placeholder="Enter complete prescription details including drug names, dosages, and patient information...",
            height=150,
            key="interaction_prescription"
        )
    
    with col2:
        st.markdown("**Analysis Options:**")
        if st.button("🔍 Analyze Interactions", type="primary", use_container_width=True):
            if prescription_text.strip():
                with st.spinner("🔄 Running comprehensive analysis..."):
                    result = app.call_interaction_endpoint(prescription_text)
                    
                    if result["success"]:
                        data = result["data"]
                        
                        # Store result for display
                        st.session_state.interaction_result = data
                        st.session_state.prescription_text = prescription_text
                        
                        # Store in analysis history
                        if 'analysis_history' not in st.session_state:
                            st.session_state.analysis_history = []
                        
                        # Add current analysis to history
                        st.session_state.analysis_history.append({
                            'prescription': prescription_text,
                            'type': 'Drug Interaction Check',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'results': data
                        })
                        
                        st.rerun()
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Please enter prescription text to analyze")
        
        if st.button("🔄 Clear Results", use_container_width=True):
            if 'interaction_result' in st.session_state:
                del st.session_state.interaction_result
            st.session_state.prescription_text = ""
            st.rerun()
    
    # Display results if available
    if 'interaction_result' in st.session_state:
        st.markdown("---")
        data = st.session_state.interaction_result
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #2563eb; margin: 0;">💊</h3>
                <h2 style="color: #1e293b; margin: 0.5rem 0 0 0;">{}</h2>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Medicines Found</p>
            </div>
            """.format(len(data.get('extracted_medicines', []))), unsafe_allow_html=True)
        
        with col2:
            total_interactions = data.get("total_interactions", 0)
            color = "#dc2626" if total_interactions > 0 else "#059669"
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: {}; margin: 0;">⚠️</h3>
                <h2 style="color: #1e293b; margin: 0.5rem 0 0 0;">{}</h2>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Interactions</p>
            </div>
            """.format(color, total_interactions), unsafe_allow_html=True)
        
        with col3:
            alerts_count = len(data.get('alerts', []))
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #d97706; margin: 0;">🧠</h3>
                <h2 style="color: #1e293b; margin: 0.5rem 0 0 0;">{}</h2>
                <p style="color: #64748b; margin: 0; font-weight: 500;">AI Alerts</p>
            </div>
            """.format(alerts_count), unsafe_allow_html=True)
        
        with col4:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #059669; margin: 0;">⏱️</h3>
                <h2 style="color: #1e293b; margin: 0.5rem 0 0 0; font-size: 1.2rem;">{}</h2>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Analysis Time</p>
            </div>
            """.format(timestamp), unsafe_allow_html=True)
        
        # Extracted medicines
        if data.get('extracted_medicines'):
            st.markdown("## 💊 **Extracted Medicines**")
            medicines_df = pd.DataFrame([
                {"Medicine": med, "Status": "✅ Detected"} 
                for med in data['extracted_medicines']
            ])
            st.dataframe(medicines_df, use_container_width=True)
        
        # Drug interactions
        interactions = data.get("interactions", [])
        if interactions:
            st.markdown("## ⚠️ **Drug-Drug Interactions**")
            
            for i, interaction in enumerate(interactions, 1):
                severity = interaction.get('severity', 'UNKNOWN').upper()
                
                # Choose icon and color based on severity
                if severity == 'CRITICAL':
                    icon = "🔴"
                    severity_color = "color: #dc2626; font-weight: bold;"
                elif severity == 'WARNING':
                    icon = "🟡"
                    severity_color = "color: #d97706; font-weight: bold;"
                else:
                    icon = "🟢"
                    severity_color = "color: #059669; font-weight: bold;"
                
                with st.expander(f"{icon} **Interaction {i}:** {interaction.get('drug_a', 'Unknown')} + {interaction.get('drug_b', 'Unknown')} - {severity}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**🎯 Severity:** <span style='{severity_color}'>{severity}</span>", unsafe_allow_html=True)
                        st.markdown(f"**🔧 Mechanism:** {interaction.get('mechanism', 'Not specified')}")
                        st.markdown(f"**📚 Source:** {interaction.get('reference', 'Internal Database')}")
                    
                    with col2:
                        # Show Watson NLU alert if available
                        matching_alert = None
                        for alert in data.get('alerts', []):
                            if alert.get('interaction_pair') == f"{interaction.get('drug_a')} ↔ {interaction.get('drug_b')}":
                                matching_alert = alert
                                break
                        
                        if matching_alert:
                            st.info(f"**🧠 AI Analysis:** {matching_alert.get('alert_message', 'Interaction detected')}")
                            st.success(f"**💡 Recommendation:** {matching_alert.get('recommendation', 'Consult healthcare provider')}")
                    
                    st.markdown(f"**📄 Description:** {interaction.get('description', 'No description available')}")
        else:
            st.success("✅ **No drug interactions detected!** The analyzed medications appear to be safe when used together.")
        
        # Export functionality
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download JSON Report", use_container_width=True):
                report_data = {
                    "analysis_type": "drug_interactions",
                    "timestamp": datetime.now().isoformat(),
                    "prescription_text": prescription_text,
                    "results": data
                }
                st.download_button(
                    label="💾 Save Report",
                    data=json.dumps(report_data, indent=2),
                    file_name=f"interaction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if interactions:
                interactions_df = pd.DataFrame(interactions)
                csv_data = interactions_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV Data",
                    data=csv_data,
                    file_name=f"interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

def render_dosage_checker(app: PrescriptionVerifierApp):
    """Render dosage checker page"""
    st.markdown("# 💊 Dosage & Alternative Checker")
    st.markdown("**Verify correct dosages and discover safer alternatives based on patient age and clinical guidelines**")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prescription_text = st.text_area(
            "**Enter Prescription Text:**",
            value=st.session_state.get('prescription_text', ''),
            placeholder="Enter prescription with dosage details and patient information...",
            height=150,
            key="dosage_prescription"
        )
    
    with col2:
        st.markdown("**Patient Information:**")
        patient_age = st.number_input(
            "**Patient Age (years):**",
            min_value=0,
            max_value=120,
            value=45,
            step=1,
            key="dosage_patient_age"
        )
        
        # Age group indicator
        if patient_age < 12:
            st.info("👶 **Pediatric Patient** (< 12 years)")
        elif patient_age >= 65:
            st.warning("👴 **Geriatric Patient** (≥ 65 years)")
        else:
            st.success("👤 **Adult Patient** (12-64 years)")
        
        if st.button("💊 Analyze Dosage", type="primary", use_container_width=True):
            if prescription_text.strip():
                with st.spinner("🔄 Analyzing dosage and finding alternatives..."):
                    result = app.call_dosage_endpoint(prescription_text, patient_age)
                    
                    if result["success"]:
                        data = result["data"]
                        st.session_state.dosage_result = data
                        st.session_state.prescription_text = prescription_text
                        st.session_state.patient_age = patient_age
                        
                        # Store in analysis history
                        if 'analysis_history' not in st.session_state:
                            st.session_state.analysis_history = []
                        
                        # Add current analysis to history
                        st.session_state.analysis_history.append({
                            'prescription': prescription_text,
                            'type': 'Dosage & Alternatives Check',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'results': data
                        })
                        
                        st.rerun()
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Please enter prescription text to analyze")
    
    # Display results if available
    if 'dosage_result' in st.session_state:
        st.markdown("---")
        data = st.session_state.dosage_result
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #2563eb;">👤</h3>
                <h2 style="color: #1e293b;">{} years</h2>
                <p style="color: #64748b; font-weight: 500;">Patient Age</p>
            </div>
            """.format(st.session_state.get('patient_age', 'N/A')), unsafe_allow_html=True)
        
        with col2:
            medicines_count = len(data.get('extracted_medicines', []))
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #059669;">💊</h3>
                <h2 style="color: #1e293b;">{}</h2>
                <p style="color: #64748b; font-weight: 500;">Medicines Analyzed</p>
            </div>
            """.format(medicines_count), unsafe_allow_html=True)
        
        with col3:
            alternatives_count = len(data.get('alternatives', []))
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #d97706;">🔄</h3>
                <h2 style="color: #1e293b;">{}</h2>
                <p style="color: #64748b; font-weight: 500;">Alternatives Found</p>
            </div>
            """.format(alternatives_count), unsafe_allow_html=True)
        
        # Extracted medicines
        if data.get('extracted_medicines'):
            st.markdown("## 💊 **Extracted Medicines**")
            medicines_df = pd.DataFrame([
                {"Medicine": med, "Status": "✅ Analyzed"} 
                for med in data['extracted_medicines']
            ])
            st.dataframe(medicines_df, use_container_width=True)
        
        # Dosage recommendations
        dosage_recs = data.get('dosage_recommendations', [])
        if dosage_recs:
            st.markdown("## ⚠️ **Dosage Recommendations**")
            
            for i, rec in enumerate(dosage_recs, 1):
                medicine = rec.get('medicine', 'Unknown')
                age_group = rec.get('age_group', 'N/A')
                recommendation = rec.get('recommendation', 'No specific recommendation')
                
                with st.expander(f"💊 **{medicine}** - {age_group.title()} Patient"):
                    if 'reduce' in recommendation.lower() or 'lower' in recommendation.lower():
                        st.warning(f"**⬇️ Dosage Adjustment Needed:** {recommendation}")
                    elif 'avoid' in recommendation.lower() or 'contraindicated' in recommendation.lower():
                        st.error(f"**🚫 Contraindication:** {recommendation}")
                    else:
                        st.info(f"**ℹ️ Clinical Note:** {recommendation}")
        
        # Alternative medications
        alternatives = data.get('alternatives', [])
        if alternatives:
            st.markdown("## 🔄 **Alternative Medications**")
            
            alternatives_data = []
            for alt in alternatives:
                alternatives_data.append({
                    "Original Drug": alt.get('original_drug', 'Unknown'),
                    "Alternative Drug": alt.get('alternative_drug', 'Unknown'),
                    "Reason": alt.get('reason', 'Same therapeutic class'),
                    "Dosage Form": alt.get('dosage_form', 'Various forms available')
                })
            
            if alternatives_data:
                alternatives_df = pd.DataFrame(alternatives_data)
                st.dataframe(alternatives_df, use_container_width=True)
        
        # If no issues found
        if not dosage_recs and not alternatives:
            st.success("""
            ✅ **No dosage adjustments needed!** 
            
            The prescribed medications and dosages appear appropriate for the patient's age group based on current clinical guidelines.
            """)

def render_analysis_history():
    """Render analysis history page"""
    st.markdown("# 📊 Analysis History")
    st.markdown("**View and manage your previous prescription analyses**")
    
    if 'analysis_history' in st.session_state and st.session_state.analysis_history:
        st.success(f"📈 **Found {len(st.session_state.analysis_history)} previous analyses**")
        
        for i, analysis in enumerate(reversed(st.session_state.analysis_history), 1):
            with st.expander(f"📋 **Analysis {i}** - {analysis.get('timestamp', 'Unknown time')}"):
                st.markdown(f"**💬 Prescription:** {analysis.get('prescription', 'No prescription text')}")
                st.markdown(f"**📊 Type:** {analysis.get('type', 'Unknown')}")
                st.markdown(f"**⏰ Timestamp:** {analysis.get('timestamp', 'Not recorded')}")
                
                if analysis.get('results'):
                    st.json(analysis['results'])
        
        # Clear history button
        if st.button("🗑️ Clear Analysis History", type="secondary"):
            st.session_state.analysis_history = []
            st.success("✅ Analysis history cleared!")
            st.rerun()
    else:
        st.info("""
        📝 **No analysis history available**
        
        Start by analyzing prescriptions using the Drug Interaction Checker or Dosage Checker to build your analysis history.
        """)

def main():
    """Main application function"""
    # Initialize the app
    app = PrescriptionVerifierApp()
    
    # Render header
    render_header()
    
    # Render sidebar and get selected page
    selected_page = render_sidebar(app)
    
    # Route to appropriate page
    if selected_page == "🏠 Home":
        render_home_page()
    elif selected_page == "🔍 Drug Interaction Checker":
        render_interaction_checker(app)
    elif selected_page == "💊 Dosage & Alternatives":
        render_dosage_checker(app)
    elif selected_page == "📊 Analysis History":
        render_analysis_history()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; margin-top: 2rem;">
        <p><strong>AI Prescription Verifier v1.0</strong> | Powered by Hugging Face Posos/ClinicalNER, IBM Watson & RxNorm</p>
        <p>🏥 Enhancing medication safety through artificial intelligence</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
