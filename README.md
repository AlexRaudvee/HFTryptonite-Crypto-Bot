# HFTryptonite-Crypto-Bot

This repository implements and benchmarks 10 high-frequency trading (HFT) strategies using Python. The project is designed to simulate various HFT methods on synthetic (or real) market data, compare their performance, and serve as a starting point for further research and development.

## Table of Contents

- [Project Overview](#project-overview)
- [HFT Strategies](#hft-strategies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Benchmarking](#benchmarking)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

This project explores and benchmarks a range of HFT algorithms, from classic market-making to modern machine learning approaches. Our goal is to build a modular simulation framework that allows us to test these strategies under controlled conditions and compare their performance metrics (e.g., profit, risk, execution speed).

## HFT Strategies

1. **Market Making:**  
   Continuously place bid and ask orders around the mid-price to capture the bid-ask spread. This strategy provides liquidity by quoting both sides of the market.

2. **Statistical Arbitrage:**  
   Exploit temporary deviations between correlated instruments. The strategy triggers trades when the price ratio between two assets deviates beyond a defined threshold.

3. **Momentum Trading:**  
   Identify short-term trends by comparing recent price movements. The algorithm enters a position in the direction of the momentum.

4. **Mean Reversion:**  
   Assume that prices will revert to their historical average. When the current price deviates significantly from a moving average, the strategy triggers a counter-trend trade.

5. **Order Book Imbalance:**  
   Analyze the size imbalance between bids and asks in the order book. A significant imbalance may indicate short-term price pressure, triggering buy or sell orders accordingly.

6. **Latency Arbitrage:**  
   Take advantage of tiny delays (latencies) between different data feeds or venues. This strategy simulates a lagged version of price data to identify arbitrage opportunities.

7. **Liquidity Sniping:**  
   Detect unusually large orders in the order book (either on the bid or ask side) and quickly trade to capture liquidity imbalances.

8. **VWAP/TWAP Execution:**  
   Implement execution algorithms that split large orders over time. VWAP (Volume-Weighted Average Price) and TWAP (Time-Weighted Average Price) help minimize market impact during execution.

9. **Reinforcement Learning-Based Strategy:**  
   Use reinforcement learning to dynamically adapt trading decisions based on market conditions. This method leverages an agent that learns from simulated interactions with the market environment.

10. **Neural Network Forecasting:**  
    Apply neural networks (e.g., feedforward models) to predict short-term price movements, generating trading signals based on the forecasted returns.

## Project Structure
```
HFTryptonite-Crypto-Bot/ 
├── notebooks/ # Jupyter notebooks for exploration and visualization 
├── strategies/ # Implementation of individual HFT strategies 
│ ├── market_making.py 
│ ├── stat_arb.py 
│ ├── momentum_trading.py 
│ ├── mean_reversion.py 
│ ├── order_book_imbalance.py 
│ ├── latency_arbitrage.py 
│ ├── liquidity_sniping.py 
│ ├── twap_strategy.py 
│ ├── rl_strategy.py 
│ └── nn_forecasting.py 
├── benchmarks/ # Scripts for benchmarking and performance comparison 
├── tests/ # Unit tests for each module 
├── README.md # This file 
├── requirements.txt # Python dependencies 
├── main.py # Main script to run simulations and benchmarks
├── bybit.py # script with connections to ByBit API
└── config.py configuration file with APIs and global variables
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AlexRaudvee/HFTryptonite-Crypto-Bot
   cd HFTryptonite-Crypto-Bot
   ```
2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
### Usage

1. Run the benchmark suite:
    Execute the main script to simulate and benchmark all strategies.
    ```bash
    python main.py
    ```

2. Explore individual strategies:
    Each strategy is implemented as a separate module in the strategies/ directory. You can run or modify these modules to test specific behaviors.

3. Interactive exploration:
    Use the notebooks in the notebooks/ directory to visualize data and performance metrics.

### Benchmarking

Benchmarks are located in the benchmarks/ folder. These scripts compare key performance indicators (KPIs) such as profit, drawdown, execution speed, and risk measures.

You are encouraged to add new benchmark tests or modify the existing ones as you refine the strategies.

### Roadmap
Integrate live or historical market data feeds.
Optimize strategy implementations for reduced latency.
Extend the reinforcement learning module with advanced techniques.
Enhance risk management and execution simulation.
Document benchmark results and publish performance comparisons.

### Contributing

Contributions, feedback, and suggestions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For questions or further discussion, please contact Alex_Raudvee.