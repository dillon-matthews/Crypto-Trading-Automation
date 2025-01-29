# Cryptocurrency Trading Automation

## Overview

This project is an advanced continuation of **cryptocurrency trading automation**, leveraging **real-time exchange rates** and **paper trading** to simulate profitable trades. The program detects **arbitrage opportunities** by analyzing exchange rate discrepancies using **graph-based traversal techniques**.

## Key Features

### 📊 Data Retrieval & Storage

- **Fetch real-time exchange rates** using the **CoinGecko API**.
- **Expanded the trading graph** by adding **6 additional cryptocurrencies**.
- **Store exchange rate data** in **CSV format**, using a structured naming convention:
  ```plaintext
  crypto_advanced/data/currency_pair_YYYY.MM.DD:HH.MM.txt
  ```

### 🔎 Arbitrage Detection & Trading

- **Graph Representation**:
  - Nodes represent cryptocurrencies.
  - Directed edges represent exchange rates.
  - Detect cycles that **deviate from equilibrium**.
- **Arbitrage Detection**:
  - Identify profitable trade paths **where a round-trip yields more than 1.0**.
  - Execute simulated trades based on detected opportunities.
- **Paper Trading Execution**:
  - Use **Alpaca Paper Trading API** to submit simulated trades.
  - Ensure all trades follow a logical order **(buy/sell sequences)**.

### ⏰ Automated Execution

- **Run the script every weekday at 9 AM ET** using `cron`.
- Ensure the program:
  - Fetches fresh data
  - Detects arbitrage cycles
  - Simulates trades
  - Logs results

## API Usage

### 🔗 CoinGecko API (Exchange Rates)

```plaintext
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin,bitcoin-cash,eos,cardano,ripple&vs_currencies=btc,eth,ltc,bch,eos,ada,xrp
```

- Returns JSON structure with exchange rates.

### 📑 Alpaca Paper Trading API (Simulated Trades)

- **Base URL:** `https://paper-api.alpaca.markets/v2`
- Trades are executed with **API keys** ensuring only paper trades are submitted.

## Example Output

```json
{
  "best_arbitrage_opportunity": {
    "path": ["btc", "xrp", "eth", "btc"],
    "profit_factor": 1.0089,
    "expected_profit": "$120.75"
  },
  "last_trade": "Executed simulated trade cycle successfully."
}
```

## Future Enhancements

- **Live Trading Integration** (real-money execution).
- **Expanded Market Coverage** (more crypto pairs).
- **Machine Learning Predictions** for trend analysis.

---

*Developed as an advanced cryptocurrency trading simulation project using real-time data and automated execution.*

