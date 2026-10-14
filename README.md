# ✈️ Airline Safety Analytics Dashboard

An interactive data analytics dashboard built with Python, Pandas, Plotly, and Streamlit to explore historical airline incidents, fatal accidents, and fatalities.

The project uses a real-world airline safety dataset to compare recorded events across two periods: **1985–1999** and **2000–2014**.

## 📊 Features

- **Interactive dashboard** with key statistics and historical comparisons.
- **Colorful bar charts** for comparing airlines by recorded incidents, fatal accidents, and fatalities.
- **Pie and donut charts** showing the distribution of recorded events.
- **Grouped bar charts** comparing the two historical periods.
- **Scatter plots** exploring available seat-kilometres and recorded incidents.
- **Heatmaps** for comparing airline metrics.
- **Histograms** for exploring the distribution of recorded events.
- **Interactive filters** for airline names, historical periods, and metrics.
- **CSV export** to download filtered data.
- **Automated tests** for dataset validation and analysis functions.

## 🗂️ Dataset

The project uses `data/airline-safety.csv`, containing 56 airline records and 8 columns.

| Column | Description |
|---|---|
| `airline` | Airline name |
| `avail_seat_km_per_week` | Available seat-kilometres per week |
| `incidents_85_99` | Recorded incidents from 1985–1999 |
| `fatal_accidents_85_99` | Fatal accidents from 1985–1999 |
| `fatalities_85_99` | Fatalities from 1985–1999 |
| `incidents_00_14` | Recorded incidents from 2000–2014 |
| `fatal_accidents_00_14` | Fatal accidents from 2000–2014 |
| `fatalities_00_14` | Fatalities from 2000–2014 |

**Data interpretation:** These are historical records, not current airline safety ratings. Raw event counts do not account for differences in flight volume, routes, or operating exposure. They should not be interpreted as definitive comparisons of passenger risk.

### Dataset source

The dataset is commonly distributed as *Airline Safety* through public data repositories, including Kaggle. Verify and document the original source URL and applicable data licence before redistribution.

## 🛠️ Technologies Used

- **Python** — application logic and data processing.
- **Pandas** — loading, cleaning, filtering, and aggregating data.
- **Plotly Express and Graph Objects** — interactive charts and visualizations.
- **Streamlit** — interactive web dashboard.
- **Pytest** — automated testing.

## 📁 Project Structure

```text
Poll Results Visualize/
├── app.py
├── data/
│   └── airline-safety.csv
├── src/
│   └── analysis.py
├── tests/
│   └── test_project.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Poll Results Visualize"
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the environment (optional)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the dashboard

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

### 6. Run automated tests

```powershell
python -m pytest -q
```

## 🧪 Testing

The test suite checks:

- Dataset dimensions and required columns.
- Summary calculations.
- Historical period comparisons.
- Correct sorting of airline records.
- Handling of invalid metrics and ranking limits.

## 🚀 Future Improvements

- Add additional validated airline safety datasets.
- Include exposure-adjusted metrics when suitable denominator data is available.
- Add data-source citations and automated data validation.
- Improve accessibility and dashboard performance.
- Deploy the dashboard for public access.

## ⚠️ Disclaimer

This project is for educational and exploratory data analysis. It is not an official aviation safety assessment and should not be used on its own to make travel decisions.

## 👨‍💻 Author

Developed as a data science project to practice data cleaning, exploratory data analysis, interactive visualization, and dashboard development.
