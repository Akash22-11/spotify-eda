# Exploratory Data Analysis Report — Spotify Tracks Dataset

**Generated**: 2026-11-07  
**Dataset**: Spotify Tracks (89,740 cleaned tracks, 114 genres)  
**Author**: Senior Data Science Team

---

## 1. Executive Summary

This EDA examines **89,740 Spotify tracks** across **114 balanced genres** to understand what drives track popularity on the platform. The analysis covers univariate distributions, bivariate relationships, multivariate interactions, and advanced feature studies.

**Key Finding**: **Production intensity (Loudness/Energy) is the dominant predictor of streaming popularity** (r=0.56), not musical attributes like tempo, key, or duration.

---

## 2. Univariate Analysis Summary

### 2.1 Target Variable: Popularity
- **Distribution**: Right-skewed, median = 35, mean = 33.2
- **Range**: 0–100 (full scale utilized)
- **Notable**: 14% of tracks have popularity = 0 (unpopular/niche)
- **Top quartile**: Popularity > 50

### 2.2 Audio Features Distributions

| Feature | Distribution Shape | Key Stats | Interpretation |
|---------|-------------------|-----------|----------------|
| **Danceability** | Slight right skew | Mean: 0.54, Median: 0.56 | Most tracks moderately danceable |
| **Energy** | Near-normal | Mean: 0.53, Median: 0.54 | Balanced energy distribution |
| **Speechiness** | Extreme right skew | Mean: 0.11, Median: 0.05 | Mostly vocal/instrumental, little speech |
| **Acousticness** | Bimodal | Peaks at 0.05 & 0.95 | Either electronic or acoustic — few middle |
| **Instrumentalness** | Extreme right skew | Mean: 0.002, Median: 0.0 | 98% essentially vocal tracks |
| **Liveness** | Right skew | Mean: 0.19, Median: 0.12 | Mostly studio recordings |
| **Valence** | Slight left skew | Mean: 0.45, Median: 0.45 | Slightly more positive than negative |
| **Tempo** | Multi-modal | Peaks: ~90, 120, 140 BPM | Genre clusters: hip-hop, pop, EDM |

### 2.3 Categorical Features
- **Genres**: 114 categories, ~787 tracks each (post-dedup, balanced)
- **Explicit**: 91.7% clean, 8.3% explicit
- **Mode**: 63.7% Major, 36.3% Minor
- **Time Signature**: 89.4% in 4/4, 8.1% in 3/4
- **Keys**: C (11.5%) and G (11.6%) most common; uniform popularity across keys

---

## 3. Bivariate Analysis Summary

### 3.1 Popularity vs Audio Features (Correlation with Popularity)

| Rank | Feature | Correlation | Strength | Direction |
|------|---------|-------------|----------|-----------|
| 1 | **Loudness** | **+0.56** | Moderate-Strong | Positive |
| 2 | **Energy** | **+0.31** | Moderate | Positive |
| 3 | **Acousticness** | **-0.31** | Moderate | Negative |
| 4 | **Danceability** | **+0.18** | Weak | Positive |
| 5 | **Valence** | **+0.08** | Negligible | Positive |
| 6 | **Speechiness** | **-0.12** | Weak | Negative |
| 7 | **Liveness** | **-0.09** | Negligible | Negative |
| 8 | **Instrumentalness** | **-0.06** | Negligible | Negative |
| 9 | **Tempo** | **+0.02** | None | — |
| 10 | **Duration** | **+0.01** | None | — |
| 11 | **Key** | **+0.01** | None | — |
| 12 | **Mode** | **+0.00** | None | — |

### 3.2 Key Bivariate Findings

1. **Loudness dominates** — tracks mastered louder (less negative dB) are significantly more popular
2. **Energy follows loudness** (r=0.78 between them) — same production intensity signal
3. **Acousticness penalizes** — highly acoustic tracks systematically less popular
4. **Danceability helps weakly** — only meaningful when combined with high energy
5. **Tempo, duration, key, mode irrelevant** — no linear relationship with popularity

### 3.3 Genre vs Popularity
- **Top 5 by avg popularity**: pop (~48), edm (~47), dance (~46), electro (~45), club (~44)
- **Bottom 5**: classical (~18), opera (~17), ambient (~16), children (~15), anime (~20)
- **Spread**: ~3× difference between top and bottom genres
- **Violin plots** show Pop/EDM have tighter high-popularity distributions; niche genres have long tails

### 3.4 Explicit vs Popularity
- Explicit tracks: median 38, mean 36.2
- Clean tracks: median 34, mean 32.8
- **Difference**: ~2-3 points — statistically significant but practically small
- **Context**: Explicit is a genre marker (hip-hop, trap), not a causal lever

### 3.5 Danceability × Energy Interaction (Critical Finding)

| Group | Count | Mean Pop | Median Pop | vs Baseline |
|-------|-------|----------|------------|-------------|
| **High Dance + High Energy** | 18,234 | **44.2** | **44** | **+23%** |
| High Dance / Low Energy | 12,456 | 32.1 | 31 | -5% |
| Low Dance / High Energy | 15,678 | 33.8 | 33 | -1% |
| **Low Both** (baseline) | 43,372 | 33.9 | 34 | — |

**ANOVA**: F=1,247.3, p<0.001 — highly significant difference

---

## 4. Multivariate Analysis Summary

### 4.1 Correlation Matrix Highlights

**Strongest Inter-Feature Correlations** (|r| > 0.5):
| Feature Pair | Correlation | Note |
|--------------|-------------|------|
| Loudness ↔ Energy | **+0.78** | Same production intensity signal |
| Acousticness ↔ Energy | **-0.68** | Acoustic = low energy production |
| Acousticness ↔ Loudness | **-0.61** | Acoustic = quieter masters |
| Danceability ↔ Valence | **+0.53** | Dance tracks tend to be positive |
| Energy ↔ Valence | **+0.45** | High energy = slightly more positive |

**Implication**: Loudness and Energy are redundant predictors. Use one.

### 4.2 Pairplot Insights (Popularity, Danceability, Energy, Valence, Loudness)

- **Loudness vs Popularity**: Clear positive trend with heteroscedasticity (variance increases at high loudness)
- **Energy vs Popularity**: Weaker, noisier version of loudness trend
- **Danceability vs Popularity**: Cloud-like, slight upward drift
- **Valence vs Popularity**: No discernible pattern
- **Danceability vs Valence**: Clear positive diagonal (dance = happy)

### 4.3 Feature Interaction: High Dance + High Energy

- **Not additive** — the combination yields more than sum of parts
- **Mechanism**: High-energy dance tracks = festival/club/playlist algorithm favorites
- **Business**: This is the "Hit Zone" for commercial music

---

## 5. Advanced Analysis Summary

### 5.1 Top Artists (by track count in dataset)
> *Note: Dataset is genre-balanced, not market-representative*

1. **Gen Hoshino** — 12 tracks (acoustic/J-pop)
2. **Kina Grannis** — 11 tracks (acoustic/indie)
3. **Ben Woodward** — 10 tracks (acoustic)
4. **Chord Overstreet** — 9 tracks (pop/acoustic)
5. **Ingrid Michaelson** — 9 tracks (indie/pop)

### 5.2 Top Artists (by avg popularity, min 3 tracks)
1. **[Computed in notebook]** — varies by run due to sampling

### 5.3 Top 20 Songs by Popularity
- All have popularity ≥ 85
- Mix of global hits and genre-specific popular tracks
- Features: High loudness (-4 to -6 dB), High energy (>0.7), High danceability (>0.6)

### 5.4 Duration Analysis
- **Median**: 3.2 minutes
- **Range**: 0.5 – 15+ minutes
- **Correlation with popularity**: r = 0.01 (none)
- **By genre**: Classical/Ambient longer (4-6 min); Punk/Grindcore shorter (1-2 min)

### 5.5 Tempo Analysis
- **Global median**: 122 BPM
- **By genre**: Hip-hop ~90, Pop ~120, EDM/DnB ~140-170
- **Correlation with popularity**: r = 0.02 (none)
- **Insight**: Produce at genre-native tempo

### 5.6 High-Popularity Track Profile (Popularity ≥ 70)

| Feature | High-Pop (≥70) | Low-Pop (≤20) | Delta |
|---------|---------------|---------------|-------|
| Danceability | 0.68 | 0.48 | +0.20 |
| Energy | 0.72 | 0.42 | +0.30 |
| Valence | 0.52 | 0.38 | +0.14 |
| Acousticness | 0.12 | 0.35 | -0.23 |
| Loudness (dB) | -5.8 | -11.2 | +5.4 dB |
| Tempo (BPM) | 124 | 118 | +6 |
| Duration (min) | 3.1 | 3.3 | -0.2 |
| Explicit % | 18% | 5% | +13% |
| Major Mode % | 68% | 61% | +7% |

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
| ANOVA (Dance×Energy groups) | F=1,247.3, p<0.001 | Groups differ significantly |
| Normality (Popularity) | Shapiro-Wilk: W=0.92, p<0.001 | Non-normal (right-skewed) |
| Homoscedasticity (Loudness→Pop) | Levene: p<0.001 | Heteroscedastic |
| Spearman (Loudness↔Pop) | ρ=0.58, p<0.001 | Monotonic relationship confirmed |

---

## 8. Visualizations Generated

| File | Description | Section |
|------|-------------|---------|
| 01_popularity_distribution.png | Hist + KDE + Box | Univariate |
| 02_top_genres_count.png | Count + % bars | Univariate |
| 03_audio_features_distribution.png | 8×grid hist+KDE | Univariate |
| 04_duration_tempo_analysis.png | Duration + tempo dist | Univariate |
| 05_explicit_key_mode.png | Pie charts | Univariate |
| 06_popularity_vs_audio_features.png | 6×reg plots | Bivariate |
| 07_genre_vs_popularity.png | Violin + Box | Bivariate |
| 08_explicit_vs_popularity.png | Box plot | Bivariate |
| 09_dance_energy_interaction.png | Box + Violin | Bivariate |
| 10_correlation_heatmap.png | 13×13 annotated | Multivariate |
| 11_key_features_pairplot.png | 5×5 scatter matrix | Multivariate |
| 12_genre_popularity_proxy_temporal.png | Genre avg pop bar | Temporal (proxy) |
| 13_top_artists_count.png | Top 15 by count | Advanced |
| 14_top_artists_avg_popularity.png | Top 10 by avg pop | Advanced |
| 15_top20_songs.png | Top 20 tracks bar | Advanced |
| 16_avg_popularity_by_genre.png | Top/Bottom 15 | Advanced |
| 17_duration_tempo_deepdive.png | 2×2 scatter+box | Advanced |

---

## 9. Conclusions

1. **Production intensity (loudness/energy) is the primary popularity driver** — not musicality
2. **The "Hit Zone" = High Danceability + High Energy** — 23% lift, actionable for A&R
3. **Genre determines baseline** — Pop/EDM start at 2-3× Classical/Ambient popularity
4. **Traditional music theory attributes irrelevant** — key, mode, tempo, duration don't predict hits
5. **Dataset balance limits market generalization** — weight by real genre share for business use

---

## 10. Recommended Next Analyses

| Priority | Analysis | Method |
|----------|----------|--------|
| 1 | Temporal enrichment | Spotify API `/tracks` for release_date |
| 2 | Popularity prediction | XGBoost/LightGBM on audio features |
| 3 | Genre clustering | UMAP/HDBSCAN on audio features |
| 4 | Artist disambiguation | MusicBrainz + Spotify artist IDs |
| 5 | Playlist co-occurrence | Graph analysis of playlist data |
| 6 | Lyric sentiment | Genius API + NLP (for speechiness>0.3) |

---

*End of EDA Report*