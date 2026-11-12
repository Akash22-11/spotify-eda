# Spotify Track Analysis (EDA)

An exploratory data analysis of 114,000 tracks from the Spotify Tracks Dataset, looking at how audio features, genres, and track characteristics relate to track popularity.

For a concise overview of the findings, business implications, and recommended next steps, see the [Executive Summary](reports/executive_summary.md).

> **Note on dataset balance**: The cleaned dataset contains ~794 tracks per genre (113 genres). This is a **balanced sample** designed for fair cross-genre comparison and **does not reflect Spotify's natural catalog distribution**. Apply market-share weights before generalizing insights.
---
## Key findings

- **Audio features barely correlate with popularity** — contrary to common intuition, no single feature (danceability, energy, loudness, tempo) predicts popularity on its own. Loudness has the highest positive correlation, but it's weak (`r ≈ 0.07`).
- **Production intensity shows internal structure, not popularity** — Loudness and Energy correlate strongly with each other (`r = +0.76`), and both inversely with Acousticness (`r = -0.73`), reflecting production style rather than track success.
- **Genre dominates track popularity** — average popularity varies widely by genre. K-pop (59.4 avg), Pop-film (59.1), and Metal (56.4) sit at the top, while Romance (3.5) and Iranian (2.2) sit at the bottom.
- **Explicit content gets a small boost** — ~8.6% of tracks are explicit, averaging a 36.9 popularity score compared to 32.9 for clean tracks.
- **Song length and key don't matter** — duration (`r = -0.02`), musical key (`r = 0.00`), and mode (`r = -0.02`) have virtually zero linear relationship with popularity.

---

## Repository layout

```
.
├── build_eda_assets.py        
├── requirements.txt           
├── README.md
│
├── data/
│   └── spotify.csv           
│
├── notebooks/
│   └── spotify_eda.ipynb      
│
├── visuals/                   
│   ├── 01_popularity_distribution.png
│   ├── 02_top_genres_count.png
│   ├── 03_audio_features_distribution.png
│   ├── 04_popularity_vs_audio_features.png
│   ├── 05_genre_vs_popularity_violin.png
│   ├── 06_correlation_heatmap.png
│   ├── 07_key_features_pairplot.png
│   ├── 08_dance_energy_interaction.png
│   ├── 09_explicit_vs_popularity.png
│   └── 10_top_genres_by_avg_popularity.png
│
├── dashboard/
│   └── spotify_dashboard.html 
│
└── reports/                  
    ├── data_cleaning_report.md
    ├── eda_report.md
    ├── business_insights_report.md
    └── executive_summary.md
```
---

## Dataset summary

| Metric | Value |
|---|---|
| **Raw tracks** | 114,000 |
| **Cleaned tracks** | 89,740 (after dropping missing metadata and duplicate track IDs) |
| **Columns** | 21 (track_id, artists, album_name, track_name, popularity, audio features, genre) |
| **Unique genres** | 113 (balanced at ~1,000 tracks each in the raw dataset) |
| **Target feature** | `popularity` (0–100 score, Spotify metric) |
| **Missing info** | No `release_date` column — temporal analysis requires API enrichment |

### Feature summary

| Feature | Range | Average | Notes |
|---|---|---|---|
| `popularity` | 0 – 100 | 33.2 | Median 33; ~23.6% of tracks score ≥50 |
| `duration_ms` | ~8s – 87min | 3.8 min | Median 3.6 min; long tail of audiobooks/podcasts |
| `danceability` | 0.0 – 0.985 | 0.56 | Moderately right-skewed |
| `energy` | 0.0 – 1.0 | 0.64 | High-energy bias overall |
| `loudness` | -49.5 – 4.5 dB | -8.2 dB | Strongly co-varies with energy |
| `acousticness` | 0.0 – 1.0 | 0.31 | Bimodal (peaks near 0 and 1) |
| `speechiness` | 0.0 – 0.96 | 0.08 | Highly skewed, mostly music tracks |
| `tempo` | 0 – 243 BPM | 122 BPM | Median 122 BPM |

---

## Reproducing the analysis

### Setup

**Requirements**
- Python ≥ 3.9
- Dependencies in `requirements.txt` (pandas, numpy, matplotlib, seaborn, plotly, scipy, kaleido)

**Folder layout**
```
spotify-eda/
├── build_eda_assets.py    # Chart & dashboard generator
├── requirements.txt
├── data/
│   └── spotify.csv        # Place the raw CSV here (114,000 tracks)
├── notebooks/
│   └── spotify_eda.ipynb  # Full EDA notebook
├── visuals/               # Output: 10 PNG charts (300 DPI)
├── dashboard/             # Output: spotify_dashboard.html
└── reports/               # Output: 4 Markdown reports
```

```bash
# Clone the repository
git clone https://github.com/Akash22-11/spotify-eda.git
cd spotify-eda

# Optional: virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Regeneration

Run the build script to regenerate **all 10 static PNG charts** in `visuals/` and the **interactive Plotly dashboard** in `dashboard/`:

```bash
python build_eda_assets.py
```

Outputs created:
- `visuals/01_popularity_distribution.png` through `10_top_genres_by_avg_popularity.png`
- `dashboard/spotify_dashboard.html`

### Open the interactive dashboard

Open `dashboard/spotify_dashboard.html` in any browser to inspect the Plotly dashboard (genre rankings, energy vs popularity scatter, correlation heatmap, popularity distribution, explicit ratio, musical keys).

---

## License

MIT License — free to use for learning, portfolio, or reference.
