# Rugplay Trading BOT

**Rugplay Trading BOT** is a Python-based community toolkit for Rugplay.com. It provides scripts to automate coin management, streamline trading operations, and monitor portfolios. Designed for educational and community use, these scripts aim to simplify repetitive tasks while offering insights into gameplay strategies.

> ⚠️ **Disclaimer:** Use responsibly. These scripts are intended for learning and community purposes only. Test on small accounts first, and never share private credentials.

---

## Folder Contents

| File               | Description                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| `main.py`          | Automates buying and selling of a specified coin to maintain pool balance. |
| `sell_all.py`      | Sells all coins in your portfolio safely, excluding protected coins.       |
| `requirements.txt` | Python dependencies required to run the scripts.                           |

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/gatsbyingdev/rugplay-kit.git
cd rugplay-kit/Rugplay/
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Set the following variables for authentication and headers:

```
CF_CLEARANCE=<your cf_clearance cookie>
SECURE_BETTER_AUTH=<your session token>
USER_AGENT=<your browser user-agent string>
```

> Recommended: Use a `.env` file with `python-dotenv` to manage credentials securely.

---

## Usage

### Running Scripts

```bash
python main.py      # Automatically manages coin trading
python sell_all.py  # Sells all coins in portfolio safely
```

### Best Practices

* Test scripts with minimal amounts first.
* Always use environment variables; do not hard-code sensitive information.
* Monitor the script output to ensure proper operation.
* These scripts are intended as **community tools**, not investment advice.

---

## Contributing

Contributions are welcome. To contribute:

1. Keep code clean, readable, and well-commented.
2. Explain script functionality clearly.
3. Submit a pull request to `gatsbyingdev/rugplay-kit`.

All contributions must adhere to the community-focused purpose of the toolkit.

---

## License

MIT License – Free to use, modify, and share for educational and community purposes.

Do you want me to do that next?
