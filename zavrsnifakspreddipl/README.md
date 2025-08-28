# Završni projekt — Brzi Start (Windows PowerShell)

## 🚀 Pokretanje projekta u 6 koraka

U PowerShellu zalijepi **redom**:

```powershell
# 1) Uđi u folder projekta
cd C:\Users\Ivan\Downloads\zavrsnifaks_diverged_aggressive_final_patched

# 2) Kreiraj i aktiviraj virtualno okruženje
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3) Instaliraj potrebne pakete
pip install -r requirements.txt

# 4) Postavi svoj NewsAPI ključ (zamijeni OVDJE_TVOJ_API_KEY)
$env:NEWS_API_KEY="OVDJE_TVOJ_API_KEY"

# 5) Inicijaliziraj bazu (napravi tablice u news.db)
python init_db.py

# 6) Pokreni aplikaciju
python run.py
```

---

## 🌍 Korištenje
Kad zadnja naredba krene, aplikacija će se pokrenuti na:  
👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## ℹ️ Napomene
- Ako se pojavi greška oko `newsapi`, ponovi:
  ```powershell
  pip install newsapi-python
  ```
- Ako `news.db` ne postoji ili nema tablica, ponovno pokreni:
  ```powershell
  python init_db.py
  ```
