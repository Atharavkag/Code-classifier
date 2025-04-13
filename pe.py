import streamlit as st
import sqlite3
from openai import OpenAI

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("code_reviews.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS reviews
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              language TEXT, 
              code TEXT,
              feedback TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Code Review Buddy",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    :root {
        --primary: #4361ee;
        --secondary: #3a0ca3;
        --accent: #4895ef;
        --dark: #1b263b;
        --light: #f8f9fa;
        --success: #4cc9f0;
        --warning: #f72585;
        --card-bg: #ffffff;
    }
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
    }
    
    .main-title {
        color: var(--dark);
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        line-height: 1.2;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        text-align: center;
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Form container */
    .stForm {
        background-color: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Code input area */
    .stTextArea textarea {
        font-family: 'Fira Code', monospace !important;
        font-size: 14px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        line-height: 1.6;
    }
    
    /* Select boxes */
    .stSelectbox div, .stMultiselect div {
        border-radius: 10px !important;
    }
    
    /* Buttons */
    .stButton>button {
        font-size: 1.1rem;
        background: linear-gradient(45deg, var(--primary), var(--accent));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.25);
        background: linear-gradient(45deg, var(--secondary), var(--primary));
    }
    
    /* Feedback section */
    .feedback-container {
        background-color: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        border-left: 4px solid var(--accent);
    }
    
    /* Icons and labels */
    .input-label {
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.5rem;
        display: block;
        font-size: 1rem;
    }
    
    /* Explanation options */
    .explanation-option {
        display: flex;
        gap: 12px;
        align-items: center;
        padding: 12px 16px;
        border-radius: 10px;
        background: #f8fafc;
        margin-bottom: 8px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .explanation-option:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
    }
    
    .explanation-option.selected {
        background: #e0e7ff;
        border-color: var(--primary);
    }
    
    /* Responsive columns */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading-text {
        animation: pulse 1.5s infinite;
        text-align: center;
        font-size: 1.2rem;
        color: var(--primary);
    }
    
    /* Badges for focus areas */
    .focus-badge {
        display: inline-block;
        padding: 4px 10px;
        background: #e0e7ff;
        color: var(--primary);
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>Code Review Buddy</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Get expert-level code reviews with clear, actionable feedback to improve your programming skills</div>", unsafe_allow_html=True)

# ---------- USER INPUT ----------
with st.form("code_review_form"):
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<span class='input-label'>🖥️ Programming Language</span>", unsafe_allow_html=True)
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript", "C#", "Swift", "Kotlin"],
            label_visibility="collapsed",
            index=0
        )
        
        st.markdown("<span class='input-label'>📝 Paste Your Code Below</span>", unsafe_allow_html=True)
        code = st.text_area(
            "Code Input",
            height=350,
            placeholder="Example:\ndef hello():\n    print('Hello, world!')\n    # Add your code here...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<span class='input-label'>🔍 Focus Areas for Review</span>", unsafe_allow_html=True)
        review_focus = st.multiselect(
            "Focus Areas",
            ["Bug Detection", "Code Style", "Performance", "Security", 
             "Best Practices", "Readability", "Maintainability", "Error Handling",
             "Documentation", "Testing"],
            default=["Best Practices", "Code Style"],
            label_visibility="collapsed"
        )
        
        st.markdown("<span class='input-label'>📘 Explanation Level</span>", unsafe_allow_html=True)
        
        # Radio buttons styled as cards for explanation level
        explanation_level = st.radio(
            "Explanation Level",
            ["Concise", "Balanced", "Detailed"],
            index=1,
            label_visibility="collapsed",
            horizontal=True,
            key="explanation_level"
        )
        
        st.markdown("""
            <div style="margin-top: 1.5rem; padding: 1.2rem; background-color: #f8fafc; 
                        border-radius: 12px; border-left: 4px solid var(--accent);">
                <p style="margin: 0; color: var(--dark); font-size: 0.9rem; line-height: 1.6;">
                    <span style="font-weight: 600; color: var(--primary);">💡 Pro Tip:</span> 
                    For complex code, include comments about your intent. This helps the AI provide more relevant feedback.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    submit = st.form_submit_button("Get Code Review", type="primary")

# ---------- OPENROUTER API FUNCTION ----------
def call_openrouter(prompt):
    client = OpenAI(
        api_key="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",  # Replace securely in production
        base_url="https://openrouter.ai/api/v1"
    )
    try:
        response = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API Error: {str(e)}"

# ---------- ON SUBMIT ----------
if submit and code.strip():
    focus_text = ", ".join([f"<span class='focus-badge'>{f}</span>" for f in review_focus]) if review_focus else "general code quality"
    prompt = f"""You are an expert {language} developer with 15+ years of experience.
Please review the following code with a focus on: {', '.join(review_focus) if review_focus else 'general code quality'}.
Provide feedback in a {explanation_level.lower()} manner, structured as follows:

1. **Code Summary**: Brief explanation of what the code does
2. **Strengths**: What's working well in the implementation
3. **Areas for Improvement**: Specific, actionable suggestions
4. **Recommendations**: Concrete steps to improve the code

For each suggestion, include:
- Importance level (Low/Medium/High)
- Estimated effort to implement (Quick/Moderate/Extensive)
- Code examples when applicable

Code:
{code}
"""
    
    with st.spinner():
        st.markdown("<div class='loading-text'>Analyzing your code with expert precision...</div>", unsafe_allow_html=True)
        feedback = call_openrouter(prompt)
    
    with st.container():
        st.markdown(f"""
            <div class='feedback-container'>
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.5rem;">
                    <h2 style='color: var(--primary); margin: 0;'>🤖 AI Code Review</h2>
                    <div style="font-size: 0.9rem; background: #e0e7ff; color: var(--primary); 
                                padding: 4px 10px; border-radius: 20px; font-weight: 500;">
                        {language}
                    </div>
                </div>
                <div style="margin-bottom: 1rem;">
                    <span style="font-weight: 600; color: var(--dark);">Focus Areas:</span>
                    {focus_text if review_focus else '<span class="focus-badge">General Review</span>'}
                </div>
                <div style='margin-top: 1rem; line-height: 1.8; color: var(--dark);'>
        """, unsafe_allow_html=True)
        
        st.markdown(feedback, unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Save to database
    c.execute("INSERT INTO reviews (language, code, feedback) VALUES (?, ?, ?)",
              (language, code, feedback))
    conn.commit()