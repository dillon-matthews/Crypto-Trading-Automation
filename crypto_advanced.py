import networkx as nx
import requests
import csv
import os
from datetime import datetime
import alpaca_trade_api as tradeapi

# Alpaca API credentials
API_KEY = "Insert your API key here for testing"
API_SECRET = "insert your API secret here for testing"
BASE_URL = "https://paper-api.alpaca.markets/v2"

# coin IDs and ticker symbols
coin_ids = [
    "aave",
    "bitcoin-cash",
    "bitcoin",
    "curve-dao-token",
    "polkadot",
    "ethereum",
    "the-graph",
    "chainlink",
    "litecoin",
    "maker",
    "shiba-inu",
    "uniswap",
    "usd-coin",
    "tether",
    "tezos",
]
coin_tickers = [
    "aave",
    "bch",
    "btc",
    "crv",
    "dot",
    "eth",
    "grt",
    "link",
    "ltc",
    "mkr",
    "shib",
    "uni",
    "usdc",
    "usdt",
    "xtz",
]

# directed graph
g = nx.DiGraph()


# Function to get exchange rates from CoinGecko API
def get_exchange_rates():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(coin_ids), "vs_currencies": ",".join(coin_tickers)}
    try:
        response = requests.get(url, params=params).json()
        save_currency_pair_data(response)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return

    for coin_id, ticker in zip(coin_ids, coin_tickers):
        for vs_currency, rate in response[coin_id].items():
            g.add_weighted_edges_from(
                [(ticker, vs_currency, rate), (vs_currency, ticker, 1 / rate)]
            )


# Function to save currency pair data to CSV file
def save_currency_pair_data(response):
    timestamp = datetime.now().strftime("%Y.%m.%d:%H.%M")
    filename = f"crypto_advanced/data/currency_pair_{timestamp}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for coin_id, ticker in zip(coin_ids, coin_tickers):
            if coin_id not in response:
                print(f"Warning: No data found for {coin_id}")
                continue
            for vs_currency, rate in response[coin_id].items():
                writer.writerow([ticker, vs_currency, rate])


# Function to find arbitrage opportunities
def find_arbitrage_opportunities():
    arbitrage_opportunities = []
    for cycle in nx.simple_cycles(g):
        if len(cycle) > 2:
            cycle_weight = 1
            for i in range(len(cycle)):
                node1 = cycle[i]
                node2 = cycle[(i + 1) % len(cycle)]
                cycle_weight *= g[node1][node2]["weight"]

            if abs(cycle_weight - 1) > 0.001:
                arbitrage_opportunities.append((cycle, cycle_weight))

    return arbitrage_opportunities


# Function to execute trades based on arbitrage opportunities
def execute_trades(arbitrage_opportunities):
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
    trading_results = []

    for opportunity in arbitrage_opportunities:
        cycle, cycle_weight = opportunity

        # Place buy order for the first currency in the cycle
        buy_currency = cycle[0]
        buy_quantity = 1.0

        try:
            buy_order = api.submit_order(
                symbol=buy_currency,
                qty=buy_quantity,
                side="buy",
                type="market",
                time_in_force="gtc",
            )

            # Place sell orders for the subsequent currencies in the cycle
            for i in range(1, len(cycle)):
                sell_currency = cycle[i]
                sell_quantity = buy_quantity * g[cycle[i - 1]][sell_currency]["weight"]

                sell_order = api.submit_order(
                    symbol=sell_currency,
                    qty=sell_quantity,
                    side="sell",
                    type="market",
                    time_in_force="gtc",
                )

            trading_results.append(
                {
                    "cycle": cycle,
                    "cycle_weight": cycle_weight,
                    "buy_order": buy_order,
                    "sell_orders": [sell_order],
                }
            )

        except tradeapi.rest.APIError as e:
            print(f"Error executing trade: {e}")

    return trading_results


# Main function to run the analysis and trading
def main():
    get_exchange_rates()
    arbitrage_opportunities = find_arbitrage_opportunities()
    trading_results = execute_trades(arbitrage_opportunities)


if __name__ == "__main__":
    main()
