from flask import Flask, render_template, request
import pickle, json, numpy as np

app = Flask(__name__)

# Load model and metadata
model = pickle.load(open('FinalModel.pickle', 'rb'))
columns = json.load(open('columns.json'))['data_colums']

# ---------- Core Prediction Function ----------
def predict_price(location, sqft, bhk, build_up):
    if (sqft/bhk) < 300:
        return None, '❌ Minimum of 300 sqft should be allotted per bedroom'
    elif (sqft/bhk) > 2000:
        return None, '❌ Maximum of 2000 sqft allowed per bedroom'

    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bhk
    x[2] = sqft/bhk

    if location.lower() in columns:
        x[columns.index(location.lower())] = 1
    if build_up.lower() in columns:
        x[columns.index(build_up.lower())] = 1

    pred = float(model.predict([x])[0]) * 100000
    abs_value = abs(pred)
    if abs_value >= 1e7:
        formatted = f"₹ {pred/1e7:.2f} Cr"
    elif abs_value >= 1e5:
        formatted = f"₹ {pred/1e5:.2f} L"
    else:
        formatted = f"₹ {pred:.2f}"
    return pred, formatted


# ---------- Routes ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text, actual_value = None, None
    if request.method == 'POST':
        sqft = float(request.form['total_sqft'])
        bhk = int(request.form['bhk'])
        location = request.form['location']
        build_up = request.form['build_up']
        pred, formatted = predict_price(location, sqft, bhk, build_up)
        if pred is not None:
            prediction_text = f"🏠 Estimated Price: {formatted}"
            actual_value = f"{pred:,.2f}"
        else:
            prediction_text = formatted

    return render_template('index.html',
                           prediction_text=prediction_text,
                           actual_value=actual_value,
                           request=request)


if __name__ == '__main__':
    app.run(debug=True)
