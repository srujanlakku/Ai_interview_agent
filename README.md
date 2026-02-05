# 🎯 AI Interview Agent

A stunning, production-ready AI-powered technical interview preparation platform with a modern glassmorphism UI design.

## ✨ Features

- **🤖 AI-Powered Interviewer** - Intelligent question selection with OpenAI integration
- **📈 Adaptive Difficulty** - Questions adjust based on your performance
- **💡 Real-time Feedback** - Get detailed evaluation and improvement suggestions
- **🎯 Role-Specific Questions** - Tailored for 10+ technical roles
- **📊 Comprehensive Results** - Score breakdown with strengths and weaknesses
- **🎨 Modern UI** - Beautiful glassmorphism design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/srujanlakku/Ai_interview_agent.git
cd Ai_interview_agent
```

2. **Set up the backend**
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Create .env file in the backend folder
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
   - Navigate to: http://localhost:8501

## 📁 Project Structure

```
Interview-agent/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI agents (question selector, evaluator)
│   │   │   ├── base_agent.py
│   │   │   ├── evaluation_agent.py
│   │   │   └── question_selector_agent.py
│   │   ├── data/             # Question repository
│   │   │   └── question_repository.py
│   │   ├── memory/           # Session memory management
│   │   │   ├── memory_manager.py
│   │   │   └── interview_memory.py
│   │   ├── schemas/          # Data models
│   │   └── utils/            # Utilities
│   ├── pages/                # Streamlit pages
│   │   ├── home_page.py      # Landing page
│   │   ├── login_page.py     # Profile setup
│   │   ├── interview_page.py # Interview interface
│   │   └── results_page.py   # Results dashboard
│   ├── app.py                # Main Streamlit entry point
│   ├── requirements.txt
│   └── .env                  # Environment configuration
└── frontend/                 # Original React frontend (alternative)
```

## 🎮 How to Use

1. **Start the App** - Run `streamlit run app.py`
2. **Set Up Profile** - Enter your name, select role and experience level
3. **Take Interview** - Answer AI-generated questions one at a time
4. **Get Feedback** - Receive real-time evaluation on each answer
5. **View Results** - See comprehensive score breakdown and recommendations

## 🎭 Supported Roles

- Backend Engineer
- Frontend Engineer
- Full Stack Developer
- DevOps Engineer
- AI/ML Engineer
- Data Engineer
- Mobile Developer
- Security Engineer
- Database Engineer
- QA Engineer
- Cloud Architect
- System Administrator

## 📊 Experience Levels

- **Junior (0-2 years)** - Entry-level questions, fundamental concepts
- **Mid-level (2-5 years)** - Intermediate complexity, system design basics
- **Senior (5-8 years)** - Advanced questions, architecture & leadership
- **Principal (8+ years)** - Expert-level, strategic & complex scenarios

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional
INTERVIEW_MAX_QUESTIONS=8
LOG_LEVEL=INFO
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS (glassmorphism design)
- **Backend**: Python 3.10+, AsyncIO
- **AI**: OpenAI GPT-4/GPT-3.5 API
- **State Management**: Streamlit session state
- **Styling**: Custom CSS with animations

## 📝 API Usage

The app uses the following OpenAI API calls:
- **Question Generation** - When local repository is exhausted
- **Answer Evaluation** - For each submitted answer

Estimated cost: ~$0.05-0.10 per full interview session (8 questions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary. All rights reserved.

## 💬 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ for interview success**
