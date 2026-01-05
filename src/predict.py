import pandas as pd
import joblib

# ---------------- LOAD MODEL & ENCODER ----------------
model = joblib.load("models/best_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


def predict_alert(magnitude, depth, cdi, mmi, sig):
    """
    Predict earthquake alert level and compute
    realistic risk & aftershock metrics.
    """

    # ---------------- RISK SCORE CALCULATION ----------------
    # Weighted formula aligned with seismic reality
    risk_score = (
    magnitude * 8 +          # magnitude impact
    (10 - min(depth / 100, 10)) * 4 +   # depth impact
    mmi * 4 +                # shaking intensity
    (sig / 200)              # significance
)

    risk_score = min(risk_score, 100)


    # ---------------- AFTERSHOCK PROBABILITY ----------------
    aftershock_prob = (
        (magnitude / 9) * 0.6 +
        (1 - min(depth / 300, 1)) * 0.4
    )

    # Cap probability between 0 and 1
    aftershock_prob = max(0, min(aftershock_prob, 1))

    # ---------------- ML MODEL INPUT ----------------
    # IMPORTANT: Must match training features EXACTLY
    input_df = pd.DataFrame([{
        "magnitude": magnitude,
        "depth": depth,
        "cdi": cdi,
        "mmi": mmi,
        "sig": sig
    }])

    # ---------------- PREDICTION ----------------
    pred_encoded = model.predict(input_df)
    probabilities = model.predict_proba(input_df)

    alert = label_encoder.inverse_transform(pred_encoded)[0]
    confidence = probabilities[0].max()

    # ---------------- RETURN RESULTS ----------------
    return (
        alert,
        round(risk_score, 1),
        round(confidence * 100, 1),
        round(aftershock_prob * 100, 1)
    )
