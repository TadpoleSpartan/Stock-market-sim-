"""
Stock Market Simulation

Interactive terminal-based stock trading simulator. The PowerPoint referenced in
 the request is not available in the repository, so the game starts with clear
 defaults; replace these with the presentation's exact rules when it is supplied.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

STARTING_CASH = 100_000.00
TRADING_FEE = 0.0


@dataclass
class Stock:
    symbol: str
    name: str
    price: float
    previous_price: float
    volatility: float
    sector: str
    market_cap: str
    pe_ratio: float

    @property
    def day_change(self) -> float:
        return self.price - self.previous_price

    @property
    def day_change_percent(self) -> float:
        return self.day_change / self.previous_price * 100 if self.previous_price else 0.0


@dataclass
class Holding:
    shares: int = 0
    average_cost: float = 0.0


@dataclass
class Transaction:
    day: int
    timestamp: str
    kind: str
    symbol: str
    shares: int
    price: float
    fee: float

    @property
    def total(self) -> float:
        return self.shares * self.price + self.fee


@dataclass
class Market:
    stocks: Dict[str, Stock] = field(default_factory=dict)

    def advance_day(self) -> None:
        for stock in self.stocks.values():
            stock.previous_price = stock.price
            move = random.gauss(0.0003, stock.volatility)
            if random.random() < 0.08:  # occasional simulated news shock
                move += random.gauss(0.0, stock.volatility * 2.5)
            stock.price = round(max(1.0, stock.price * (1 + move)), 2)


class StockMarketSimulator:
    def __init__(self) -> None:
        self.cash = STARTING_CASH
        self.day = 1
        self.holdings: Dict[str, Holding] = {}
        self.transactions: List[Transaction] = []
        self.running = True
        self.market = Market()
        stocks = [
            ("AAPL", "Apple", 228.50, .018, "Technology", "Mega", 34.2),
            ("MSFT", "Microsoft", 420.10, .016, "Technology", "Mega", 36.8),
            ("NVDA", "NVIDIA", 138.85, .032, "Semiconductors", "Mega", 52.4),
            ("AMZN", "Amazon", 192.35, .024, "Consumer / Cloud", "Mega", 41.1),
            ("TSLA", "Tesla", 352.56, .045, "Automotive", "Mega", 79.3),
            ("JPM", "JPMorgan Chase", 237.20, .014, "Financials", "Mega", 14.2),
            ("JNJ", "Johnson & Johnson", 158.40, .012, "Healthcare", "Large", 24.6),
            ("XOM", "Exxon Mobil", 112.75, .022, "Energy", "Large", 14.8),
        ]
        for symbol, name, price, vol, sector, cap, pe in stocks:
            self.market.stocks[symbol] = Stock(symbol, name, price, price, vol, sector, cap, pe)

    @staticmethod
    def money(value: float) -> str:
        return f"{'-' if value < 0 else ''}${abs(value):,.2f}"

    def portfolio_value(self) -> float:
        return sum(h.shares * self.market.stocks[s].price for s, h in self.holdings.items())

    def net_worth(self) -> float:
        return self.cash + self.portfolio_value()

    def explain(self) -> None:
        print("\n" + "=" * 68)
        print("STOCK MARKET SIMULATION — HOW TO PLAY")
        print("=" * 68)
        print("Objective: make your own investing decisions and grow your portfolio.")
        print(f"Starting cash: {self.money(STARTING_CASH)} | Trading fee: {self.money(TRADING_FEE)}")
        print("Buy/sell whole shares; no borrowing or short selling. Advance a day to")
        print("generate simulated price changes and occasional news shocks. All trades")
        print("are recorded. This is a fictional market, not live financial data.")
        print("The referenced PowerPoint was not attached to the repository, so its")
        print("specific rules and starting balance still need to be verified.")
        input("\nPress Enter to start trading... ")

    def dashboard(self) -> None:
        print("\n" + "=" * 75)
        print(f"TRADING DAY {self.day} | CASH {self.money(self.cash)} | INVESTED {self.money(self.portfolio_value())}")
        print(f"NET WORTH {self.money(self.net_worth())} | OVERALL P/L {self.money(self.net_worth() - STARTING_CASH)}")
        print("-" * 75)
        print(f"{'SYMBOL':<8}{'COMPANY':<22}{'PRICE':>12}{'CHANGE':>12}{'DAY %':>10}")
        print("-" * 75)
        for s in self.market.stocks.values():
            print(f"{s.symbol:<8}{s.name:<22}{s.price:>12,.2f}{s.day_change:>+12,.2f}{s.day_change_percent:>+9.2f}%")

    def portfolio(self) -> None:
        print("\nPORTFOLIO")
        print(f"{'SYMBOL':<8}{'SHARES':>8}{'AVG COST':>12}{'VALUE':>14}{'UNREALIZED P/L':>18}")
        has_holding = False
        for symbol, holding in sorted(self.holdings.items()):
            if not holding.shares:
                continue
            has_holding = True
            price = self.market.stocks[symbol].price
            value = holding.shares * price
            pl = value - holding.shares * holding.average_cost
            print(f"{symbol:<8}{holding.shares:>8}{holding.average_cost:>12,.2f}{value:>14,.2f}{pl:>+18,.2f}")
        if not has_holding:
            print("No shares held yet.")
        print(f"Cash: {self.money(self.cash)} | Portfolio: {self.money(self.portfolio_value())} | Net worth: {self.money(self.net_worth())}")

    def details(self) -> None:
        symbol = input("Symbol: ").strip().upper()
        stock = self.market.stocks.get(symbol)
        if not stock:
            print("Unknown symbol.")
            return
        print(f"\n{stock.symbol} — {stock.name} | {stock.sector} | {stock.market_cap} cap")
        print(f"Price {self.money(stock.price)} | Day {stock.day_change:+.2f} ({stock.day_change_percent:+.2f}%) | P/E {stock.pe_ratio:.1f} | Simulated daily volatility {stock.volatility:.1%}")

    @staticmethod
    def read_shares() -> int:
        try:
            amount = int(input("Whole shares: ").strip())
            if amount < 1:
                raise ValueError
            return amount
        except ValueError:
            print("Enter a positive whole number.")
            return 0

    def buy(self) -> None:
        symbol = input("Buy symbol: ").strip().upper()
        stock = self.market.stocks.get(symbol)
        if not stock:
            print("Unknown symbol.")
            return
        shares = self.read_shares()
        total = shares * stock.price + TRADING_FEE
        if not shares:
            return
        if total > self.cash:
            print(f"Insufficient cash; order total is {self.money(total)}.")
            return
        holding = self.holdings.setdefault(symbol, Holding())
        holding.average_cost = (holding.shares * holding.average_cost + shares * stock.price) / (holding.shares + shares)
        holding.shares += shares
        self.cash -= total
        self.record("BUY", symbol, shares, stock.price)
        print(f"Bought {shares} {symbol} share(s) for {self.money(total)}.")

    def sell(self) -> None:
        symbol = input("Sell symbol: ").strip().upper()
        holding = self.holdings.get(symbol)
        stock = self.market.stocks.get(symbol)
        if not stock or not holding or holding.shares == 0:
            print("You do not own that stock.")
            return
        shares = self.read_shares()
        if not shares:
            return
        if shares > holding.shares:
            print(f"You own only {holding.shares} share(s).")
            return
        proceeds = shares * stock.price - TRADING_FEE
        holding.shares -= shares
        if holding.shares == 0:
            holding.average_cost = 0.0
        self.cash += proceeds
        self.record("SELL", symbol, shares, stock.price)
        print(f"Sold {shares} {symbol} share(s) for {self.money(proceeds)}.")

    def record(self, kind: str, symbol: str, shares: int, price: float) -> None:
        self.transactions.append(Transaction(self.day, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kind, symbol, shares, price, TRADING_FEE))

    def history(self) -> None:
        print("\nTRANSACTION HISTORY")
        if not self.transactions:
            print("No trades yet.")
            return
        print(f"{'DAY':<6}{'TYPE':<7}{'SYMBOL':<8}{'SHARES':>8}{'PRICE':>12}{'FEE':>9}{'TIME':>22}")
        for t in self.transactions:
            print(f"{t.day:<6}{t.kind:<7}{t.symbol:<8}{t.shares:>8}{t.price:>12,.2f}{t.fee:>9,.2f}{t.timestamp:>22}")

    def run(self) -> None:
        self.explain()
        while self.running:
            self.dashboard()
            print("\n1 Dashboard  2 Stock details  3 Buy  4 Sell  5 Portfolio  6 Transactions  7 Advance day  8 Exit")
            choice = input("Select: ").strip()
            if choice == "1":
                continue
            elif choice == "2":
                self.details()
            elif choice == "3":
                self.buy()
            elif choice == "4":
                self.sell()
            elif choice == "5":
                self.portfolio()
            elif choice == "6":
                self.history()
            elif choice == "7":
                self.market.advance_day()
                self.day += 1
                print("Market prices updated for the next trading day.")
            elif choice == "8":
                self.running = False
                print("Thanks for trading!")
            else:
                print("Choose an option from 1 to 8.")


if __name__ == "__main__":
    StockMarketSimulator().run()
