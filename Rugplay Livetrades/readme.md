# Rugplay Livetrades

**Rugplay Livetrades** is a Python-based live trade monitor for Rugplay.com. It fetches real-time trades, detects buys and sells, formats detailed trade information (prices, amounts, trader wallets, and stats), and sends updates directly to a Discord webhook.

Designed for **community use**, this script includes features like filtering by coin, ANSI-styled console output, session counters, and automatic cookie loading. It helps players monitor market activity efficiently and safely.

> ⚠️ **Disclaimer:** Use responsibly. This tool is for **educational and community purposes only**. Test on small accounts first and do not share private credentials.

---

## Features

* Real-time detection of buys and sells
* Formatted trade information: prices, amounts, wallet addresses, and trader info
* Sends notifications to a Discord webhook in real time
* Filtering options for specific coins or trade amounts
* ANSI-styled console output for clear monitoring
* Automatic cookie/session handling and counters
* Supports both WebSocket and HTTP polling modes

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/gatsbyingdev/rugplay-kit.git
cd rugplay-kit/Rugplay\ Livetrades
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

> Make sure `requests` and `websocket-client` are installed if you want WebSocket monitoring.

---

## Configuration

Set the following environment variables (or use a `.env` file in the folder):

```
RUGPLAY_COOKIE=<your Rugplay session cookie>
DISCORD_WEBHOOK=<your Discord webhook URL>
POLL_INTERVAL=8          # Seconds between HTTP polls
LIMIT=100                # Max trades per poll
COIN_FILTER=             # Optional: filter for a specific coin symbol
MIN_USD=0                # Optional: minimum trade value to notify
WEBSOCKET_URL=wss://ws.rugplay.com/
WEBSOCKET_USERID=<your user ID>
WEBSOCKET_COIN=@global
AUTO_SUBSCRIBE=true
```

> Tip: Keep credentials in environment variables for safety.

---

## Usage

Run the live monitor:

```bash
python main.py
```

* The script will start monitoring Rugplay trades in real time.
* Trades matching your filters will be sent to your configured Discord webhook.
* Console output is styled with ANSI colors for easy monitoring of buys, sells, and session statistics.

---

## Safety Guidelines

* **Never hard-code credentials** in scripts. Use environment variables.
* Start with low-value accounts for testing.
* Monitor the console output and Discord notifications closely.
* Treat this as an **educational tool**, not financial advice.

---

## Contributing

Contributions are welcome!

* Keep code readable and well-commented
* Explain any new features or filters clearly
* Submit pull requests to `gatsbyingdev/rugplay-kit`
* Ensure contributions align with community-focused educational use

---

## License

MIT License – Free to use, modify, and share for educational and community purposes.
