## 🏠 Bangalore House Price Prediction

This project predicts real estate prices (houses, apartments, and plots) across **Bangalore**, using data from [this Kaggle dataset](https://www.kaggle.com/datasets/sumanbera19/bengaluru-house-price-dataset).

This project helped me understand real-world data workflows and made me more adaptable and eager to grow in the **data science and ML** domain.

---

## 💡 Project Overview

* Trained a **Linear Regression model** to estimate property prices based on features like total area, number of bedrooms, and location.
* Preprocessed for inconsistent or noisy data through various data pipelines
* Compared the performance of **Lasso Regression** and **Decision Tree Regression** using **GridSearchCV**.
* Used **Cross-Validation** and **ShuffleSplit** to evaluate model consistency.
* Linear Regression performed best overall, balancing accuracy and interpretability.
* Exports trained model as `FinalModel.pickle` for reuse

---

## ⚙️ Tech Stack

* **Python 3**
* **Pandas** for data manipulation
* **NumPy** for numerical operations
* **Matplotlib** for visualization
* **Scikit-learn** for model training

---

## 🚀 Usage

To use the model in your project:

```python
import pickle

with open('FinalModel.pickle', 'rb') as f:
    model = pickle.load(f)

# Example input
features = ['Indira Nagar', 1102, 3,'Carpet Area'] /['location',total_sqft, bhk, 'Build Type']
predicted_price = model.predict([features])
print(predicted_price)
```
---

## 📩 Contact

If you have an **updated dataset**, feel free to reach out!

I’m happy to **retrain** the model and improve its performance.

If you’d like to collaborate or to suggest improvements, feel free to ping me — I’m always open to learning and feedback.

---

## 🪪 License

You are free to use the trained model (`FinalModel.pickle`) for **personal or educational purposes**.

Please credit this repository if you build upon it.

