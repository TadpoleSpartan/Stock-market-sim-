# Stock Market Simulation

A simple interactive stock-market simulator. `game.py` is the original terminal version; `index.html` is the browser version and needs no install or extra packages.

## Run the website locally

1. Download or clone this repository.
2. Open `index.html` in a current web browser (double-clicking the file is enough).
3. Buy/sell shares, advance the simulated market, and follow your portfolio and transaction history. Game state is saved in that browser using local storage.

To run a local web server instead, open a terminal in the project folder and use:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish it as a website with GitHub Pages

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose the `main` branch and `/ (root)` folder, then save.
4. After the Pages deployment finishes, open the URL shown in the Pages settings (usually `https://tadpolespartan.github.io/Stock-market-sim-/`).

## Simulation notes

The browser version begins with $100,000 of simulated cash, no trading fees, and whole-share trades. Prices are fictional and change only when you advance the day. The game saves in the current browser/device; its saved state does not automatically sync between devices. The referenced PowerPoint was not available when this version was created, so the defaults still need to be checked against its exact rules and starting balance. This is an educational simulation, not live financial data or investment advice.
