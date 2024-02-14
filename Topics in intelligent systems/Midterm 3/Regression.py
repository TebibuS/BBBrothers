import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr

# Given data
x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6]).reshape((-1, 1))
y = np.array([99, 90, 87, 88, 111, 91, 103, 87, 94, 78, 77, 85, 86])

# (a) Solve and Print the Simple Linear Regression Equation
model = LinearRegression().fit(x, y)
intercept = model.intercept_
slope = model.coef_[0]
regression_eq = f"y = {slope:.2f}x + {intercept:.2f}"

# (b) Solve and Print the Pearson Correlation Coefficient (r)
pearson_r, _ = pearsonr(x.flatten(), y)

# (c) Solve and Print the RMSE or std_error
y_pred = model.predict(x)
rmse = np.sqrt(mean_squared_error(y, y_pred))

# (d) Predict the Speed of a Car with age 10 years old
predicted_speed = model.predict(np.array([[10]]))[0]

regression_eq, pearson_r, rmse, predicted_speed
