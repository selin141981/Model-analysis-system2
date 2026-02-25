def predict_model(user_tokens):
    if user_tokens < 5:
        return {"error": "Not enough tokens", "tokens": user_tokens}

    # כאן תוכלי לקרוא לפונקציית predict מהחלק הראשון אם יש
    user_tokens -= 5
    return {"message": "Prediction done", "tokens": user_tokens}
