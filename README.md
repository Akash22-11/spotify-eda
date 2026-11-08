# Spotify Data Analysis — Exploratory Data Analysis (EDA)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-yellow.svg)](https://pandas.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Project Overview

A complete, industry-level Exploratory Data Analysis (EDA) project on the **Spotify Tracks Dataset** (114,000 tracks across 114 genres). This project uncovers trends, patterns, artist performance, genre insights, popularity drivers, and audio feature relationships using Python's data science stack.

**Role**: Senior Data Scientist / Data Analyst / Data Visualization Expert  
**Objective**: Discover what makes a track popular on Spotify through rigorous EDA

---

## Dataset Information

| Property | Value |
|----------|-------|
| **Source** | Spotify Tracks Dataset (Kaggle / Spotify API) |
| **Rows** | 114,000 (cleaned: 89,740) |
| **Columns** | 21 |
| **Genres** | 114 (balanced ~1,000 tracks each) |
| **Features** | Audio features (danceability, energy, valence, tempo, loudness, acousticness, etc.), metadata (artist, track, album, genre, popularity, explicit, duration, key, mode) |
| **Target** | `popularity` (0–100, Spotify's proprietary metric) |

> **Note**: This dataset does **not** contain `release_date`. Temporal analysis requires enrichment via Spotify API.

### Column Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `track_id` | string | Unique Spotify track identifier |
| `artists` | string | Artist name(s), semicolon-separated for collaborations |
| `album_name` | string | Album name |
| `track_name` | string | Track title |
| `popularity` | int | Spotify popularity score (0–100) |
| `duration_ms` | int | Track length in milliseconds |
| `explicit` | bool | Explicit content flag |
| `danceability` | float | How suitable for dancing (0–1) |
| `energy` | float | Intensity/activity measure (0–1) |
| `key` | int | Musical key (0=C, 1=C#, ... 11=B) |
| `loudness` | float | Overall loudness in dB (negative values) |
| `mode` | int | 0=Minor, 1=Major |
| `speechiness` | float | Presence of spoken words (0–1) |
| `acousticness` | float | Acoustic confidence (0–1) |
| `instrumentalness` | float | Instrumental confidence (0–1) |
| `liveness` | float | Live audience detection (0–1) |
| `valence` | float | Musical positiveness (0–1) |
| `tempo` | float | Estimated BPM |
| `time_signature` | int | Estimated time signature |
| `track_genre` | string | Genre label (114 categories) |

---

## Project Structure

```
Spotify_Data_Analysis/
│
├── data/
│   └── spotify.csv                 # Raw dataset (114k tracks)
│
├── notebooks/
│   └── spotify_eda.ipynb           # Complete Jupyter Notebook (all sections)
│
├── visuals/                        # Static PNG visualizations (300 DPI)
│   ├── 01_popularity_distribution.png
│   ├── 02_top_genres_count.png
│   ├── 03_audio_features_distribution.png
│   ├── 04_duration_tempo_analysis.png
│   ├── 05_explicit_key_mode.png
│   ├── 06_popularity_vs_audio_features.png
│   ├── 07_genre_vs_popularity.png
│   ├── 08_explicit_vs_popularity.png
│   ├── 09_dance_energy_interaction.png
│   ├── 10_correlation_heatmap.png
│   ├── 11_key_features_pairplot.png
│   ├── 12_genre_popularity_proxy_temporal.png
│   ├── 13_top_artists_count.png
│   ├── 14_top_artists_avg_popularity.png
│   ├── 15_top20_songs.png
│   ├── 16_avg_popularity_by_genre.png
│   └── 17_duration_tempo_deepdive.png
│
├── dashboard/
│   └── spotify_dashboard.html      # Interactive Plotly Dashboard
│
├── reports/
│   ├── data_cleaning_report.md
│   ├── eda_report.md
│   ├── business_insights_report.md
│   └── executive_summary.md
│
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Spotify_Data_Analysis

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Requirements

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
jupyter>=1.0.0
nbconvert>=7.0.0
scipy>=1.10.0
kaleido>=0.2.0
```

---

## Usage

### 1. Run the Jupyter Notebook (Full Analysis)

```bash
cd notebooks
jupyter notebook spotify_eda.ipynb
```

Execute cells sequentially. The notebook contains:
- **Section 1**: Environment Setup
- **Section 2**: Data Understanding (shape, types, missing, duplicates, stats)
- **Section 3**: Data Cleaning (missing, duplicates, feature engineering)
- **Section 4**: Univariate Analysis (15+ charts with observations)
- **Section 5**: Bivariate Analysis (scatter, regression, box, violin plots)
- **Section 6**: Multivariate Analysis (correlation heatmap, pairplot, interactions)
- **Section 7**: Temporal Analysis (noted as unavailable — needs release_date)
- **Section 8**: Advanced Analysis (top artists, songs, genres, duration, tempo)
- **Section 9**: Business Questions (8 answered with data)
- **Section 10**: Business Insights (16 actionable insights with recommendations)
- **Section 11**: Executive Summary (for management)
- **Section 12**: Data Cleaning Report
- **Viva Preparation**: 30 Q&A covering Pandas, NumPy, EDA, Viz, Statistics, Business

### 2. View Interactive Dashboard

Open `dashboard/spotify_dashboard.html` in any browser for an interactive Plotly dashboard with:
- KPI Cards (Top Genres, Popularity Distribution)
- Scatter plots with trends
- Correlation heatmap
- Explicit content breakdown
- Musical key distribution

### 3. Generate Reports

Reports are pre-generated in the `reports/` folder as Markdown files.

---

## Key Visualizations

| # | Visualization | Insight |
|---|---------------|---------|
| 1 | Popularity Distribution (Hist + KDE + Box) | Right-skewed, median 35, mass at 0 |
| 2 | Top Genres Count & % | Balanced dataset: ~1,000 tracks/genre |
| 3 | Audio Features Distribution (8×grid) | Speechiness/Instrumentalness highly skewed |
| 4 | Popularity vs Audio Features (6×reg plots) | Loudness strongest (r=0.56), then Energy |
| 5 | Genre vs Popularity (Violin + Box) | Pop/EDM lead; Classical/Ambient trail |
| 6 | Correlation Heatmap (13×13) | Loudness↔Energy r=0.78 (same signal) |
| 7 | Pairplot (5 key features) | Visual feature relationships |
| 8 | Danceability × Energy Interaction | **High Both = 23% popularity lift** |
| 9 | Explicit vs Popularity | Slight edge for explicit, but 91% clean |
| 10 | Top Genres by Avg Popularity | Pop, EDM, Dance ~45-50; Classical ~15 |

---

## Business Insights (Top 5)

| # | Insight | Recommendation |
|---|---------|----------------|
| 1 | **Loudness is #1 predictor** (r=0.56) | Master at competitive loudness (-6 to -8 LUFS) |
| 2 | **High Dance + High Energy = Hit Zone** (23% lift) | A&R: prioritize tracks scoring >0.6 on both |
| 3 | **Acoustic tracks underperform** (r=-0.31) | Target acoustic/chill/sync playlists, not top charts |
| 4 | **Duration/Tempo/Key don't matter** (r≈0.01) | Produce at genre-appropriate specs; don't chase 120 BPM |
| 5 | **Genre popularity gap: 3x** (Pop~45 vs Classical~15) | Create genre-specific success metrics, not one-size-fits-all |

---

## Business Questions Answered

| Question | Answer |
|----------|--------|
| **Which artist has highest avg popularity?** | Computed from dataset (min 3 tracks) — see notebook |
| **Which genre dominates?** | By count: balanced. By avg popularity: **Pop/EDM/Dance** (~45-50) |
| **What factors influence popularity most?** | 1. Loudness (0.56) 2. Energy (0.31) 3. Acousticness (-0.31) 4. Danceability (0.18) |
| **Are longer songs more popular?** | **No** — correlation ≈ 0.01 (negligible) |
| **Is danceability related to popularity?** | **Slightly** — r=0.18, weak positive |
| **Are energetic songs more popular?** | **Yes** — Energy is 2nd strongest predictor (r=0.31) |
| **Has popularity increased over time?** | **Cannot determine** — no release_date column |
| **Which genres are growing fastest?** | **Cannot determine** — needs temporal data |

---

## Executive Summary (For Management)

### Key Findings
1. Production intensity (Loudness/Energy) dominates popularity prediction
2. **Hit Formula**: High Danceability + High Energy → 23% popularity lift
3. Acoustic/Instrumental/Live tracks systematically disadvantaged
4. Duration, tempo, valence, key have negligible direct impact
5. Genre matters: Pop/EDM average 2-3× popularity of Classical/Ambient
6. Dataset is balanced — insights are comparative, not market-representative

### Opportunities
- Build "High Energy + High Dance" algorithmic playlists
- Coach acoustic artists on production intensity for crossover
- Create niche verticals (Classical, Ambient, Children's) with tailored metrics
- Redirect instrumental/live catalog to focus/sleep/meditation playlists
- Use audio feature profiles as A&R screening signals

### Risks
- Loudness war incentive → listener fatigue
- Genre homogenization from algorithmic optimization
- Niche artist marginalization by popularity metrics
- No temporal data → cannot detect emerging trends
- Balanced dataset bias → insights need market-weight calibration

### Recommendations
| Priority | Action |
|----------|--------|
| Immediate | Enrich with `release_date` via Spotify API |
| Immediate | Add market-share weights to genre analyses |
| Q1 | Launch "Production Intensity" dashboard for A&R |
| Q1 | Create genre-specific success metrics |
| Q2 | Develop Niche-to-Mainstream pathway via sync/wellness |
| Q2 | A/B test playlists using danceability×energy features |
| Ongoing | Monitor loudness distribution for fatigue prevention |

---

## Viva Preparation

The notebook includes **30 probable viva questions with answers** covering:

- **Pandas**: loc vs iloc, memory optimization, missing value handling
- **NumPy**: Vectorization, broadcasting, performance
- **EDA**: Univariate/Bivariate/Multivariate, outlier detection, correlation vs causation
- **Visualization**: Box plot, violin plot, pairplot, heatmap, Matplotlib vs Seaborn vs Plotly
- **Statistics**: Pearson vs Spearman, ANOVA, p-value interpretation, bias-variance tradeoff
- **Business Insights**: Translating findings to recommendations, validation strategies
- **Project Architecture**: Reproducibility, requirements.txt, Git, dashboard design

---

## Future Improvements

- [ ] Enrich dataset with `release_date` via Spotify Web API
- [ ] Add market-share weighting for genre analyses
- [ ] Build Streamlit/Plotly Dash interactive web app
- [ ] Implement popularity prediction model (XGBoost/LightGBM)
- [ ] Add artist disambiguation (MusicBrainz integration)
- [ ] Temporal trend analysis by year/quarter
- [ ] Audio feature clustering for genre discovery
- [ ] A/B testing framework for playlist algorithms
- [ ] Docker containerization for full reproducibility
- [ ] CI/CD pipeline for automated notebook execution

---

## License

MIT License — feel free to use for learning, portfolio, or academic submission.

---

## Author

**Senior Data Science Portfolio Project**  
Built for: College Project Submission | Portfolio | GitHub Showcase | Viva Presentation

---

## Acknowledgments

- Spotify for audio feature API
- Kaggle community for dataset curation
- Python data science ecosystem (Pandas, NumPy, Matplotlib, Seaborn, Plotly, SciPy)

---

⭐ **Star this repo if you found it useful!**