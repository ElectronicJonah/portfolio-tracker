import matplotlib.pyplot as plt
import tabulate as t
import numpy as np
from model import get_historical_prices

# Plots
def plot_portfolio_tickers(portfolio, period="6mo"):
    plt.figure(figsize=(12,6))

    for asset in portfolio:
        ticker = asset["ticker"]
        prices = get_historical_prices(ticker, period)
        plt.plot(prices.index, prices.values, label=ticker)

    plt.title("Price history")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_monte_carlo(simulation_results, years=15, paths_to_show=100):
    plt.figure(figsize=(12, 6))

    max_paths = min(paths_to_show, simulation_results.shape[1])
    for i in range(max_paths):
        plt.plot(simulation_results[:, i], alpha=0.1, color='gray')

    median = np.median(simulation_results, axis=1)
    p5 = np.percentile(simulation_results, 5, axis=1)
    p95 = np.percentile(simulation_results, 95, axis=1)

    plt.plot(median, color='blue', linewidth=2, label='Median')
    plt.fill_between(range(len(median)), p5, p95, alpha=0.2, color='blue', label='5th-95th percentile')

    plt.title(f"Monte Carlo Simulation of Portfolio Value ({years} Years)")
    plt.xlabel("Trading Days")
    plt.ylabel("Portfolio Value")
    plt.ylim(0, np.percentile(simulation_results[-1, :], 99))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def display_simulation_summary(simulation_results):

    final_values = simulation_results[-1, :] # last row all columns

    print("\nSimulation Summary:")
    print(f"Average final value: {final_values.mean():.2f}")
    print(f"Minimum final value: {final_values.min():.2f}")
    print(f"Maximum final value: {final_values.max():.2f}")
    print(f"Median final value: {np.median(final_values):.2f}")
    print(f"5th percentile: {np.percentile(final_values, 5):.2f}")
    print(f"95th percentile: {np.percentile(final_values, 95):.2f}")



def display_portfolio(table, total_current_value, total_invested, weights):
    print(t.tabulate(table, headers=["Ticker", "Sector", "Class", "Quantity",
          "Purchase Price", "Current Price", "Transaction Value", "Current Value",
          "Gain/Loss"], tablefmt="fancy_grid"))

    print("Total portfolio value is", round(total_current_value, 2))
    print("Total money invested is", round(total_invested, 2))

    print("Weights:")
    for ticker, weight in weights.items():
        print(f"{ticker}: {weight * 100:.2f}%")


def display_weights_breakdown(sector_weights, class_weights):
    print("\nBy sector:")
    for sector, weight in sector_weights.items():
        print(f"  {sector}: {weight * 100:.2f}%")

    print("\nBy asset class:")
    for asset_class, weight in class_weights.items():
        print(f"  {asset_class}: {weight * 100:.2f}%")


def plot_single_ticker(ticker, period="6mo"):
    prices = get_historical_prices(ticker, period)
    plt.figure(figsize=(12, 6))
    plt.plot(prices.index, prices.values)
    plt.title(f"Price history - {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()