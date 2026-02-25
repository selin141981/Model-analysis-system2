"""
הקוד מריץ את החלק השני של הפרויקט
שבו יש שתי פעולות עיקריות: אימון מודל וחיזוי.
"""


from logic.train_logic import train_model
from logic.predict_logic import predict_model


def run_part2():
    user_tokens = 10

    train_result = train_model(user_tokens)
    user_tokens = train_result.get("tokens", user_tokens)

    predict_result = predict_model(user_tokens)

    return {
        "train": train_result,
        "predict": predict_result
    }


if __name__ == "__main__":
    result = run_part2()
    print(result)
