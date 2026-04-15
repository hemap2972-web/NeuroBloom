def calculate_adaptive_score(stress_level, focus_score):
    # Higher stress reduces score
    stress_impact = (10 - stress_level) * 0.6

    # Focus increases score
    focus_impact = focus_score * 0.4

    adaptive_score = stress_impact + focus_impact
    return round(adaptive_score, 2)


def generate_recommendation(stress_level, focus_score):
    adaptive_score = calculate_adaptive_score(stress_level, focus_score)

    if adaptive_score < 4:
        recommendation = "Critical state. Immediate relaxation and guided therapy recommended."
    elif adaptive_score < 7:
        recommendation = "Moderate state. Recommend mindfulness and focus improvement exercises."
    else:
        recommendation = "Optimal cognitive condition. Suggest advanced brain training challenges."

    return adaptive_score, recommendation

