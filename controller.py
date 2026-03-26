import model
import view

portfolio = []

def add_asset(portfolio): # user input assets
    ticker = input("Enter ticker: ")
    sector = input("Enter sector: ")
    asset_class = input("Enter asset class: ")
    quantity = int(input("Enter quantity: "))
    purchase_price = float(input("Enter purchase price: "))

    asset = { # bundle everything into dict
        "ticker": ticker,
        "sector": sector,
        "asset_class": asset_class,
        "quantity": quantity,
        "purchase_price": purchase_price
    }
    portfolio.append(asset)

def show_portfolio(portfolio):
    table = []
    total_current_value = 0
    total_invested = model.calculate_total_invested_value(portfolio)
    weights = model.calculate_portfolio_weights(portfolio)

    for asset in portfolio:
        current_price = model.get_current_price(asset["ticker"])
        if current_price is None: # if invalid ticker
            print(asset["ticker"], "No price found!")
            continue
        table.append([
            asset["ticker"], asset["sector"], asset["asset_class"],
            asset["quantity"], round(asset["purchase_price"], 2),
            round(current_price, 2),
            round(model.calculate_transaction_value(asset), 2),
            round(model.calculate_current_value(asset, current_price), 2),
            round(model.calculate_gain_loss(asset, current_price), 2)
        ])
        total_current_value += model.calculate_current_value(asset, current_price)

    view.display_portfolio(table, total_current_value, total_invested, weights) # assemble data -> displayed by view

def run():
    while True:
        print("\n0. Load test portfolio")
        print("1. Add asset")
        print("2. View portfolio")
        print("3. Plot prices")
        print("4. View weights breakdown")
        print("5. Run simulation")
        print("6. Quit")
        choice = input("Choose: ")

        if choice == "0":
            load_test_portfolio()
        elif choice == "1":
            add_asset(portfolio)
        elif choice == "2":
            if not portfolio:
                print("Portfolio is empty!")
            else:
                show_portfolio(portfolio)
        elif choice == "3":
            if not portfolio:
                print("Portfolio is empty!")
            else:
                print("1. Plot all tickers")
                print("2. Plot single ticker")
                sub_choice = input("Choose: ")

                if sub_choice == "1":
                    view.plot_portfolio_tickers(portfolio)
                elif sub_choice == "2":
                    print("Available tickers:")
                    for asset in portfolio:
                        print(f"  {asset['ticker']}")
                    ticker = input("Enter ticker: ")
                    view.plot_single_ticker(ticker)
        elif choice == "4":
            if not portfolio:
                print("Portfolio is empty!")
            else:
                sector_weights = model.calculate_sector_weights(portfolio)
                class_weights = model.calculate_asset_class_weights(portfolio)
                view.display_weights_breakdown(sector_weights, class_weights)
        elif choice == "5":
            if not portfolio:
                print("Portfolio is empty!")
            else:
                results = model.monte_carlo_simulation(portfolio)
                view.plot_monte_carlo(results)
                view.display_simulation_summary(results)
        elif choice == "6":
            break


def load_test_portfolio():
    test_assets = [
        {"ticker": "AAPL", "sector": "technology", "asset_class": "stock", "quantity": 10, "purchase_price": 150},
        {"ticker": "MSFT", "sector": "technology", "asset_class": "stock", "quantity": 8, "purchase_price": 280},
        {"ticker": "JNJ", "sector": "healthcare", "asset_class": "stock", "quantity": 6, "purchase_price": 160},
        {"ticker": "UNH", "sector": "healthcare", "asset_class": "stock", "quantity": 4, "purchase_price": 270},
        {"ticker": "JPM", "sector": "financials", "asset_class": "stock", "quantity": 8, "purchase_price": 140},
        {"ticker": "V", "sector": "financials", "asset_class": "stock", "quantity": 10, "purchase_price": 210},
        {"ticker": "MCD", "sector": "consumer", "asset_class": "stock", "quantity": 5, "purchase_price": 260},
        {"ticker": "PG", "sector": "consumer", "asset_class": "stock", "quantity": 7, "purchase_price": 140},
        {"ticker": "XOM", "sector": "energy", "asset_class": "stock", "quantity": 12, "purchase_price": 90},
        {"ticker": "BND", "sector": "fixed income", "asset_class": "etf", "quantity": 20, "purchase_price": 75},
    ]
    for asset in test_assets:
        portfolio.append(asset)
    print("Test portfolio loaded.")