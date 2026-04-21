# Airbnb Prices in European Cities — Auto PPTX Generator

This repository contains a **Google Colab–ready Jupyter notebook** that performs end-to-end analysis of Airbnb prices across 10 European cities and automatically produces a polished PowerPoint presentation (`.pptx`).

---

## 📁 Files

| File | Description |
|------|-------------|
| `airbnb_europe_pptx.ipynb` | Main notebook — run this in Google Colab |
| `README.md` | This file |

---

## 🚀 Quick start (Google Colab)

### Step 1 — Get the dataset
1. Go to [https://www.kaggle.com/datasets/thedevastator/airbnb-prices-in-european-cities](https://www.kaggle.com/datasets/thedevastator/airbnb-prices-in-european-cities)
2. Sign in to Kaggle and accept the dataset terms, then download and unzip.

You should have 20 CSV files following the pattern `<city>_weekdays.csv` / `<city>_weekends.csv`:

```
amsterdam_weekdays.csv   amsterdam_weekends.csv
athens_weekdays.csv      athens_weekends.csv
barcelona_weekdays.csv   barcelona_weekends.csv
berlin_weekdays.csv      berlin_weekends.csv
budapest_weekdays.csv    budapest_weekends.csv
lisbon_weekdays.csv      lisbon_weekends.csv
london_weekdays.csv      london_weekends.csv
paris_weekdays.csv       paris_weekends.csv
rome_weekdays.csv        rome_weekends.csv
vienna_weekdays.csv      vienna_weekends.csv
```

### Step 2 — Open the notebook in Colab
Click the badge below or go to [https://colab.research.google.com](https://colab.research.google.com), choose **File → Upload notebook**, and select `airbnb_europe_pptx.ipynb`.

### Step 3 — Upload CSV files to Colab
In the **Files** panel (left sidebar ▸ 📁 icon), click **Upload** and select all 20 CSV files. They will be placed in `/content/`.

### Step 4 — Run all cells
**Runtime → Run all** (or `Ctrl+F9`)

The notebook will:
1. Install `python-pptx` (the only extra dependency).
2. Load and concatenate all 20 CSVs into one combined DataFrame (51 707 rows).
3. Clean column names and drop the spurious `Unnamed: 0` index column.
4. Compute three summary tables:
   - Average `realsum` by city.
   - Average `realsum` by city and day type (weekday/weekend).
   - Average `realsum` by room type.
5. Generate and save five charts as PNG files in `/content/`:
   - **Bar chart** — average price by city.
   - **Grouped bar chart** — weekdays vs weekends by city.
   - **Box plot** — price distribution by room type.
   - **Scatter plot** — price vs person capacity (8 000-row sample).
   - **Line chart** — average price by person capacity.
6. Build a 9-slide PPTX presentation including title, dataset overview, all five charts with captions, key findings, and conclusions.
7. Save the file to `/content/Airbnb_Europe_Analysis.pptx` and trigger an automatic browser download.

---

## 📦 Dependencies

| Package | Purpose | Pre-installed in Colab? |
|---------|---------|------------------------|
| `pandas` | Data loading & manipulation | ✅ Yes |
| `matplotlib` | Plotting | ✅ Yes |
| `seaborn` | Statistical plots | ✅ Yes |
| `python-pptx` | PPTX generation | ❌ Installed by Cell 0 |

---

## 📊 Presentation structure

| Slide | Content |
|-------|---------|
| 1 | Title slide |
| 2 | Dataset & goal |
| 3 | Bar chart — average price by city |
| 4 | Grouped bar — weekdays vs weekends |
| 5 | Box plot — price by room type |
| 6 | Scatter — price vs capacity |
| 7 | Line — average price by capacity |
| 8 | Key findings |
| 9 | Conclusions & next steps |

---

## 💡 Key findings (pre-populated in the slides)

- **Amsterdam** has the highest average Airbnb price (~€573); **Athens** is the most affordable (~€152).
- Weekend prices exceed weekday prices in most cities; **Paris** is a notable exception.
- **Entire home/apt** commands the highest average price (~€324); shared rooms are cheapest (~€144).
- Price rises consistently with **person capacity**.
- Superhost status and high cleanliness ratings correlate with premium pricing.
