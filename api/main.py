# api/main.py - FastAPI backend with Gemini AI integration
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import os
import google.generativeai as genai

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

app = FastAPI(
    title="PolicyMe Cortex API",
    description="AI-powered insurance intelligence platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class IncidentData(BaseModel):
    location: str
    dateTime: str
    description: str
    injuries: bool = False
    propertyDamage: bool = False
    claimedAmount: Optional[float] = 0.0

class ClaimAnalysisRequest(BaseModel):
    incidentData: IncidentData
    policyId: Optional[str] = "POL-001"

class FraudScore(BaseModel):
    score: float
    risk_level: str
    indicators: List[str]
    confidence: float

class AIAnalysis(BaseModel):
    validity: str
    recommendation: str
    estimated_payout: float
    red_flags: List[str]
    reasoning: str

class ClaimAnalysisResponse(BaseModel):
    claim_id: str
    fraud_score: FraudScore
    ai_analysis: AIAnalysis
    status: str
    created_at: str

# Helper functions
def calculate_fraud_score(incident: IncidentData) -> FraudScore:
    """Calculate fraud risk score using rule-based system"""
    score = 0.0
    indicators = []
    
    # High claimed amount relative to description
    if incident.claimedAmount > 50000:
        score += 25
        indicators.append("High claim amount")
    
    # Vague or suspicious description
    if len(incident.description) < 50:
        score += 15
        indicators.append("Insufficient details")
    elif any(word in incident.description.lower() for word in ['stolen', 'total loss', 'fire', 'flood']):
        score += 20
        indicators.append("High-risk incident type")
    
    # Weekend/holiday timing (simplified)
    try:
        incident_dt = datetime.fromisoformat(incident.dateTime.replace('Z', '+00:00'))
        if incident_dt.weekday() >= 5:  # Saturday or Sunday
            score += 10
            indicators.append("Weekend incident")
    except:
        pass
    
    # Both injuries and property damage
    if incident.injuries and incident.propertyDamage:
        score += 15
        indicators.append("Multiple damage types")
    
    # Location anomalies (placeholder logic)
    if not incident.location or len(incident.location) < 5:
        score += 10
        indicators.append("Vague location")
    
    score = min(score, 100.0)
    
    if score < 30:
        risk_level = "Low"
        confidence = 0.85
    elif score < 60:
        risk_level = "Medium"
        confidence = 0.75
    else:
        risk_level = "High"
        confidence = 0.90
    
    return FraudScore(
        score=round(score, 2),
        risk_level=risk_level,
        indicators=indicators,
        confidence=confidence
    )

async def ai_analyze_claim(incident: IncidentData, fraud_score: FraudScore) -> AIAnalysis:
    """Use Gemini AI to analyze claim validity and provide recommendations"""
    
    if not GEMINI_API_KEY:
        # Fallback logic when API key is not configured
        validity = "needs_review" if fraud_score.score > 40 else "valid"
        recommendation = "manual_review" if fraud_score.score > 40 else "auto_approve"
        estimated = incident.claimedAmount * (0.6 if fraud_score.score > 60 else 0.85)
        
        return AIAnalysis(
            validity=validity,
            recommendation=recommendation,
            estimated_payout=round(estimated, 2),
            red_flags=fraud_score.indicators,
            reasoning="Automated analysis based on rule-based system. Configure GEMINI_API_KEY for advanced AI insights."
        )
    
    # Use Gemini AI for advanced analysis
    prompt = f"""You are an insurance claims adjuster AI. Analyze this claim:

Incident Details:
- Location: {incident.location}
- Date/Time: {incident.dateTime}
- Description: {incident.description}
- Injuries Reported: {incident.injuries}
- Property Damage: {incident.propertyDamage}
- Claimed Amount: ${incident.claimedAmount}

Fraud Risk Score: {fraud_score.score}/100 ({fraud_score.risk_level} risk)
Fraud Indicators: {', '.join(fraud_score.indicators)}

Provide your analysis in this exact JSON format:
{{
    "validity": "valid" or "questionable" or "invalid",
    "recommendation": "auto_approve" or "manual_review" or "reject",
    "estimated_payout": numeric value,
    "red_flags": ["flag1", "flag2"],
    "reasoning": "brief explanation"
}}

Be concise and objective."""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Parse JSON from response
        import json
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]
        
        ai_result = json.loads(result_text.strip())
        
        return AIAnalysis(
            validity=ai_result.get("validity", "needs_review"),
            recommendation=ai_result.get("recommendation", "manual_review"),
            estimated_payout=float(ai_result.get("estimated_payout", incident.claimedAmount * 0.8)),
            red_flags=ai_result.get("red_flags", fraud_score.indicators),
            reasoning=ai_result.get("reasoning", "AI analysis completed")
        )
    except Exception as e:
        print(f"Gemini AI error: {e}")
        # Fallback to rule-based
        validity = "needs_review" if fraud_score.score > 40 else "valid"
        recommendation = "manual_review" if fraud_score.score > 40 else "auto_approve"
        estimated = incident.claimedAmount * (0.6 if fraud_score.score > 60 else 0.85)
        
        return AIAnalysis(
            validity=validity,
            recommendation=recommendation,
            estimated_payout=round(estimated, 2),
            red_flags=fraud_score.indicators,
            reasoning=f"AI analysis fallback due to error: {str(e)}"
        )

# API Routes
@app.get("/")
async def root():
    return {
        "message": "PolicyMe Cortex API",
        "version": "1.0.0",
        "status": "operational",
        "ai_enabled": bool(GEMINI_API_KEY)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.post("/api/claims/analyze", response_model=ClaimAnalysisResponse)
async def analyze_claim(request: ClaimAnalysisRequest):
    """Analyze insurance claim for fraud and validity"""
    
    # Calculate fraud score
    fraud_score = calculate_fraud_score(request.incidentData)
    
    # Get AI analysis
    ai_analysis = await ai_analyze_claim(request.incidentData, fraud_score)
    
    # Determine claim status
    if ai_analysis.recommendation == "auto_approve" and fraud_score.score < 30:
        status = "approved"
    elif ai_analysis.recommendation == "reject" or fraud_score.score > 80:
        status = "flagged"
    else:
        status = "processing"
    
    # Generate claim ID
    claim_id = f"CLM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    return ClaimAnalysisResponse(
        claim_id=claim_id,
        fraud_score=fraud_score,
        ai_analysis=ai_analysis,
        status=status,
        created_at=datetime.utcnow().isoformat()
    )

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics (mock data for now)"""
    return {
        "active_claims": 247,
        "fraud_detected": 12,
        "processing_time": "2.3s",
        "approval_rate": 78.5,
        "total_payout": 1250000.00,
        "risk_distribution": {
            "low": 156,
            "medium": 73,
            "high": 18
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
