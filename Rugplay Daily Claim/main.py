import requests
import os
import json
import time
import datetime

DEFAULT_CONFIG_PATH = "config.json"

def load_config(path=DEFAULT_CONFIG_PATH):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("check_interval_seconds", 30)
    cfg.setdefault("options", {})
    cfg["options"].setdefault("auto_retry_on_fail", True)
    cfg["options"].setdefault("retry_delay_seconds", 5)
    cfg["options"].setdefault("log_to_file", True)
    cfg["options"].setdefault("log_file_path", "rugplay_claim_log.txt")
    cfg["options"].setdefault("max_attempts_per_account", 3)
    cfg["options"].setdefault("send_money", True)
    cfg["options"].setdefault("send_money_account", "facedev")
    return cfg

cfg = load_config()
accounts = cfg.get("accounts")
if not isinstance(accounts, list) or len(accounts) == 0:
    print("No 'accounts' list found in config, exiting.")
    exit(1)

check_interval = int(cfg.get("check_interval_seconds", 30))
options = cfg.get("options", {})

# Logging function
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    if options.get("log_to_file"):
        try:
            with open(options.get("log_file_path"), "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to write log: {e}")

headers = {
    'User-Agent': os.getenv("USER_AGENT", "Mozilla/5.0"),
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://rugplay.com',
    'Content-Type': 'application/json',
    'Origin': 'https://rugplay.com/',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

def ms_to_hours_minutes(ms):
    seconds = ms // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def send_money(account, recipient_username, amount):
    display_name = account.get("display_name", "No name")
    if not recipient_username or amount is None:
        log(f"[{display_name}] Invalid transfer parameters.")
        return False

    cookies = {
        'cf_clearance': account.get("cf_clearance"),
        '__Secure-better-auth.session_token': account.get("__Secure-better-auth.session_token"),
    }

    payload = {
        "recipientUsername": str(recipient_username),
        "type": "CASH",
        "amount": int(amount),
    }

    try:
        resp = requests.post(
            "https://rugplay.com/api/transfer",
            cookies=cookies,
            headers=headers,
            json=payload,
            timeout=15
        )

        if resp.status_code in (200, 201, 204):
            try:
                body = resp.json()
                sent_amount = body.get("amount", payload["amount"]) if isinstance(body, dict) else payload["amount"]
            except Exception:
                sent_amount = payload["amount"]
            log(f"[{display_name}] Sent {sent_amount} to {recipient_username} successfully.")
            return True
        else:
            log(f"[{display_name}] Transfer failed ({resp.status_code}): {resp.text}")
            return False

    except Exception as e:
        log(f"[ERROR][{display_name}] Failed to send money to {recipient_username}: {e}")
        return False

def claim_daily_reward(account):
    display_name = account.get("display_name", "No name")
    cookies = {
        'cf_clearance': account.get("cf_clearance"),
        '__Secure-better-auth.session_token': account.get("__Secure-better-auth.session_token"),
    }

    attempts = 0
    max_attempts = options.get("max_attempts_per_account", 3)
    while attempts < max_attempts:
        try:
            response = requests.post(
                'https://rugplay.com/api/rewards/claim',
                cookies=cookies,
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                try:
                    body = response.json()
                    reward_amount = body.get('rewardAmount') if isinstance(body, dict) else None
                except Exception:
                    reward_amount = None
                if reward_amount:
                    log(f"[{display_name}] Claimed {reward_amount} successfully, next in 12h 00m.")
                    if options.get("send_money"):
                        send_money(account, options.get("send_money_account"), reward_amount)
                else:
                    log(f"[{display_name}] Claimed successfully, next in 12h 00m.")
                return  # success, exit loop

            elif response.status_code == 429:
                try:
                    body = response.json()
                except ValueError:
                    body = {}
                time_remain = body.get("timeRemaining") or body.get("time_remaining") or body.get("timeLeft")
                if time_remain:
                    log(f"[{display_name}] Daily reward not ready. Try again in {ms_to_hours_minutes(int(time_remain))}.")
                else:
                    log(f"[{display_name}] Daily reward not ready. Wait before claiming again.")
                return  # cannot claim yet

            else:
                log(f"[{display_name}] Claim failed ({response.status_code}): {response.text}")

        except Exception as e:
            log(f"[ERROR][{display_name}] {e}")

        attempts += 1
        if options.get("auto_retry_on_fail") and attempts < max_attempts:
            time.sleep(options.get("retry_delay_seconds", 5))
        else:
            break

def main_loop():
    while True:
        for account in accounts:
            claim_daily_reward(account)
            time.sleep(1)  # small delay to avoid rate limits
        time.sleep(check_interval)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        log("Script stopped by user.")
    except Exception as e:
        log(f"[ERROR] {e}")
