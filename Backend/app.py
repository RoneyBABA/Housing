from flask import Flask, request, render_template
import pickle
import json
import numpy as np

app = Flask(__name__)

# Load model and columns
model = pickle.load(open('FinalModel.pickle', 'rb'))
columns = json.load(open('columns.json'))['data_colums']


def predict_price(location, sqft, bhk, build_up):
    # Validation checks
    if (sqft / bhk) < 300:
        return None, '❌ Minimum of 300 sqft should be allotted per 1 Bedroom'
    elif (sqft / bhk) > 2000:
        return None, '❌ Maximum of 2000 sqft is allotted per 1 Bedroom'

    # Prepare input vector
    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bhk
    x[2] = sqft / bhk

    # One-hot encode location
    if location.lower() in columns:
        loc_index = columns.index(location.lower())
        x[loc_index] = 1

    # One-hot encode build-up type
    if build_up.lower() in columns:
        build_up_index = columns.index(build_up.lower())
        x[build_up_index] = 1

    # Predict
    pred = float(model.predict([x])[0]) * 100000

    # Format value
    abs_value = abs(pred)
    if abs_value >= 1e7:
        formatted = f"₹ {pred / 1e7:.2f} Cr"
    elif abs_value >= 1e5:
        formatted = f"₹ {pred / 1e5:.2f} L"
    elif abs_value >= 1e3:
        formatted = f"₹ {pred / 1e3:.2f} K"
    else:
        formatted = f"₹ {pred:.2f}"

    return pred, formatted


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        sqft = float(request.form['total_sqft'])
        bhk = int(request.form['bhk'])
        location = request.form['location']
        build_up = request.form['build_up']

        pred, formatted = predict_price(location, sqft, bhk, build_up)

        if pred is None:
            return render_template('index.html', prediction_text=formatted)

        actual_value = f"{pred:,.2f}"  # formatted number with commas and 2 decimals
        return render_template('index.html', 
                               prediction_text=f'🏠 Estimated Price: {formatted}',
                               actual_value=actual_value)
    except Exception as e:
        return render_template('index.html', prediction_text=f'⚠️ Error: {str(e)}')



if __name__ == '__main__':
    app.run(debug=True)
