from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model
model = pickle.load(open("best_nids_model.pkl", "rb"))

# Define the selected features
selected_features = [
    "Flow Duration", "Protocol", "Tot Fwd Pkts", "Tot Bwd Pkts", 
    "Fwd Pkt Len Max", "Bwd Pkt Len Max", "Flow Byts/s", "Flow Pkts/s", 
    "Hour", "Minute", "Second"
]
lab=['Benign','FTP-BruteForce','SSH-Bruterorce']
@app.route("/")
def home():
    return render_template("index.html")  # Ensure "index.html" is the HTML form

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form values as a list of floats
        values = [float(request.form[feature]) for feature in selected_features]

        # Convert to a NumPy array and reshape for model input
        input_array = np.array(values).reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_array)[0]

        # Return the prediction result
        return render_template("index.html", prediction=lab[prediction])

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
    