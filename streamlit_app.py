from io import BytesIO
import time
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

import streamlit as st
from dotenv import load_dotenv


def create_pdf_report(selected_idea, market_report, competitor_report, business_report, pitch_report):
    buffer = BytesIO()
    
    # 1. Page Template Setup (0.75 in / 54 pt margins)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=65
    )
    
    # 2. Typography Styles definition
    styles = getSampleStyleSheet()
    
    custom_title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'), # slate-900
        spaceAfter=6
    )
    
    custom_subtitle_style = ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'), # slate-500
        spaceAfter=15
    )
    
    section_heading_style = ParagraphStyle(
        name='SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#4f46e5'), # indigo-600
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    custom_body_style = ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'), # slate-700
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    custom_subheading_style = ParagraphStyle(
        name='CustomSubHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'), # slate-800
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    custom_bullet_style = ParagraphStyle(
        name='CustomBullet',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    story = []
    
    # 3. Add Document Header Cover block
    story.append(Paragraph("AI STARTUP BRIEF", ParagraphStyle(
        name='CategoryTag',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=4
    )))
    
    story.append(Paragraph("AI Startup Idea Generator Report", custom_title_style))
    
    generation_date = time.strftime("%B %d, %Y")
    story.append(Paragraph(f"Analysis Report &bull; Compiled on {generation_date} &bull; Powered by Gemini AI", custom_subtitle_style))
    
    # Divider Rule
    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor('#cbd5e1'), # slate-300
        spaceAfter=15
    ))
    
    # Parser helper to cleanly format LLM unstructured text lists
    def add_section_content(text):
        if not text:
            story.append(Paragraph("No data available.", custom_body_style))
            return
            
        lines = text.split("\n")
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Strip bold formatting markdown
            clean_line = line_stripped.replace("**", "").replace("###", "").strip()
            
            # Check for bullet layouts
            is_bullet = False
            if clean_line.startswith("*") or clean_line.startswith("-") or clean_line.startswith("•"):
                is_bullet = True
                clean_line = re.sub(r"^[-*•]\s*", "", clean_line)
                
            if is_bullet:
                story.append(Paragraph(f"&bull; {clean_line}", custom_bullet_style))
            elif re.match(r"^\d+\.", clean_line) or clean_line.endswith(":"):
                story.append(Paragraph(clean_line, custom_subheading_style))
            else:
                story.append(Paragraph(clean_line, custom_body_style))
    
    # 4. Render Section 1: Selected Startup Idea
    story.append(Paragraph("1. Startup Concept", section_heading_style))
    story.append(Paragraph(selected_idea, ParagraphStyle(
        name='IdeaHighlight',
        parent=custom_body_style,
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )))
    
    # 5. Render Section 2: Market Analysis
    story.append(Paragraph("2. Market Research & Demand", section_heading_style))
    add_section_content(market_report)
    
    # 6. Render Section 3: Competitor Analysis
    story.append(Paragraph("3. Competitive Landscape & Gaps", section_heading_style))
    add_section_content(competitor_report)
    
    # 7. Render Section 4: Business Model
    story.append(Paragraph("4. Business Strategy & Monetization", section_heading_style))
    add_section_content(business_report)
    
    # 8. Render Section 5: Investor Pitch
    story.append(Paragraph("5. Elevator Pitch & Value Proposition", section_heading_style))
    add_section_content(pitch_report)
    
    # 9. Canvas Decorator Footer
    def add_page_decorations(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 8.5)
        canvas.setFillColor(colors.HexColor('#64748b'))
        
        # Horizontal boundary line above footer
        canvas.setStrokeColor(colors.HexColor('#e2e8f0'))
        canvas.setLineWidth(0.5)
        canvas.line(54, 48, doc.pagesize[0] - 54, 48)
        
        # Left footer note
        canvas.drawString(54, 32, "Confidential - For Internal Use Only")
        
        # Right footer page number
        page_num = canvas.getPageNumber()
        canvas.drawRightString(doc.pagesize[0] - 54, 32, f"Page {page_num}")
        canvas.restoreState()
        
    doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
    buffer.seek(0)
    return buffer

# Load environment variables
load_dotenv()

# Import core agents and fallback logic
from agents.idea_agent import generate_startup_idea
from agents.market_agent import analyze_market
from agents.competitor_agent import analyze_competitors
from agents.business_agent import generate_business_model
from agents.pitch_agent import generate_pitch
from agents.fallback import (
    get_mock_ideas,
    get_mock_market,
    get_mock_competitors,
    get_mock_business,
    get_mock_pitch
)

# Set up clean, responsive dashboard configuration
st.set_page_config(
    page_title="AI Startup Idea Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply sleek, professional CSS styling to override standard designs
st.markdown("""
<style>
    /* Main gradient title */
    .title-text {
        background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Subheading description */
    .subtitle-text {
        color: #94a3b8;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2.5rem;
    }

    /* Style standard button to look premium */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: opacity 0.2s, transform 0.1s;
    }
    
    div.stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        color: white;
    }
    
    /* Add styled container cards for content blocks */
    .content-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        color: #cbd5e1 !important;
    }
    .content-box h1, .content-box h2, .content-box h3, .content-box h4, .content-box h5, .content-box h6 {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif;
    }
    .content-box p, .content-box li, .content-box span, .content-box ul {
        color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State values to persist variables across Streamlit runs
if "ideas_list" not in st.session_state:
    st.session_state.ideas_list = []
if "selected_idea" not in st.session_state:
    st.session_state.selected_idea = ""
if "market_report" not in st.session_state:
    st.session_state.market_report = None
if "competitor_report" not in st.session_state:
    st.session_state.competitor_report = None
if "business_report" not in st.session_state:
    st.session_state.business_report = None
if "pitch_report" not in st.session_state:
    st.session_state.pitch_report = None
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

def invoke_with_retry(func, *args, **kwargs):
    """
    Executes Gemini LLM invocations with automatic rate-limit waiting.
    Sends user alerts directly to the Streamlit layout.
    """
    max_attempts = 4
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            is_rate_limit = any(term in error_msg.lower() for term in [
                "429", "resourceexhausted", "resource_exhausted", "exhausted", "quota", "rate limit", "limit exceeded"
            ])
            if is_rate_limit and attempt < max_attempts - 1:
                # Default delay is 32 seconds
                delay = 32
                delay_match = re.search(r"retryDelay':\s*'(\d+)s?'", error_msg)
                if delay_match:
                    delay = int(delay_match.group(1)) + 1
                
                # Show wait status to user in Streamlit
                st.warning(f"⏳ API Rate Limit Hit. Pausing for {delay} seconds to recover...")
                time.sleep(delay)
            else:
                raise e

# Render App Headers
st.markdown('<div class="title-text">🚀 AI Startup Idea Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Multi-agent intelligence: Brainstorming, Market Research, Competitor Analysis, and Pitch Decks.</div>', unsafe_allow_html=True)

# Sidebar Configuration Layout
with st.sidebar:
    st.header("⚙️ Configuration")
    domain_input = st.text_input("Startup Domain / Focus", placeholder="e.g. AI + Education")
    
    # Reset button to clear session cache
    if st.button("Reset Session", use_container_width=True):
        st.session_state.ideas_list = []
        st.session_state.selected_idea = ""
        st.session_state.market_report = None
        st.session_state.competitor_report = None
        st.session_state.business_report = None
        st.session_state.pitch_report = None
        st.session_state.demo_mode = False
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Multi-Agent Orchestrator:**
    * 🤖 **Idea Agent**
    * 📈 **Market Analyst**
    * 🔍 **Competitor Intelligence**
    * 💼 **Business Strategist**
    * 🎤 **Pitch VC Advisor**
    """)

# Core Generation trigger button
if domain_input:
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_ideas_btn = st.button("Brainstorm Ideas", use_container_width=True)
        
    if generate_ideas_btn:
        with st.spinner("Brainstorming startup ideas..."):
            try:
                ideas = invoke_with_retry(generate_startup_idea, domain_input)
            except Exception:
                st.warning("⚠️ API Rate Limit / Quota fully exhausted. Activating Local Demo Mode...")
                st.session_state.demo_mode = True
                ideas = get_mock_ideas(domain_input)
            
            # Parse numbered/bullet lists
            idea_lines = ideas.split("\n")
            clean_ideas = []
            for idea in idea_lines:
                idea_stripped = idea.strip()
                if idea_stripped:
                    if re.match(r"^\d+[\.\)]", idea_stripped) or re.match(r"^[-*]\s+", idea_stripped):
                        clean_ideas.append(idea_stripped)
            
            # Fallback
            if not clean_ideas:
                clean_ideas = [line.strip() for line in idea_lines if line.strip()]
            
            # Sanitise numberings/bullets
            sanitized_ideas = []
            for idea in clean_ideas:
                clean = re.sub(r"^\d+[\.\)]\s*", "", idea)
                clean = re.sub(r"^[-*]\s*", "", clean)
                sanitized_ideas.append(clean.strip())
            
            st.session_state.ideas_list = sanitized_ideas
            # Reset previous briefs
            st.session_state.market_report = None
            st.session_state.competitor_report = None
            st.session_state.business_report = None
            st.session_state.pitch_report = None

# Render brainstormed ideas list selection
if st.session_state.ideas_list:
    st.markdown("---")
    st.subheader("💡 Brainstormed Startup Concepts")
    selected_option = st.selectbox(
        "Choose an idea to analyze:",
        options=st.session_state.ideas_list
    )
    
    st.session_state.selected_idea = selected_option
    
    col3, col4 = st.columns([2, 3])
    with col3:
        generate_report_btn = st.button("Generate Multi-Agent Analysis Report", use_container_width=True)
        
    if generate_report_btn:
        # Create progress container
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Market Analysis
        status_text.text("📈 Agent 1/4: Analyzing Market Demand...")
        progress_bar.progress(10)
        try:
            if st.session_state.demo_mode:
                market_report = get_mock_market(selected_option)
            else:
                time.sleep(5)
                market_report = invoke_with_retry(analyze_market, selected_option)
        except Exception:
            st.warning("⚠️ API Quota limit reached. Transitioning to Local Demo Mode...")
            st.session_state.demo_mode = True
            market_report = get_mock_market(selected_option)
        st.session_state.market_report = market_report
        
        # Step 2: Competitor Analysis
        status_text.text("🔍 Agent 2/4: Mapping Competitor Gaps...")
        progress_bar.progress(35)
        try:
            if st.session_state.demo_mode:
                competitor_report = get_mock_competitors(selected_option)
            else:
                time.sleep(5)
                competitor_report = invoke_with_retry(analyze_competitors, selected_option)
        except Exception:
            st.session_state.demo_mode = True
            competitor_report = get_mock_competitors(selected_option)
        st.session_state.competitor_report = competitor_report
        
        # Step 3: Business Model Generation
        status_text.text("💼 Agent 3/4: Creating Revenue Strategy...")
        progress_bar.progress(60)
        try:
            if st.session_state.demo_mode:
                business_report = get_mock_business(selected_option)
            else:
                time.sleep(5)
                business_report = invoke_with_retry(
                    generate_business_model,
                    selected_option,
                    market_report,
                    competitor_report
                )
        except Exception:
            st.session_state.demo_mode = True
            business_report = get_mock_business(selected_option)
        st.session_state.business_report = business_report
        
        # Step 4: Pitch Summary
        status_text.text("🎤 Agent 4/4: Writing Elevator Pitch...")
        progress_bar.progress(85)
        try:
            if st.session_state.demo_mode:
                pitch_report = get_mock_pitch(selected_option)
            else:
                time.sleep(5)
                pitch_report = invoke_with_retry(
                    generate_pitch,
                    selected_option,
                    market_report,
                    competitor_report,
                    business_report
                )
        except Exception:
            st.session_state.demo_mode = True
            pitch_report = get_mock_pitch(selected_option)
        st.session_state.pitch_report = pitch_report
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Full report generated successfully!")
        time.sleep(1)
        st.rerun()

# Render Generated Analysis Briefs inside a Tab layout
if st.session_state.market_report:
    st.markdown("---")
    st.success(f"📊 Business Intelligence Brief: **{st.session_state.selected_idea}**")
    
    # Creating responsive tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Market Analysis",
        "🔍 Competitor intelligence",
        "💼 Business Model",
        "🎤 Investor Pitch"
    ])
    
    with tab1:
        st.markdown(f'<div class="content-box"><h3>Market Research</h3>{st.session_state.market_report}</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown(f'<div class="content-box"><h3>Competitive Analysis</h3>{st.session_state.competitor_report}</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown(f'<div class="content-box"><h3>Business & Strategy Model</h3>{st.session_state.business_report}</div>', unsafe_allow_html=True)
        
    with tab4:
        st.markdown(f'<div class="content-box"><h3>Elevator Pitch & Deck Overview</h3>{st.session_state.pitch_report}</div>', unsafe_allow_html=True)
# Create downloadable report
pdf_file = create_pdf_report(
    st.session_state.selected_idea,
    st.session_state.market_report,
    st.session_state.competitor_report,
    st.session_state.business_report,
    st.session_state.pitch_report
)

st.markdown("---")

safe_name = st.session_state.selected_idea.replace(" ", "_")

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_file,
    file_name=f"{safe_name}_report.pdf",
    mime="application/pdf"
)