from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import pandas as pd
import numpy as np
from datetime import datetime
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SINDHI TRADER BOT")

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

# Promo System
used_promo_codes = set()
MASTER_CODE = "SINDHIMASTER2026"

reviews = [
    {"name": "Rahim Khan", "text": "Best signals ever! Made 300+ pips this week.", "rating": 5},
    {"name": "Ayesha Malik", "text": "VIP activated, accuracy is insane.", "rating": 5},
    {"name": "Samiullah", "text": "Real analysis, not random. Highly recommended.", "rating": 5}
]

hot_setups = []  # Will be updated dynamically

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/signal")
async def get_live_signal(request: Request):
    # ... (previous real analysis code)
    pass  # use previous version

@app.post("/api/redeem-promo")
async def redeem_promo(request: Request):
    try:
        data = await request.json()
        code = data.get("code", "").strip().upper()

        if code == MASTER_CODE:
            return {"success": True, "message": "🎉 Master Access Granted - Lifetime VIP!", "status": "lifetime"}

        if code in used_promo_codes:
            return {"success": False, "message": "❌ Code already used"}

        valid_series = [f"VIP{str(i).zfill(4)}" for i in range(1, 1001)]
        if code in valid_series:
            used_promo_codes.add(code)
            return {"success": True, "message": "🎉 VIP Activated for 6 Months ($50 value)!", "status": "active", "expires": "6 months"}
        else:
            return {"success": False, "message": "❌ Invalid Promo Code"}
    except:
        return {"success": False, "message": "Error"}

@app.get("/api/reviews")
async def get_reviews():
    return reviews

@app.get("/api/hot-setups")
async def get_hot_setups():
    # Simulate real hot setups
    return [
        {"symbol": "XAUUSD", "direction": "BUY", "confidence": 92, "reason": "Strong Breakout"},
        {"symbol": "EURUSD", "direction": "SELL", "confidence": 85, "reason": "Resistance Rejection"}
    ]

@app.get("/api/news")
async def get_news():
    return {"news": "High Impact News: US CPI Today - Expect volatility in USD pairs", "impact_pairs": ["EURUSD", "GBPUSD", "USDJPY"]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
