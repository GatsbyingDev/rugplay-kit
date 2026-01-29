# Rugplay Daily Claim

Automated daily reward claimer for [Rugplay](https://rugplay.com).  
Supports multiple accounts, logging, retries, and fully configurable options.

---

## Folder Structure

```

Rugplay Daily Claim/
│
├─ script.py
├─ config.json
├─ requirements.txt
├─ README.md

````

---

## 1. Install Requirements

Make sure you have **Python 3.9+** installed.

Install dependencies:

```bash
pip install -r requirements.txt
````

**requirements.txt content:**

```
requests>=2.31.0
```

---

## 2. Configure `config.json`

Template:

```json
{
  "check_interval_seconds": 60,
  "accounts": [
    {
      "display_name": "YOUR_DISPLAY_NAME_HERE",
      "cf_clearance": "PASTE_YOUR_CF_CLEARANCE_COOKIE_HERE",
      "__Secure-better-auth.session_token": "PASTE_YOUR_SESSION_TOKEN_HERE",
      "notes": "Use Chrome DevTools → Application tab → Cookies to get these values."
    }
  ],
  "options": {
    "auto_retry_on_fail": true,
    "retry_delay_seconds": 5,
    "log_to_file": true,
    "log_file_path": "rugplay_claim_log.txt",
    "max_attempts_per_account": 3
  },
  "metadata": {
    "created_by": "@Cash1416 & @GatsbyingDev",
    "script_version": "1.0.0",
    "description": "Template config for Rugplay Daily Reward Claimer."
  }
}
```

**Instructions:**

* Replace `"YOUR_DISPLAY_NAME_HERE"` with a label for the account.
* Replace `"PASTE_YOUR_CF_CLEARANCE_COOKIE_HERE"` and `"PASTE_YOUR_SESSION_TOKEN_HERE"` with your actual cookies from Chrome DevTools → Application → Cookies.
* Adjust `"check_interval_seconds"` to control how often the script loops.
* Configure logging and retry options under `"options"` if needed.
* Multiple accounts can be added by copying the account object into the `"accounts"` array.

---

## 3. Running the Script

From inside the folder:

```bash
python script.py
```

What the script does:

1. Loops through all accounts in `config.json`.
2. Claims daily rewards automatically.
3. Respects retries, delays, and logging options from the config.
4. Prints logs to the console and optionally to `rugplay_claim_log.txt`.
5. Handles 429 rate-limit responses gracefully.

---

## 4. Config Options Explained

| Option                     | Type | Default                 | Description                         |
| -------------------------- | ---- | ----------------------- | ----------------------------------- |
| `auto_retry_on_fail`       | bool | true                    | Automatically retries failed claims |
| `retry_delay_seconds`      | int  | 5                       | Seconds to wait between retries     |
| `log_to_file`              | bool | true                    | Save logs to a file                 |
| `log_file_path`            | str  | `rugplay_claim_log.txt` | Path for log file                   |
| `max_attempts_per_account` | int  | 3                       | Maximum retry attempts per account  |

---

## 5. Notes & Best Practices

* **Keep your cookies secret**: Anyone with them can access your Rugplay account.
* **Avoid over-frequent runs**: Use `check_interval_seconds` to prevent rate-limiting.
* **Multiple accounts supported**: Simply add them to `"accounts"` in `config.json`.
* **Stopping the script**: Press `Ctrl+C` to safely exit.
* **Logging**: All claim results, errors, and retries are logged to console and optionally to a file.

---

## 6. Credits

* **Author:** @Cash1416 & @GatsbyingDev
* **Script Version:** 1.0.0
* **Description:** Full-featured Rugplay Daily Reward Claimer with multi-account support, logging, and retries.
