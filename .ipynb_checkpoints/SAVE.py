import yfinance as yf
import matplotlib.pyplot as plt
import tabulate as t
import numpy as np


portfolio = []

## HELPER FUNCTIONS

# Retrieve stock data
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d")

    if history.empty:
        return None

    return history["Close"].iloc[-1] # WHY ILOC???

def get_historical_prices(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    if history.empty:
        return None

    return history["Close"]

# Plots
def plot_portfolio_tickers(portfolio, period="6mo"):
    plt.figure(figsize=(12,6))

    for asset in portfolio:
        ticker = asset["ticker"]
        prices = get_historical_prices(ticker, period)
        plt.plot(prices.index, prices.values, label=ticker)

    plt.title("price history")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Simulation
def get_daily_returns(ticker, period="5y"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    returns = history["Close"].pct_change().dropna()

    return returns

def calculate_portfolio_weights(portfolio):
    total_current_value = 0
    weights = {}

    for asset in portfolio:
        current_price = get_current_price(asset["ticker"])

        current_value = calculate_current_value(asset, current_price)
        total_current_value += current_value
        weights[asset["ticker"]] = current_value

    for ticker in weights:
        weights[ticker] = weights[ticker] / total_current_value

    return weights


def estimate_portfolio_parameters(portfolio, period="5y"):
    weights = calculate_portfolio_weights(portfolio)
    portfolio_returns = None

    for asset in portfolio:
        ticker = asset["ticker"]
        returns = get_daily_returns(ticker, period)

        weighted_returns = returns * weights[ticker]

        if portfolio_returns is None:
            portfolio_returns = weighted_returns
        else:
            portfolio_returns = portfolio_returns.add(weighted_returns, fill_value=0)

    mu = portfolio_returns.mean()
    sigma = portfolio_returns.std()

    return mu, sigma


def monte_carlo_simulation(portfolio, years=15, simulations=1000, period="5y"):
    mu, sigma = estimate_portfolio_parameters(portfolio, period)

    if mu is None or sigma is None:
        print("Could not estimate portfolio parameters.")
        return None

    trading_days = 252
    total_days = years * trading_days

    initial_value = calculate_total_invested_value(portfolio)

    simulation_results = np.zeros((total_days + 1, simulations))

    for sim in range(simulations):
        value = initial_value
        simulation_results[0, sim] = value

        for day in range(1, total_days + 1):
            daily_return = np.random.normal(mu, sigma)
            value = value * (1 + daily_return)
            simulation_results[day, sim] = value

    return simulation_results

def plot_monte_carlo(simulation_results, years=15, paths_to_show=100):
    if simulation_results is None:
        print("No simulation results to plot.")
        return

    plt.figure(figsize=(12, 6))

    max_paths = min(paths_to_show, simulation_results.shape[1])

    for i in range(max_paths):
        plt.plot(simulation_results[:, i])

    plt.title(f"Monte Carlo Simulation of Portfolio Value ({years} Years)")
    plt.xlabel("Trading Days")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def display_simulation_summary(simulation_results):
    if simulation_results is None:
        print("No simulation results available.")
        return

    final_values = simulation_results[-1, :]

    print("\nSimulation Summary:")
    print(f"Average final value: {final_values.mean():.2f}")
    print(f"Minimum final value: {final_values.min():.2f}")
    print(f"Maximum final value: {final_values.max():.2f}")
    print(f"Median final value: {np.median(final_values):.2f}")
    print(f"5th percentile: {np.percentile(final_values, 5):.2f}")
    print(f"95th percentile: {np.percentile(final_values, 95):.2f}")

# Calculations
def calculate_current_value(asset, current_price):
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





## END HELPER FUNCTIONS


def add_asset(portfolio): # Adding to portfolio
    ticker = input("Enter ticker: ")
    sector = input("Enter sector: ")
    asset_class = input("Enter asset_class: ")
    quantity = int(input("Enter quantity: "))
    purchase_price = float(input("Enter purchase price: "))

    asset = {
        "ticker": ticker,
        "sector": sector,
        "asset_class": asset_class,
        "quantity": quantity,
        "purchase_price": purchase_price
    }
    portfolio.append(asset)


def display_portfolio(portfolio): # Displaying portfolio
    table = []
    current_values = {}
    total_current_value = 0

    for asset in portfolio:
        current_price = get_current_price(asset["ticker"])

        if current_price is None: # SAFETY
            print(asset["ticker"], "No price found!")
            continue

        transaction_value = calculate_transaction_value(asset)
        current_value = calculate_current_value(asset, current_price)
        gain_loss = calculate_gain_loss(asset, current_price)

        current_values[asset["ticker"]] = current_value
        total_current_value += current_value

        table.append([
            asset["ticker"],
            asset["sector"],
            asset["asset_class"],
            asset["quantity"],
            round(asset["purchase_price"], 2),
            round(current_price, 2),
            round(transaction_value, 2),
            round(current_value, 2),
            round(gain_loss, 2)
        ])
    print(t.tabulate(table, headers=["Ticker", "Sector", "Class", "Quantity", "Purchase Price", "Current Price", "Transaction Value", "Current Value", "Gain/Loss"], tablefmt="fancy_grid"))

    print("Total portfolio value is", round(total_current_value, 2))
    print("Total money invested is", round(calculate_total_invested_value(portfolio), 2))

    print("Weights:")
    for ticker, current_value in current_values.items():
        weight = (current_value / total_current_value) * 100
        print(f"{ticker}: {weight:.2f}%")


### RUN CODE FROM HERE

'''while True:
    add_asset(portfolio)
    more = input("Would you like to add more assets? (y/n): ")  
    if more.lower() == "n":
        break

display_portfolio(portfolio)
'''

#TEST
portfolio = [
    {
        "ticker": "MSFT",
        "sector": "tech",
        "asset_class": "stock",
        "quantity": 10,
        "purchase_price": 150
    },
    {
        "ticker": "AMZN",
        "sector": "tech",
        "asset_class": "stock",
        "quantity": 10,
        "purchase_price": 200
    }
]

#display_portfolio(portfolio)
#plot_portfolio_tickers(portfolio, period="1y")

simulation_results = monte_carlo_simulation(portfolio, years=15, simulations=1000, period="5y")
plot_monte_carlo(simulation_results, years=15, paths_to_show=5)
display_simulation_summary(simulation_results)


