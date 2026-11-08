# Exploratory Data Analysis Report — Spotify Tracks Dataset

**Generated**: 2026-11-08  
**Dataset**: Spotify Tracks (89,740 cleaned tracks, 113 genres)  
**Author**: Senior Data Science Team

---

## 1. Executive Summary

This EDA examines **89,740 Spotify tracks** across **113 balanced genres** to understand what drives track popularity on the platform. The analysis covers univariate distributions, bivariate relationships, multivariate interactions, and advanced feature studies.

**Key Finding**: **No single audio feature strongly predicts popularity** — the highest correlation is loudness at **r = +0.07** (weak). Genre is the dominant factor: average popularity ranges from ~59 (K-pop, Pop-film) to ~2 (Iranian, Romance). Production intensity (loudness/energy) shows strong internal structure (r = +0.76 between them) but only weak marginal links to popularity.

---

## 2. Univariate Analysis Summary

### 2.1 Target Variable: Popularity
- **Distribution**: Right-skewed, median = 33, mean = 33.2
- **Range**: 0–100 (full scale utilized)
- **Notable**: ~37% of tracks have popularity < 25; ~24% score ≥ 50
- **Top quartile**: Popularity > 50

### 2.2 Audio Features Distributions

| Feature | Distribution Shape | Key Stats | Interpretation |
|---------|-------------------|-----------|----------------|
| **Danceability** | Slight right skew | Mean: 0.56, Median: 0.57 | Most tracks moderately danceable |
| **Energy** | Near-normal | Mean: 0.64, Median: 0.64 | High-energy bias overall |
| **Speechiness** | Extreme right skew | Mean: 0.08, Median: 0.05 | Mostly music, little spoken word |
| **Acousticness** | Bimodal | Peaks at 0.05 & 0.95 | Either electronic or acoustic — few middle |
| **Instrumentalness** | Extreme right skew | Mean: 0.002, Median: 0.0 | 98% essentially vocal tracks |
| **Liveness** | Right skew | Mean: 0.19, Median: 0.12 | Mostly studio recordings |
| **Valence** | Near-symmetric | Mean: 0.45, Median: 0.45 | Slightly more positive than negative |
| **Tempo** | Multi-modal | Peaks: ~90, 120, 140 BPM | Genre clusters: hip-hop, pop, EDM |
| **Loudness** | Near-normal | Mean: -8.2 dB, Median: -7.8 dB | Strong co-variation with energy |

### 2.3 Categorical Features
- **Genres**: 113 categories, ~794 tracks each (post-dedup, balanced)
- **Explicit**: 91.4% clean, 8.6% explicit
- **Mode**: 63.7% Major, 36.3% Minor
- **Time Signature**: 89.4% in 4/4, 8.1% in 3/4
- **Keys**: C (11.5%) and G (11.6%) most common; uniform popularity across keys

---

## 3. Bivariate Analysis Summary

### 3.1 Popularity vs Audio Features (Correlation with Popularity)

| Rank | Feature | Correlation | Strength | Direction |
|------|---------|-------------|----------|-----------|
| 1 | **Loudness** | **+0.072** | Weak | Positive |
| 2 | **Danceability** | **+0.064** | Weak | Positive |
| 3 | **Energy** | **+0.014** | Negligible | Positive |
| 4 | **Tempo** | **+0.007** | Negligible | — |
| 5 | **Key** | **+0.003** | Negligible | — |
| 6 | **Valence** | **-0.012** | Negligible | Negative |
| 7 | **Liveness** | **-0.014** | Negligible | Negative |
| 8 | **Mode** | **-0.016** | Negligible | Negative |
| 9 | **Duration** | **-0.023** | Negligible | Negative |
| 10 | **Acousticness** | **-0.039** | Weak | Negative |
| 11 | **Speechiness** | **-0.047** | Weak | Negative |
| 12 | **Instrumentalness** | **-0.127** | Weak | Negative |

### 3.2 Key Bivariate Findings

1. **No strong linear predictors** — every audio feature correlates weakly (|r| < 0.13) with popularity
2. **Loudness and Energy are redundant** (r = +0.76 between them) — same production intensity signal
3. **Acousticness is the strongest negative feature** (r = -0.04) — highly acoustic tracks slightly less popular
4. **Instrumentalness has the largest |r|** (r = -0.13) — but still weak
5. **Tempo, duration, key, mode irrelevant** — correlations ≤ 0.02

### 3.3 Genre vs Popularity
- **Top 5 by avg popularity**: K-pop (59.4), Pop-film (59.1), Metal (56.4), Chill (53.7), Latino (51.8)
- **Bottom 5**: Detroit-techno (11.1), Latin (9.9), Jazz (9.8), Romance (3.5), Iranian (2.2)
- **Spread**: ~27× difference between top and bottom genres (2.2 → 59.4)
- **Violin plots** show Pop/EDM have tighter high-popularity distributions; niche genres have long tails

### 3.4 Explicit vs Popularity
- Explicit tracks: mean 36.9, median 38
- Clean tracks: mean 32.9, median 34
- **Difference**: ~4 points — statistically detectable but practically small
- **Context**: Explicit is a genre marker (hip-hop, trap), not a causal lever

### 3.5 Danceability × Energy Interaction

| Group | Count | Mean Pop | Median Pop | vs Low-Both Baseline |
|-------|-------|----------|------------|----------------------|
| **High Dance + High Energy** | 25,463 | 33.2 | 34.0 | **+5.8%** |
| High Dance / Low Energy | 14,532 | 35.1 | 37.0 | **+11.8%** |
| Low Dance / High Energy | 27,871 | 33.6 | 32.0 | **+7.0%** |
| **Low Both** (baseline) | 21,874 | 31.4 | 31.0 | — |

**ANOVA**: F ≈ 310, p < 0.001 — groups differ significantly  
**Note**: The "High Dance + High Energy" group does **not** show the largest lift; "High Dance / Low Energy" does. The interaction is not a simple "Hit Zone."

---

## 4. Multivariate Analysis Summary

### 4.1 Correlation Matrix Highlights

**Strongest Inter-Feature Correlations** (|r| > 0.45):
| Feature Pair | Correlation | Note |
|--------------|-------------|------|
| Loudness ↔ Energy | **+0.76** | Same production intensity signal |
| Acousticness ↔ Energy | **-0.73** | Acoustic = low energy production |
| Acousticness ↔ Loudness | **-0.58** | Acoustic = quieter masters |
| Danceability ↔ Valence | **+0.49** | Dance tracks tend to be positive |
| Instrumentalness ↔ Loudness | **-0.44** | Instrumental = quieter masters |

**Implication**: Loudness and Energy are redundant predictors. Use one.

### 4.2 Pairplot Insights (Popularity, Danceability, Energy, Valence, Loudness)

- **Loudness vs Popularity**: Very slight positive trend, high variance at all loudness levels
- **Energy vs Popularity**: Near-flat cloud, no discernible trend
- **Danceability vs Popularity**: Cloud-like, very slight upward drift
- **Valence vs Popularity**: No discernible pattern
- **Danceability vs Valence**: Clear positive diagonal (dance tracks tend to be positive)

### 4.3 High-Popularity vs Low-Popularity Track Profile

| Feature | High-Pop (≥70) | Low-Pop (≤20) | Delta |
|---------|---------------|---------------|-------|
| Danceability | 0.62 | 0.56 | +0.06 |
| Energy | 0.66 | 0.63 | +0.04 |
| Valence | 0.51 | 0.46 | +0.05 |
| Acousticness | 0.23 | 0.33 | -0.10 |
| Loudness (dB) | -6.7 | -9.0 | +2.3 dB |
| Tempo (BPM) | 121 | 122 | -1 |
| Duration (min) | 3.62 | 3.88 | -0.26 |
| Explicit % | 17.9% | 6.9% | +11.0% |
| Major Mode % | 61% | 63% | -2% |

---

## 5. Advanced Analysis Summary

### 5.1 Top Artists (by track count in dataset)
> *Note: Dataset is genre-balanced, not market-representative*

1. **George Jones** — 260 tracks (country, avg pop 16.6)
2. **My Little Airport** — 171 tracks (indie pop, avg pop 33.2)
3. **The Beatles** — 149 tracks (rock, avg pop 60.3)
4. **BTS** — 143 tracks (K-pop, avg pop 67.9)
5. **Håkan Hellström** — 141 tracks (Swedish pop, avg pop 30.7)

### 5.2 Top Artists (by avg popularity, min 3 tracks)
1. **Harry Styles** — 3 tracks, avg 92.0
2. **Olivia Rodrigo** — 5 tracks, avg 87.4
3. **Bad Bunny** — 22 tracks, avg 85.4
4. **IVE** — 3 tracks, avg 84.0
5. **Morgan Wallen** — 3 tracks, avg 83.3

### 5.3 Top 20 Songs by Popularity
- All have popularity ≥ 85
- Mix of global hits and genre-specific popular tracks
- Typical features: Higher danceability/energy/valence, lower acousticness, louder masters

### 5.4 Duration Analysis
- **Median**: 3.55 minutes
- **Range**: ~0.5 – 15+ minutes
- **Correlation with popularity**: r = -0.023 (none)
- **By genre**: Classical/Ambient longer (4-6 min); Punk/Grindcore shorter (1-2 min)

### 5.5 Tempo Analysis
- **Global median**: 122 BPM
- **By genre**: Hip-hop ~90, Pop ~120, EDM/DnB ~140-170
- **Correlation with popularity**: r = +0.007 (none)
- **Insight**: Produce at genre-native tempo

---

## 6. Temporal Analysis — LIMITATION

**No `release_date` column in dataset.**

Cannot perform:
- Songs released per year/month
- Popularity trends over time
- Genre evolution/trend detection
- Artist career trajectory analysis
- Seasonal release patterns

**Required for temporal analysis**: Enrich via Spotify Web API `GET /tracks/{id}` endpoint.

---

## 7. Statistical Validations

| Test | Result | Interpretation |
|------|--------|----------------|
| ANOVA (Dance×Energy groups) | F ≈ 310, p < 0.001 | Groups differ significantly |
| Normality (Popularity) | Shapiro-Wilk: W ≈ 0.92, p < 0.001 | Non-normal (right-skewed) |
| Spearman (Loudness↔Pop) | ρ ≈ +0.08, p < 0.001 | Monotonic but very weak |

---

## 8. Visualizations Generated

| File | Description | Section |
|------|-------------|---------|
| 01_popularity_distribution.png | Hist + KDE + Box | Univariate |
| 02_top_genres_count.png | Count + % bars | Univariate |
| 03_audio_features_distribution.png | 8×grid hist+KDE | Univariate |
| 04_popularity_vs_audio_features.png | 6×reg plots | Bivariate |
| 05_genre_vs_popularity_violin.png | Violin + Box | Bivariate |
| 06_correlation_heatmap.png | 13×13 annotated | Multivariate |
| 07_key_features_pairplot.png | 5×5 scatter matrix | Multivariate |
| 08_dance_energy_interaction.png | Box + Violin | Bivariate |
| 09_explicit_vs_popularity.png | Box plot | Bivariate |
| 10_top_genres_by_avg_popularity.png | Top 15 bar | Bivariate |

---

## 9. Conclusions

1. **Audio features are weak individual predictors of popularity** — none exceeds |r| = 0.13
2. **Genre determines baseline popularity** — K-pop/Pop-film/Metal start ~25-27× higher than Iranian/Romance
3. **Production intensity (loudness/energy) is internally consistent** (r = +0.76) but only weakly linked to popularity
4. **Traditional music theory attributes irrelevant** — key, mode, tempo, duration don't predict hits
5. **The "High Dance + High Energy = Hit Zone" hypothesis is not supported** — the largest lift is actually in "High Dance / Low Energy"
6. **Dataset balance limits market generalization** — weight by real genre share for business decisions

---

## 10. Recommended Next Analyses

| Priority | Analysis | Method |
|----------|----------|--------|
| 1 | Temporal enrichment | Spotify API `/tracks` for `release_date` |
| 2 | Popularity prediction | XGBoost/LightGBM on audio features + genre |
| 3 | Genre clustering | UMAP/HDBSCAN on audio features |
| 4 | Artist disambiguation | MusicBrainz + Spotify artist IDs |
| 5 | Playlist co-occurrence | Graph analysis of playlist data |
| 6 | Lyric sentiment | Genius API + NLP (for speechiness > 0.3) |

---

*End of EDA Report*