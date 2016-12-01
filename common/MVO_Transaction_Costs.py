import numpy as np
from Return_Data_Collector import get_asset_return_data,get_SP500, get_market_portfolio_weights
import cvxpy
import pandas as pd

def mvoptimization(df_return, risk_limit, wealth=1):
    # expected return found by calculating the mean of each stock (sample mean)
    expected_return = df_return.mean()
    # covariance found by caluculating the covariance across different samples
    covariance = df_return.cov()
    num_assets = len(covariance)
    name_asset = covariance.columns

    # Initialize the weight variable that we are trying to find
    w = cvxpy.Variable(num_assets)
    # Input the return we get from the sample mean
    Return = np.matrix(expected_return.values)
    # Q as the covariance matrix
    Q = np.matrix(covariance.values)
    # Call the quadratic equation risk
    risk = cvxpy.quad_form(w, Q)

    # List of constraints
    constraints = list()
    # Budget Constraint
    constraints.append(cvxpy.sum_entries(w) == 1)
    # Risk Constraint
    constraints.append(risk <= risk_limit)
    # Long only Constraint, could be turned off
    constraints.append(w >= 0)
    # Objective Function
    objective = cvxpy.Maximize(Return*w)

    # Setting up the problem
    prob = cvxpy.Problem(objective, constraints)
    prob.solve(solver='CVXOPT', verbose=True)

    print("Risk of: {0}".format(np.sqrt(risk.value)))
    weights = pd.DataFrame(w.value, index=name_asset, columns=['Holding'])

    return np.round(weights, decimals=2) # Round to two significant digits

if __name__ == "__main__":
    SP500 = get_SP500()
    market_portflio_weights = get_market_portfolio_weights(SP500,3)
    #list_assets = list(["GOOG", "AAPL", "AMZN", "FB", "TSLA", "UWTI", "NFLX", "TVIX"] )
    list_assets = list(market_portflio_weights['Symbol'])
    result = get_asset_return_data(list_assets)
    optimal_weights = mvoptimization(result['df_return'], 0.05)
    print optimal_weights