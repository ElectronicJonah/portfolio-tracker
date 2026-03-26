import yfinance as yf
import numpy as np


# Fetch stock data
def get_current_price(ticker): # for portfolio
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d")
    if history.empty:
        return None

    return history["Close"].iloc[-1] # last row

def get_historical_prices(ticker, period="6mo"): # for plots
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    return history["Close"]

def get_daily_returns(ticker, period="5y"): # for simulation
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    returns = history["Close"].pct_change().dropna() # is relative change from t-1, so t1 is dropped

    return returns


# Portfolio Calculations
def calculate_current_value(asset, current_price): # access asset through portfolio
    return asset["quantity"] * current_price

def calculate_transaction_value(asset):
    return asset["quantity"] * asset["purchase_price"]

def calculate_gain_loss(asset, current_price):
    transaction_value = asset["quantity"] * asset["purchase_price"]
    current_value = asset["quantity"] * current_price
    return current_value - transaction_value

def calculate_total_invested_value(portfolio):
    total = 0
    for asset in portfolio:
        total += asset["quantity"] * asset["purchase_price"]
    return total

def calculate_portfolio_weights(portfolio):
    total_current_value = 0
    weights = {}

    for asset in portfolio: # store current value of each ticker in dict
        current_price = get_current_price(asset["ticker"])
        current_value = calculate_current_value(asset, current_price)
        total_current_value += current_value
        weights[asset["ticker"]] = current_value # adds each ticker and corresponding value

    for ticker in weights: # convert raw values to weights
        weights[ticker] = weights[ticker] / total_current_value

    return weights

def calculate_sector_weights(portfolio):
    sector_values = {}
    total_current_value = 0

    for asset in portfolio:
        current_price = get_current_price(asset["ticker"])
        current_value = calculate_current_value(asset, current_price)
        sector = asset["sector"] # String

        if sector not in sector_values:
            sector_values[sector] = 0 # create entry for new sectors
        sector_values[sector] += current_value
        total_current_value += current_value

    return {sector: value / total_current_value for sector, value in sector_values.items()}
# Unpacked for clarity
# result = {}
# for sector, value in sector_values.items(): # loop over dict getting key(string) and value at once with .items()
#     result[sector] = value / total_current_value
# return result # dict with each sector name and corresponding value

def calculate_asset_class_weights(portfolio): # exact same logic as above
    asset_class_values = {}
    total_current_value = 0

    for asset in portfolio:
        current_price = get_current_price(asset["ticker"])
        current_value = calculate_current_value(asset, current_price)
        asset_class = asset["asset_class"]

        if asset_class not in asset_class_values:
            asset_class_values[asset_class] = 0
        asset_class_values[asset_class] += current_value
        total_current_value += current_value

    return {asset_class: value / total_current_value for asset_class, value in asset_class_values.items()}

# Simulation
def estimate_portfolio_parameters(portfolio, period="5y"):
    weights = calculate_portfolio_weights(portfolio)
    portfolio_returns = None # series (same as get_daily_returns)

    for asset in portfolio: # store 1260 daily returns for each asset, cumulative
        ticker = asset["ticker"]
        returns = get_daily_returns(ticker, period)

        weighted_returns = returns * weights[ticker]

        if portfolio_returns is None: # crash without since initialized variable w/ None has no .add
            portfolio_returns = weighted_returns
        else:
            portfolio_returns = portfolio_returns.add(weighted_returns, fill_value=0)

    mu = portfolio_returns.mean()
    sigma = portfolio_returns.std()

    return mu, sigma


def monte_carlo_simulation(portfolio, forecast_years=15, simulations=100000, period="5y"): # assumption of normal distribution
    mu, sigma = estimate_portfolio_parameters(portfolio, period)

    trading_days = 252
    total_days = forecast_years * trading_days
    initial_value = calculate_total_invested_value(portfolio)

    daily_returns = np.random.normal(mu, sigma, (total_days, simulations)) # 2D array
    price_paths = np.cumprod(1 + daily_returns, axis=0)  # cumulative product column, each final value = growth factor from day 0 to that day

    simulation_results = np.vstack([
        np.ones(simulations) * initial_value, # row 0: starting portfolio value for all simulations
        price_paths * initial_value # rows 1-3780: growth factors converted to portfolio values
    ])

    return simulation_results # 3781 x 100.000 matrix with simulated price path in dollars
