from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import SessionData
from adaptive_engine import generate_recommendation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "NeuroBloom Backend Running Successfully 🚀"}


@app.post("/analyze")
def analyze(user_name: str, stress_level: float, focus_score: float):
    db = SessionLocal()

    adaptive_score, recommendation = generate_recommendation(stress_level, focus_score)

    session = SessionData(
        user_name=user_name,
        stress_level=stress_level,
        focus_score=focus_score,
        adaptive_score=adaptive_score,
        recommendation=recommendation
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()

    return {
        "user": user_name,
        "adaptive_score": adaptive_score,
        "recommendation": recommendation
    }
@app.get("/user/{user_name}/analytics")
def user_analytics(user_name: str):
    db = SessionLocal()

    sessions = db.query(SessionData).filter(
        SessionData.user_name == user_name
    ).all()

    if not sessions:
        db.close()
        return {"message": "No data found for this user."}

    total_sessions = len(sessions)

    avg_score = db.query(func.avg(SessionData.adaptive_score)) \
        .filter(SessionData.user_name == user_name) \
        .scalar()

    avg_stress = db.query(func.avg(SessionData.stress_level)) \
        .filter(SessionData.user_name == user_name) \
        .scalar()

    # Trend detection (compare last 2 sessions)
    trend = "stable"
    if total_sessions >= 2:
        last_score = sessions[-1].adaptive_score
        prev_score = sessions[-2].adaptive_score

        if last_score > prev_score:
            trend = "improving"
        elif last_score < prev_score:
            trend = "declining"

    # Burnout risk logic
    burnout_risk = "low"
    if avg_stress >= 7:
        burnout_risk = "high"
    elif avg_stress >= 5:
        burnout_risk = "moderate"

    db.close()

    return {
        "user": user_name,
        "total_sessions": total_sessions,
        "average_adaptive_score": round(avg_score, 2),
        "average_stress_level": round(avg_stress, 2),
        "trend": trend,
        "burnout_risk": burnout_risk
    }
