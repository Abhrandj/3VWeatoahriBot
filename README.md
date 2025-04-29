# 3VWeatoahriBot  
### Trading Bot Crypto Scalping - OKX API (Python Flask Version)

---

## Fitur Utama:

**1. User Login dan Session**  
- Sistem login user berbasis CSV (`users.csv`).
- Password terenkripsi (bcrypt).
- Session login agar dashboard aman.

**2. Dashboard Trading**  
- Dashboard utama untuk monitoring.
- Pair default: BTC, ETH, SOL (bisa tambah manual).
- Chart mini setiap pair.
- Menampilkan signal kombinasi dari indikator dan AI.

**3. Portfolio Manager**  
- Melihat posisi open & closed.
- Histori transaksi otomatis disimpan.
- Export ke CSV file portfolio.

**4. Backtest Engine**  
- Upload file CSV backtest (manual).
- Atau Fetch data dari OKX otomatis (live fetch).
- Multi-Strategi Tagging (BB Breakout, EMA Pullback, Volume Spike Reversal).

**5. Live Backtest + AI Prediction**  
- Prediksi harga berikutnya menggunakan Linear Regression.
- Sinyal AI langsung muncul.
- Open Trade langsung dari tombol.
- Auto-refresh 60 detik opsional.

---

## Railway Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/8t8hpX)

---

## Screenshots:

| Login Page | Welcome Home |
|------------|--------------|
| ![](static/screenshots/screenshot_1.jpeg) | ![](static/screenshots/screenshot_2.jpeg) |

| Dashboard + Telegram | Dashboard |
|----------------------|-----------|
| ![](static/screenshots/screenshot_3.jpeg) | ![](static/screenshots/screenshot_4.jpeg) |

---

## Struktur Project:
```bash
3VWeatoahriBot/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── templates/
│   └── static/
│       ├── graphs/
│       ├── portfolio/
│       └── screenshots/
├── core/
│   ├── trading_engine.py
│   ├── risk_management.py
│   ├── portfolio_manager.py
│   ├── ai_predictor.py
│   ├── mini_chart.py
│   ├── telegram.py
│   ├── okx_sdk.py
│   └── bot_instance.py
├── main.py
├── run.py
├── requirements.txt
└── README.md
```

---

## Cara Instalasi Lokal (Replit / PC)

```bash
git clone https://github.com/Abhrandj/3VWeatoahriBot.git
cd 3VWeatoahriBot
pip install -r requirements.txt
python3 main.py
```

## Deployment Railway

- Klik tombol Railway di atas.
- Setting Environment Variable:
  - `OKX_API_KEY`
  - `OKX_API_SECRET`
  - `OKX_PASSPHRASE`
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`
- Done! Bot live auto deploy!

---

## License
MIT License - Free to Use, Customize, Improve.

This project is licensed for personal use only. Commercial distribution is prohibited without permission.

---

## BONUS:
- Semua grafik, chart, CSV export sudah auto-generate.
- Support Scalping, Intraday, Multi-pair.
- Auto-Telegram alert & gambar chart!

---

# 3VWeatoahriBot - Build to Make Your Trading Smarter!