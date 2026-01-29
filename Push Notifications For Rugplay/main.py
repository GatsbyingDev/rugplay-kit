import asyncio, json, requests, websockets # remember to install these shi-

WS = "wss://ws.rugplay.com"
TOPIC = "rugrugrugrugrugrug" # edit this to your desired name, and note it down
WATCH_FOR_COMMENTS = True
WATCH_FOR_TRADES = True

# List the coins you want to watch for comments (not live trades)
COINS = ["DPED2026", "HTD3", "VOLCANOO"]

def format_dollars(amount):
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M$" # round number to millions
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K$" # round number to thousands
    else:
        return f"{amount:.0f}$" # skip rounding step if smaller than 1k

def format_tokens(amount):
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"
    else:
        return f"{amount:.1f}" # the same as format_dollars

def format_price(price):
    # format price with appropriate decimal places
    if price >= 1:
        return f"${price:.2f}"
    elif price >= 0.001:
        return f"${price:.5f}".rstrip('0').rstrip('.')
    else:
        return f"${price:.6f}".rstrip('0').rstrip('.')

async def notif(title, msg, priority="default", tags="rugplay"):
    try:
        # encode title and tags as UTF-8 bytes, so we dont get error for trying to send emojis
        headers = {
            "Title": title.encode('utf-8'),
            "Tags": tags.encode('utf-8'),
            "Priority": priority
        }
        response = requests.post(
            f"https://ntfy.sh/{TOPIC}",
            data=msg.encode('utf-8'),
            headers=headers
        )
        response.raise_for_status()
        print(f"Notification sent ({priority}): {title}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send ntfy notification: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def listen_coin(coin: str):
    while True:
        try:
            async with websockets.connect(WS) as ws:
                await ws.send(json.dumps({
                    "type": "set_coin",
                    "coinSymbol": coin
                }))

                print(f"Listening for comments on {coin}...")

                while True:
                    message = await ws.recv()
                    data = json.loads(message)

                    if data.get("type") == "new_comment":
                        comment_data = data.get("data", {})
                        username = comment_data.get("userName", "Unknown")
                        content = comment_data.get("content", "")

                        content_with_link = f"{content}\nhttps://rugplay.com/coin/{coin}"
                        title = f"Comment on {coin} from @{username}"

                        print(f"[{coin}] New comment from {username}: {content}")
                        await notif(title, content_with_link)

        except websockets.ConnectionClosed:
            print(f"Connection for {coin} closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error for {coin}: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

async def monitor():
    print("Monitoring trades over $2.5k with priority tiers")
    while True:
        try:
            async with websockets.connect(WS, ping_interval=None, ping_timeout=None) as ws:
                print("WebSocket connected")
                await ws.send(json.dumps({"type": "set_coin", "coinSymbol": "@global"}))
                async for message in ws:
                    try:
                        data = json.loads(message)
                        if data.get("type") == "ping":
                            await ws.send(json.dumps({"type": "pong"}))
                            continue
                        if data.get("type") != "all-trades":
                            continue

                        trade = data.get("data", {})
                        value = float(trade.get("totalValue", 0))

                        # Skip trades below $2.5k. you can change this threshold
                        if value < 2500:
                            continue

                        # Determine priority based on value tiers
                        if value <= 7500:     # you can change the threshold to your need
                            priority = "low"
                        elif value <= 25000:
                            priority = "default"
                        elif value <= 60000:
                            priority = "high"
                        else:  # >60k
                            priority = "urgent"

                        kind = trade.get("type", "")
                        username = trade.get("username", "???")
                        symbol = trade.get("coinSymbol", "???")
                        amount = float(trade.get("amount", 0))
                        cash_str = format_dollars(value)
                        tokens_str = format_tokens(amount)
                        price = float(trade.get("price", 0))  # get coin price
                        price_str = format_price(price)  # format price

                        # determine notif title based on trade value
                        if value < 10000:
                            if kind == "BUY":
                                title = f"🟩 *{symbol}/{price_str}"
                            elif kind == "SELL":
                                title = f"🟥 *{symbol}/{price_str}"
                        elif value < 27500:
                            if kind == "BUY":
                                title = f"🟩🟩 *{symbol}/{price_str}"
                            elif kind == "SELL":
                                title = f"🟥🟥 *{symbol}/{price_str}"
                        else:
                            if kind == "BUY":
                                title = f"🟩🟩🟩 *{symbol}/{price_str}"
                            elif kind == "SELL":
                                title = f"🟥🟥🟥 *{symbol}/{price_str}"

                        body = f"{'+' if kind == 'BUY' else '-'}{cash_str} for {tokens_str} Tokens by @{username} https://rugplay.com/coin/{symbol} "
                        # +830.0K$ for 34.5 Tokens by @daddy <coin link here>

                        await notif(title, body, priority)
                    except Exception as e:
                        print(f"Error processing trade: {e}")
                        continue
        except Exception as e:
            print(f"WebSocket error: {e}, reconnecting...")
            await asyncio.sleep(10)

async def main():
    tasks = [listen_coin(coin) for coin in COINS]
    await asyncio.gather(
        monitor(),
        *tasks,
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Monitoring stopped")

