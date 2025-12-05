# PolicyMe Cortex 🛡️

> AI-Powered Insurance Intelligence Platform - Multi-agent fraud detection, risk assessment, and automated underwriting built with React + FastAPI + Gemini AI

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://policyme-cortex.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Overview

PolicyMe Cortex is a cutting-edge InsurTech platform that leverages AI to revolutionize insurance operations. Built with React (frontend) and FastAPI + Gemini AI (backend), it automates claims processing, underwriting, fraud detection, and policy management.

### Key Features

- 🔍 **Claims Hawk-Eye**: AI-powered claim analysis with fraud detection (0-100 risk scoring)
- 📊 **Underwriting AI**: Automated risk assessment and premium calculation  
- ❓ **Policy Q&A (RAG)**: Vector-based policy document search with semantic understanding
- ✅ **Smart Validator**: Rule-based claim validation pipeline
- 🔄 **Agent Workflow**: Multi-agent orchestration for complex decision-making
- 🛒 **Smart Shopper**: Voice-to-application quote generation

## 🏗️ Architecture

```
polcyme-cortex/
├── api/                    # FastAPI Backend
│   ├── main.py            # Main API with Gemini AI integration
│   └── requirements.txt   # Python dependencies
├── src/                   # React Frontend  
│   ├── App.js            # Main application component
│   ├── index.js          # Entry point
│   └── style.css         # Styles
├── public/               # Static assets
└── vercel.json          # Deployment configuration
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Local Development

**1. Clone the repository**
```bash
git clone https://github.com/sghosh685/policyme-cortex.git
cd policyme-cortex
```

**2. Install frontend dependencies**
```bash
npm install
```

**3. Set up backend**
```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
# Create .env in api/ directory
echo "GEMINI_API_KEY=your_gemini_api_key_here" > api/.env
```

**5. Run the application**

Terminal 1 (Backend):
```bash
cd api
uvicorn main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) 🎉

## 🌐 Deployment

### Deploy to Vercel

**1. Install Vercel CLI**
```bash
npm i -g vercel
```

**2. Deploy**
```bash
vercel
```

**3. Set environment variables in Vercel Dashboard**
- Go to Project Settings → Environment Variables
- Add `GEMINI_API_KEY` with your API key

**4. Redeploy**
```bash
vercel --prod
```

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Utility-first styling  
- **Axios** - HTTP client for API calls
- **React Hooks** - State management

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini AI** - LLM for claims analysis and NLP
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📡 API Endpoints

### Claims Analysis
```http
POST /api/claims/analyze
Content-Type: application/json

{
  "incidentData": {
    "location": "Main St, Toronto",
    "dateTime": "2025-12-05T14:00:00Z",
    "description": "Rear-end collision",
    "injuries": false,
    "propertyDamage": true,
    "claimedAmount": 4500
  },
  "policyId": "POL-001"
}
```

**Response:**
```json
{
  "claim_id": "CLM-20251205140000",
  "status": "approved",
  "fraud_score": {
    "score": 15.0,
    "risk_level": "Low",
    "confidence": 0.85,
    "indicators": []
  },
  "ai_analysis": {
    "validity": "valid",
    "recommendation": "auto_approve",
    "estimated_payout": 4500,
    "red_flags": [],
    "reasoning": "Standard claim with no red flags"
  }
}
```

### Dashboard Stats
```http
GET /api/dashboard/stats
```

### Health Check
```http
GET /health
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes |
| `REACT_APP_API_URL` | Backend API URL | No (defaults to localhost) |

## 📈 Features in Detail

### Claims Hawk-Eye
- Real-time fraud risk scoring (0-100 scale)
- AI-powered claim validity assessment
- Automated approval for low-risk claims
- Multi-factor fraud indicators

### Underwriting AI  
- Extract structured data from broker notes
- Dynamic risk profiling
- Automated premium calculation
- Medical condition analysis

### Policy Q&A (RAG)
- Upload policy PDFs
- Vector-based semantic search
- Natural language Q&A
- Citation of policy sections

### Smart Validator
- Hard rule validation (policy status, limits)
- Soft rule AI checks (exclusions)
- Multi-step pipeline visualization
- Instant feedback on claim validity

### Agent Workflow
- Multi-agent orchestration
- Document ingestion → Investigation → Adjudication
- Automated consensus building
- Risk-based routing

### Smart Shopper
- Voice-to-text application intake
- Real-time form population
- Instant quote generation
- Conversion optimization

## 🎯 Roadmap

- [ ] Add PostgreSQL database integration
- [ ] Implement user authentication (JWT)
- [ ] Build admin dashboard
- [ ] Add real-time notifications
- [ ] Integrate with insurance carrier APIs
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and reporting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 👤 Author

**Saikat Ghosh**
- GitHub: [@sghosh685](https://github.com/sghosh685)
- Portfolio: [Your Portfolio URL]
- LinkedIn: [Your LinkedIn]

## 🙏 Acknowledgments

- Google Gemini AI for LLM capabilities
- Vercel for seamless deployment
- React community for amazing tools

---

⭐ Star this repo if you find it useful!

**Live Demo**: [policyme-cortex.vercel.app](https://policyme-cortex.vercel.app)
