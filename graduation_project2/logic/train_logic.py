def train_model(user_tokens):
    if user_tokens < 1:
        return {"error": "Not enough tokens", "tokens": user_tokens}

    # כאן תוכלי לקרוא לפונקציה האמיתית מהחלק הראשון אם רוצים
    user_tokens -= 1
    return {"message": "Training done", "tokens": user_tokens}
