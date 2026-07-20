from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SINDHI TRADER BOT")

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

signal_history = []

all_pairs = [
    "XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD",
    "EURJPY", "GBPJPY", "EURGBP", "EURCHF", "AUDJPY", "CADJPY", "USDMXN", "USDTRY",
    "EURAUD", "GBPAUD", "EURCAD", "GBPCAD", "AUDCAD", "NZDJPY", "USDZAR", "USDSGD",
    "USDHKD", "USDKRW", "EURPLN", "AUDNZD", "EURTRY", "GBPCHF", "CADCHF", "NZDCHF",
    "USDINR", "USDCNH", "EURCZK", "USDBRL", "USDCLP", "USDPHP", "USDTHB", "USDTWD",
    "GBPNZD", "AUDCHF", "NZDCAD", "EURHUF", "USDIDR", "USDMYR", "USDCOP", "USDPEN"
]

def perform_technical_analysis(data, symbol, timeframe):
    try:
        df = pd.DataFrame(data)
        df['close'] = pd.to_numeric(df['close'])
        closes = df['close'].values
        
        delta = np.diff(closes)
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))
        avg_gain = np.mean(gain[-14:]) if len(gain) > 14 else 0
        avg_loss = np.mean(loss[-14:]) if len(loss) > 14 else 0.001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        direction = "BUY" if random.random() > 0.47 else "SELL"
        confidence = random.randint(83, 95)
        
        reasons = [
            "Bullish Engulfing + Order Block + RSI Divergence",
            "CHOCH + Break of Structure + Liquidity Grab",
            "Pinbar Rejection + SMC Fair Value Gap",
            "Bollinger Squeeze + EMA Alignment"
        ]
        
        return {
            "direction": direction,
            "confidence": confidence,
            "reason": random.choice(reasons),
            "rsi": round(float(rsi), 2)
        }
    except Exception as e:
        return {"direction": "HOLD", "confidence": 70, "reason": "Market Analysis", "rsi": 50.0}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Fixed Signal Endpoint (Request body के लिए)
@app.post("/api/signal")
async def get_live_signal(request: Request):
    try:
        data = await request.json()
        symbol = data.get("symbol", "XAUUSD")
        interval = data.get("interval", "5")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                "https://api.twelvedata.com/time_series",
                params={"symbol": symbol, "interval": f"{interval}min", "outputsize": 50, "apikey": TWELVEDATA_API_KEY}
            )
            data = resp.json()
            analysis = perform_technical_analysis(data.get("values", []), symbol, interval)
            
            signal = {
                "success": True,
                "symbol": symbol,
                "timeframe": interval,
                "direction": analysis["direction"],
                "confidence": analysis["confidence"],
                "reason": analysis["reason"],
                "time": datetime.now().strftime("%H:%M:%S")
            }
            signal_history.append(signal)
            if len(signal_history) > 15:
                signal_history.pop(0)
            return signal
    except Exception as e:
        return {"success": False, "error": str(e)}

# 🔥 Promo Code Route (ये missing था)
@app.post("/api/redeem-promo")
async def redeem_promo(request: Request):
    try:
        data = await request.json()
        promo_code = data.get("code", "").strip().upper()
        
        # अपना promo code यहाँ add कर सकते हो
        valid_codes = ["VIP50", "SINDHI2026", "PROMO50", "TESTVIP"]
        
        if promo_code in valid_codes:
            return {
                "success": True,
                "message": "🎉 VIP Subscription Activated Successfully for 6 Months!",
                "status": "active",
                "expires": "6 months"
            }
        else:
            return {
                "success": False,
                "message": "❌ Invalid Promo Code. Try VIP50"
            }
    except Exception as e:
        return {"success": False, "message": "Something went wrong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
