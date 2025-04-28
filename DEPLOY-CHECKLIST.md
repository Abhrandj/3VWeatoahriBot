# Deploy Checklist - TradingBot Project

Checklist ini untuk memastikan TradingBot siap deploy dengan sempurna ke Railway (atau server lain).

---

## 1. Struktur Folder

- [x] `app/` - Berisi routes, templates, static.
- [x] `core/` - Berisi engine trading, AI, utils.
- [x] `data/` - Tempat file sementara (optional).
- [x] `strategies/` - Berisi semua strategi trading.
- [x] `utils/` - Helper functions.

## 2. File Penting

- [x] `main.py` - Starter file untuk running Flask App.
- [x] `requirements.txt` - Semua dependency Python.
- [x] `.env.example` - Template environment variables.
- [x] `railway.json` - Auto-deploy config Railway.
- [x] `README.md` - Dokumentasi project.
- [x] `.gitignore` - Bersih dari file junk.

## 3. Environment Variables

- [x] OKX_API_KEY
- [x] OKX_API_SECRET
- [x] OKX_API_PASSPHRASE
- [x] TELEGRAM_TOKEN
- [x] TELEGRAM_CHAT_ID
- [x] FLASK_ENV = production
- [x] (Optional) SECRET_KEY

## 4. Railway Setup

- [x] Connect GitHub ke Railway Project.
- [x] Deploy dari GitHub.
- [x] Set Environment Variables di Railway.
- [x] Klik Expose Service → pilih Port 5000.
- [x] Redeploy project setelah update env.
- [x] Cek URL Railway aktif dan app tampil.

## 5. Testing Checklist

- [x] Dashboard tampil normal.
- [x] Pair baru bisa ditambahkan.
- [x] Sinyal strategi dan AI muncul.
- [x] Backtest jalan lancar.
- [x] Live Prediction berjalan.
- [x] Open Trade bisa trigger ke Telegram.
- [x] Portfolio open/closed update normal.
- [x] Export CSV portfolio dan history berjalan.
- [x] Daily Report terkirim ke Telegram.

## 6. Optional Enhancements

- [ ] Multi-strategy lebih kompleks.
- [ ] Webhook TradingView integration.
- [ ] Trailing Stop dynamic improvement.
- [ ] Partial Take Profit system.
- [ ] Telegram Signal Broadcasting.

---

**Notes:**  
Pastikan semua update code dikirim lewat GitHub → Railway auto-deploy → selalu cek console logs untuk debug cepat.

---

Happy Deploying!  
Build With Passion  