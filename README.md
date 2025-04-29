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
|:-----------:|:------------:|
| ![Login](static/screenshots/login.jpeg) | ![Home](static/screenshots/welcome.jpeg) |

| Dashboard | Telegram Bot Notification |
|:---------:|:--------------------------:|
| ![Dashboard](static/screenshots/dashboard.jpeg) | ![Telegram](static/screenshots/telegram.jpeg) |

---

## Struktur Project:
```bash
3VWeatoahriBot/
â
âââ app/
â   âââ __init__.py
â   âââ routes/
â   âââ templates/
â   âââ static/
â       âââ graphs/
â       âââ portfolio/
â       âââ screenshots/
â
âââ core/
â   âââ trading_engine.py
â   âââ risk_management.py
â   âââ portfolio_manager.py
â   âââ ai_predictor.py
â   âââ mini_chart.py
â   âââ telegram.py
â   âââ okx_sdk.py
â   âââ bot_instance.py
â
âââ uploads/
â
âââ main.py
âââ Procfile
âââ README.md
âââ requirements.txt
âââ .env (disimpan privat)
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

---

## BONUS:
- Semua grafik, chart, CSV export sudah auto-generate.
- Support Scalping, Intraday, Multi-pair.
- Auto-Telegram alert & gambar chart!

---

# 3VWeatoahriBot - Build to Make Your Trading Smarter!