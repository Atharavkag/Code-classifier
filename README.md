# Code Review Buddy - Your AI-Powered Code Review Assistant 

![Header Banner]((https://github.com/Atharavkag/Code-classifier/blob/main/ChatGPT%20Image%20Apr%2013%2C%202025%2C%2003_32_57%20PM.png))  
*"Elevating code quality through AI-powered insights"*

---

## Project Overview

**Code Review Buddy** is an intelligent web application that provides automated code reviews using large language models (LLMs). It analyzes your code snippets across multiple dimensions and delivers expert-level feedback instantly. 

**Key Highlights:**
- 🧠 **AI-Powered Analysis**: Leverages OpenAI/Gemini-level models for deep code understanding
- 🎨 **Beautiful Glass UI**: Modern glass morphism interface with interactive elements
- 📊 **Multi-Parameter Reviews**: Evaluates code on style, performance, security, and best practices
- 🗃️ **Review History**: Automatically saves all reviews in a local SQLite database

**Disclaimer**: This project was developed through **prompt engineering** - all code was generated by LLMs based on carefully crafted prompts, then assembled into this application.

---

## ✨ Features Deep Dive

### 1. Intelligent Code Analysis
- **Language-Specific Reviews**: Supports 10+ languages (Python, JavaScript, Java, etc.)
- **Custom Focus Areas**:
  - 🐞 Bug Detection
  - 🎨 Code Style
  - ⚡ Performance
  - 🔒 Security
  - 📚 Best Practices
- **Adjustable Depth**:
  - 🔍 Concise
  - ⚖️ Balanced 
  - 📝 Detailed explanations

### 2. Beautiful User Experience
- **Glass Morphism Design**:
  - Frosted glass panels
  - Subtle backdrop blur
  - Elegant color gradients
- **Interactive Elements**:
  - Animated buttons
  - Focus area badges
  - Smooth transitions

### 3. Technical Implementation
- **Backend**:
  - 💾 SQLite database for review history
  - 🔄 Async API calls to LLM providers
  - 🛡️ Error handling and validation
- **Frontend**:
  - 🎛️ Streamlit-powered interface
  - 📱 Fully responsive design
  - 🎨 Custom CSS animations

---

## 🛠️ Technical Architecture

```mermaid
graph TD
    A[User Interface] -->|Code Input| B[Streamlit App]
    B -->|API Call| C[LLM Provider]
    C -->|Structured Feedback| B
    B -->|Save Data| D[SQLite Database]
    D -->|Retrieve History| B
