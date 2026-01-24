# RugPlay Live Trade Notifier

This script monitors live RugPlay trades in real time using WebSockets and sends push notifications when large trades happen. It’s built to be lightweight, fast, and reliable, with simple priority tiers so important trades stand out immediately.

The goal is awareness, not automation. You see what’s moving, when it moves.

---

## What it Does

- Connects to RugPlay’s live WebSocket feed
- Listens to **global trades**
- Filters out small trades (default: under $2.5k)
- Assigns notification priority based on trade size
- Sends instant push notifications using **ntfy**
- Automatically reconnects if the connection drops

---

## How Notifications Work

Trades are grouped by size and assigned priorities:

- **$2.5k – $7.5k** → Low priority  
- **$7.5k – $25k** → Default priority  
- **$25k – $60k** → High priority  
- **$60k+** → Urgent priority  

Each notification includes:
- Buy or sell indicator
- Coin symbol
- Price
- USD value
- Token amount
- Username
- Direct coin link

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Configure the topic

Edit this line in the script:

```python
TOPIC = "rugrugrugrugrugrug"
```

This is your **ntfy topic name**. Anyone subscribed to this topic will receive notifications.

### 3. Run the script

```bash
python main.py
```

---

## Customization

You can safely adjust:

* Trade value threshold (`value < 2500`)
* Priority tiers
* Emoji indicators
* Formatting styles
* ntfy topic name

The script is designed to fail gracefully and reconnect automatically if RugPlay or the network hiccups.

---

## Notes

* No authentication required
* Read-only monitoring
* No interaction with your account
* Safe to run continuously

---

## Credits

Original implementation and logic by **inyourface34456**.
Packaged and shared for community use.

---

## License

MIT. Use it, modify it, learn from it.
