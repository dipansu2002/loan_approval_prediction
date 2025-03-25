from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("Random_Forest.pkl")

# Define the required feature order
REQUIRED_FEATURES = ["Gender", "Married", "Dependents", "Education", "Credit_Card_Debt","Employment_Type"]

# Define categorical mappings
label_mapping = {
    "Gender": {"Male": 1, "Female": 0},
    "Married": {"Yes": 1, "No": 0},
    "Education": {"Graduate": 1, "Not Graduate": 0},
    "Employment_Type": {"Salaried": 0, "Self-Employed": 1, "Unemployed": 2}
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not all(feature in data for feature in REQUIRED_FEATURES):
            return jsonify({"error": "Missing required fields"}), 400

        input_df = pd.DataFrame([data])

        for col, mapping in label_mapping.items():
            if col in input_df.columns:
                input_df[col] = input_df[col].map(mapping)

        input_df = input_df[REQUIRED_FEATURES]

        prediction = model.predict(input_df)[0]
        result = "Approved" if prediction == 1 else "Rejected"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
