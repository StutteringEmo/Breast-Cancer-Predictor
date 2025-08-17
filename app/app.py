from flask import Flask, render_template, request
import joblib, json, numpy as np, os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.json")

pipe = joblib.load(MODEL_PATH)
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

FEATURES = schema["feature_order"]
LABELS = schema.get("target_labels", {0:"benign",1:"malignant"})

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", features=FEATURES)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        vals = [request.form.get(feat, type=float) for feat in FEATURES]
        x = np.array(vals, dtype=float).reshape(1, -1)
        pred = int(pipe.predict(x)[0])
        proba = getattr(pipe, "predict_proba", None)
        prob = float(proba(x)[0, pred]) if proba else None
        label = LABELS.get(str(pred), LABELS.get(pred, "unknown"))
        return render_template(
            "result.html",
            label=label,
            prob=prob,
            model_name=schema.get("selected_model"),
            test_acc=schema.get("test_accuracy")
        )
    except Exception as e:
        return render_template("error.html", error=str(e)), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
