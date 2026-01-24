// use in browser console
const ui = document.createElement("div");
ui.style = `
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(0,0,0,0.9);
  color: white;
  padding: 15px;
  border-radius: 10px;
  font-family: sans-serif;
  z-index: 999999;
  width: 300px;
  max-height: 90vh;
  overflow-y: auto;
`;

ui.innerHTML = `
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
    <div style="font-weight:bold; font-size:16px;">💰 Pom Bot</div>
    <button id="minimizeBtn" style="background:#222; color:white; border:none; padding:2px 6px; border-radius:4px; cursor:pointer;">–</button>
  </div>
  <div id="botContent">
    <label>Ticker Symbol:<br><input id="symbolInput" type="text" value="" style="width:100%"></label><br><br>
    <label id="amountLabel">Amount ($):<br><input id="amountInput" type="number" value="1" min="0.01" step="0.01" style="width:100%"></label><br><br>
    <label>Action:<br>
      <select id="actionSelect" style="width:100%">
        <option value="BUY">BUY</option>
        <option value="SELL">SELL</option>
      </select>
    </label><br><br>
    <label>Delay (ms):<br><input id="delayInput" type="number" value="50" min="10" step="10" style="width:100%"></label><br><br>
    <button id="maxBtn" style="width:100%; margin-bottom:6px;">Max Buy/Sell</button>
    <button id="loopBtn" style="width:100%; margin-bottom:6px;">Auto Buy ➜ Sell</button>
    <button id="smartSellBtn" style="width:100%; margin-bottom:6px;">Smart Sell</button>
    <button id="startBtn" style="width:48%">Start</button>
    <button id="stopBtn" style="width:48%" disabled>Stop</button>
    <hr>
    <div id="logArea" style="max-height: 200px; overflow-y: auto; background: #111; padding: 10px; font-size: 12px; border-radius: 6px;"></div>
  </div>
`;

document.body.appendChild(ui);

let minimized = false;
document.getElementById("minimizeBtn").onclick = () => {
  minimized = !minimized;
  document.getElementById("botContent").style.display = minimized ? "none" : "block";
  document.getElementById("minimizeBtn").textContent = minimized ? "+" : "–";
};

document.getElementById("actionSelect").onchange = () => {
  const mode = document.getElementById("actionSelect").value;
  const label = document.getElementById("amountLabel");
  label.innerHTML = mode === "BUY"
    ? 'Amount ($):<br><input id="amountInput" type="number" value="1" min="0.01" step="0.01" style="width:100%">'
    : 'Amount (Tokens):<br><input id="amountInput" type="number" value="1" min="0.01" step="0.01" style="width:100%">';
};

function logMsg(msg) {
  const log = document.getElementById("logArea");
  const time = new Date().toLocaleTimeString();
  log.innerHTML = `[${time}] ${msg}<br>` + log.innerHTML;
}

document.getElementById("maxBtn").onclick = async () => {
  const mode = document.getElementById("actionSelect").value;
  const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
  const input = document.querySelector("#amountInput");

  if (!symbol) return alert("Enter a symbol first.");

  try {
    if (mode === "SELL") {
      const res = await fetch("https://rugplay.com/api/portfolio/total", {
        credentials: "include",
        headers: { "User-Agent": navigator.userAgent },
        method: "GET",
        mode: "cors"
      });
      const data = await res.json();
      const holding = data.coinHoldings.find(c => c.symbol.toUpperCase() === symbol);
      if (!holding) return alert(`No holdings found for ${symbol}`);
      input.value = holding.quantity.toFixed(8);
      logMsg(`Max SELL set to ${holding.quantity.toFixed(8)} ${symbol}`);
    } else {
      const res = await fetch("https://rugplay.com/api/portfolio/summary", {
        credentials: "include",
        headers: { "User-Agent": navigator.userAgent },
        method: "GET",
        mode: "cors"
      });
      const data = await res.json();
      input.value = data.baseCurrencyBalance.toFixed(2);
      logMsg(`Max BUY set to $${data.baseCurrencyBalance.toFixed(2)}`);
    }
  } catch (err) {
    logMsg("Max fetch failed: " + err.message);
  }
};

let botRunning = false;
let botInterval;

function startTradeLoop(action, symbol, amount, delay) {
  botRunning = true;
  document.getElementById("startBtn").disabled = true;
  document.getElementById("stopBtn").disabled = false;

  botInterval = setInterval(() => {
    fetch(`https://rugplay.com/api/coin/${symbol}/trade`, {
      credentials: "include",
      headers: {
        "User-Agent": navigator.userAgent,
        "Accept": "*/*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ type: action, amount: amount }),
      method: "POST",
      mode: "cors"
    }).then(res => {
      if (!res.ok) {
        logMsg(`❌ ${action} failed: ${res.status}`);
      } else {
        logMsg(`✅ ${action} ${amount} ${symbol}`);
      }
    }).catch(err => {
      logMsg(`❌ Error: ${err.message}`);
    });
  }, delay);
}

document.getElementById("startBtn").onclick = () => {
  const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
  const amount = parseFloat(document.querySelector("#amountInput").value);
  const action = document.getElementById("actionSelect").value;
  const delay = parseInt(document.getElementById("delayInput").value);

  if (!symbol || isNaN(amount) || amount <= 0 || isNaN(delay) || delay < 10) {
    alert("Check all fields. Amount must be > 0. Delay >= 10ms.");
    return;
  }

  startTradeLoop(action, symbol, amount, delay);
};

document.getElementById("stopBtn").onclick = () => {
  botRunning = false;
  clearInterval(botInterval);
  document.getElementById("startBtn").disabled = false;
  document.getElementById("stopBtn").disabled = true;
  logMsg("🛑 Bot stopped.");
};

document.getElementById("loopBtn").onclick = async () => {
  const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
  const delay = parseInt(document.getElementById("delayInput").value);
  if (!symbol || isNaN(delay)) return alert("Check symbol and delay!");

  try {
    const buyRes = await fetch("https://rugplay.com/api/portfolio/summary", {
      credentials: "include",
      headers: { "User-Agent": navigator.userAgent },
      method: "GET",
      mode: "cors"
    });
    const buyBal = (await buyRes.json()).baseCurrencyBalance;

    await fetch(`https://rugplay.com/api/coin/${symbol}/trade`, {
      credentials: "include",
      headers: {
        "User-Agent": navigator.userAgent,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ type: "BUY", amount: buyBal }),
      method: "POST",
      mode: "cors"
    });

    logMsg(`✅ Bought $${buyBal.toFixed(2)} of ${symbol}`);

    setTimeout(async () => {
      const sellRes = await fetch("https://rugplay.com/api/portfolio/total", {
        credentials: "include",
        headers: { "User-Agent": navigator.userAgent },
        method: "GET",
        mode: "cors"
      });
      const holdings = await sellRes.json();
      const coin = holdings.coinHoldings.find(c => c.symbol.toUpperCase() === symbol);
      if (!coin) return logMsg(`❌ No ${symbol} to sell`);

      await fetch(`https://rugplay.com/api/coin/${symbol}/trade`, {
        credentials: "include",
        headers: {
          "User-Agent": navigator.userAgent,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ type: "SELL", amount: coin.quantity }),
        method: "POST",
        mode: "cors"
      });

      logMsg(`✅ Sold ${coin.quantity.toFixed(8)} ${symbol}`);
    }, delay * 5);
  } catch (err) {
    logMsg(`❌ Loop failed: ${err.message}`);
  }
};

document.getElementById("smartSellBtn").onclick = () => {
  const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
  const delay = parseInt(document.getElementById("delayInput").value);
  if (!symbol || isNaN(delay)) return alert("Enter a valid symbol and delay.");
  smartSell(symbol, delay);
};

async function smartSell(symbol, delay) {
  let sellAmount = null;
  let totalTokens = 0;

  delay = Math.max(5, delay / 2);

  async function getHoldings() {
    const res = await fetch("https://rugplay.com/api/portfolio/total", {
      credentials: "include",
      headers: { "User-Agent": navigator.userAgent },
      method: "GET",
      mode: "cors"
    });
    const data = await res.json();
    const coin = data.coinHoldings.find(c => c.symbol.toUpperCase() === symbol);
    totalTokens = coin ? coin.quantity : 0;
  }

  async function fetchMaxSellableFromError(errorText) {
    const match = errorText.match(/Max sellable: ([\d.]+)/);
    return match ? parseFloat(match[1]) : null;
  }

  async function sell(amount) {
    const resp = await fetch(`https://rugplay.com/api/coin/${symbol}/trade`, {
      credentials: "include",
      headers: {
        "User-Agent": navigator.userAgent,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ type: "SELL", amount }),
      method: "POST",
      mode: "cors"
    });

    const text = await resp.text();

    if (!resp.ok) {
      if (text.includes("Cannot sell more than 99.5% of pool tokens")) {
        const maxAllowed = await fetchMaxSellableFromError(text);
        if (maxAllowed !== null) {
          logMsg(`⚠️ Pool limit reached. Max sellable: ${maxAllowed}. Using this as starting amount.`);
          sellAmount = maxAllowed;
          return false; // will retry with new sellAmount
        } else {
          logMsg(`❌ Pool limit error but failed to parse max sellable.`);
          return false;
        }
      } else {
        logMsg(`❌ Sell failed: ${text}`);
        return false;
      }
    }

    logMsg(`✅ Sold ${amount.toFixed(6)} ${symbol}`);
    return true;
  }

  await getHoldings();

  if (totalTokens <= 0) {
    logMsg("✅ No tokens left to sell.");
    return;
  }

  if (sellAmount === null) {
    sellAmount = totalTokens;
  }

  async function sellLoop() {
    if (totalTokens <= 0) {
      logMsg("✅ Smart sell complete — no tokens left.");
      return;
    }

    if (sellAmount > totalTokens) {
      await sell(totalTokens);
      logMsg("✅ Final dump completed.");
      return;
    }

    const success = await sell(sellAmount);
    if (!success) {
      setTimeout(sellLoop, delay);
      return;
    }

    totalTokens -= sellAmount;
    sellAmount = (sellAmount * 2) - 1;

    setTimeout(sellLoop, delay);
  }

  sellLoop();
}
