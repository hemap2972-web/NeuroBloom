from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend working"}

@app.post("/analyze")
def analyze(user_name: str, stress_level: int, focus_score: int):
    
    adaptive_score = (focus_score * 0.6) + ((10 - stress_level) * 0.4)

    if adaptive_score > 7:
        recommendation = "High performance"
    elif adaptive_score > 4:
        recommendation = "Moderate, needs improvement"
    else:
        recommendation = "High stress, needs attention"

    return {
        "user": user_name,
        "adaptive_score": adaptive_score,
        "recommendation": recommendation
    }