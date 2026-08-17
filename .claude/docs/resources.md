# Resources

## Deriv Official Documentation

### DBot (Deriv Bot)
- **DBot Dashboard:** https://app.deriv.com/account/dbot
- **DBot User Guide:** https://deriv.com/trade-types/dbot/
- **Blockly XML Reference:** https://developers.google.com/blockly/guides/overview
- **Deriv API Documentation:** https://api.deriv.com/
- **Deriv API Explorer:** https://api.deriv.com/explorer/

### Deriv API
- **WebSocket API:** https://api.deriv.com/websocket/
- **API Credentials:** https://api.deriv.com/account/token
- **API Playground:** https://api.deriv.com/playground/

### Contract Types
- **Call/Put:** https://deriv.com/trade-types/call-put/
- **Accumulator:** https://deriv.com/trade-types/accumulator/
- **Multipliers:** https://deriv.com/trade-types/multipliers/
- **Turbos:** https://deriv.com/trade-types/turbos/
- **Ticks:** https://deriv.com/trade-types/ticks/

---

## Deriv Markets

### Synthetic Indices
- **Volatility Indices:** R_10, R_25, R_50, R_75, R_100 (continuous)
- **1-Minute Indices:** 1HZ10V, 1HZ25V, 1HZ50V, 1HZ75V, 1HZ100V
- **Boom/Crash:** BOOM1000, BOOM500, CRASH1000, CRASH500
- **Jump Indices:** JUMP10, JUMP25, JUMP50, JUMP75, JUMP100
- **Drift Switch:** DS10, DS20, DS50, DS70, DS100

### Forex
- Major pairs: EUR/USD, GBP/USD, USD/JPY, etc.
- Minor pairs: EUR/GBP, GBP/JPY, etc.
- Micro pairs: EUR/USD (micro), etc.

### Commodities
- Gold, Silver, Oil, Natural Gas

### Stock Indices
- Volatility 75, Volatility 25, etc.

---

## Tools

### DBot Development
- **DBot XML Editor:** Import XML directly into DBot
- **Blockly Developer Tools:** https://developers.google.com/blockly/devtools
- **Blockly Playground:** https://blockly-demo.appspot.com/

### XML Validation
- **XML Validator:** https://www.xmlvalidation.com/
- **XSD Validator:** https://www-free.nuu.edu.tw/~jwei/validator.html

### Technical Analysis Indicators
- **TA-Lib (Python):** https://github.com/TA-Lib/ta-lib-python
- **pandas-ta:** https://github.com/twopirllc/pandas-ta
- **Investopedia - Technical Analysis:** https://www.investopedia.com/terms/t/technicalanalysis.asp

### Indicator Reference
- **Bollinger Bands:** https://www.investopedia.com/terms/b/bollingerbands.asp
- **MACD:** https://www.investopedia.com/terms/m/macd.asp
- **RSI:** https://www.investopedia.com/terms/r/rsi.asp
- **Moving Averages:** https://www.investopedia.com/terms/m/movingaverage.asp
- **Stochastic Oscillator:** https://www.investopedia.com/terms/s/stochasticoscillator.asp

---

## Community

### Deriv Community
- **Deriv Community Forum:** https://community.deriv.com/
- **Deriv Blog:** https://deriv.com/blog/
- **Deriv GitHub:** https://github.com/deriv-com

### Blockly Community
- **Blockly GitHub:** https://github.com/google/blockly
- **Blockly Samples:** https://github.com/google/blockly-samples
- **Blockly Forum:** https://groups.google.com/g/blockly

---

## Strategy Resources

### Trend Following
- **Moving Average Crossover Strategy:** https://www.investopedia.com/terms/m/movingaveragecross.asp
- **MACD Strategy:** https://www.investopedia.com/articles/active-trading/121016/macd-strategy.asp

### Mean Reversion
- **Bollinger Band Strategy:** https://www.investopedia.com/articles/trading/10/bollingerbands.asp
- **RSI Mean Reversion:** https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp

### Momentum
- **Momentum Trading:** https://www.investopedia.com/terms/m/momentum.asp
- **MACD Histogram:** https://www.investopedia.com/terms/m/macd.asp

### Risk Management
- **Position Sizing:** https://www.investopedia.com/terms/p/positionsizing.asp
- **Martingale Strategy:** https://www.investopedia.com/terms/m/martingalesystem.asp
- **Kelly Criterion:** https://www.investopedia.com/terms/k/kellycriterion.asp

---

## Project-Specific

### Existing Bot Files
| File | Strategy | Notes |
|------|----------|-------|
| `bb-band-reversion.xml` | Bollinger Band mean reversion | R_25, callputequal |
| `ma-cross-trend.xml` | MA crossover trend following | R_25, callputequal |
| `macd-hist-momentum.xml` | MACD histogram momentum | R_25 |
| `macd-rsi-confirm.xml` | MACD + RSI confirmation | R_25 |
| `macd-rsi-bb-aggressive-v3.xml` | MACD + RSI + BB combo | R_100, aggressive |
| `rsi-reversal.xml` | RSI reversal signals | R_25 |
| `trend-pullback-combo.xml` | Trend + pullback entry | R_25 |
| `Martingale.xml` | Martingale accumulator | 1HZ100V |
| `smart-martingale-035.xml` | Smart martingale | R_25 |

### Python Tools
- `fix_bots.py` — Bulk add money management and stop conditions
- `fix_martingale.py` — Martingale-specific fixes

---

## Keyboard Shortcuts (DBot)

| Action | Shortcut |
|--------|----------|
| Undo | Ctrl+Z |
| Redo | Ctrl+Shift+Z |
| Delete | Delete / Backspace |
| Run Bot | F5 |
| Stop Bot | Shift+F5 |
| Save | Ctrl+S |
| Load | Ctrl+O |
