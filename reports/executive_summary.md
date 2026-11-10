# Executive Summary — Spotify Music EDA

**Prepared For**: College Internship Project  
**Date**: 2026-11-08  
**Author**: College Internship Project

---

## 🎯 One-Page Summary

**What we analyzed**: 89,740 Spotify tracks across 113 genres (balanced sample)  
**What we found**: **No single audio feature strongly predicts popularity** (max |r| ≈ 0.13, instrumentalness). **Genre is the dominant factor** — average popularity ranges 27× from K-pop (~59) to Iranian (~2). The "High Dance + High Energy = Hit Zone" hypothesis is not supported (+5.8% lift, not 23%).  
**What it means**: Streaming popularity is driven by genre, marketing, artist brand, and playlist placement — not by mastering louder or pushing danceability/energy. Acoustic/instrumental tracks are modestly disadvantaged but can succeed via functional verticals (sync, wellness).  
**What to do**: Enrich with release dates, build genre-normalized KPIs, retire audio-feature-based A&R signals, strengthen functional audio verticals.

> ⚠️ **Limitations**  
> - **Balanced-genre sample** (~794 tracks/genre) — insights are *comparative across genres*, not *representative of the real Spotify market*. Apply market-share weights before executive reporting.  
> - **No `release_date` column** — the dataset is a single cross-sectional snapshot, so it cannot support trend, seasonality, or genre-evolution analysis.

---

## 📊 Key Findings

| # | Finding | Evidence | Business Impact |
|---|---------|----------|-----------------|
| 1 | **No audio feature strongly predicts popularity** | Max |r| ≈ 0.13 (instrumentalness); loudness r=+0.07 | Retire loudness/energy/danceability as A&R signals |
| 2 | **"High Dance + High Energy" is not a special Hit Zone** | +5.8% lift; "High Dance / Low Energy" +11.8% | Don't prioritize "High-High" for playlist pitching |
| 3 | **Genre baseline gap: 27×** | K-pop 59.4 vs Iranian 2.2 avg popularity | Genre-normalized KPIs essential; uniform thresholds unfair |
| 4 | **Acoustic/Instrumental modestly penalized** | r = -0.04, -0.13 respectively | Niche verticals (sync, wellness, functional audio) viable path |
| 5 | **Tempo/Duration/Key/Mode irrelevant** | All |r| < 0.03 | Stop optimizing these for popularity; artistic freedom |
| 6 | **No temporal data** | `release_date` column missing | Cannot detect trends, seasonality, emerging genres — P0 fix |

---

## 🎯 Opportunities

### Immediate (0-30 days)
1. **Enrich dataset with release_date** via Spotify API (~2,000 batch calls) — enables all temporal intelligence
2. **Implement genre-normalized popularity** (z-score within genre) for fair A&R benchmarks
3. **Retire audio-feature screening** — loudness/energy/danceability don't predict hits

### Short-term (1-3 months)
4. **Strengthen Acoustic/Instrumental functional verticals** — Focus, Sleep, Study, Sync — with engagement-based metrics
5. **Build "Production Intensity" metric** — unify loudness+energy (r=+0.76) for internal tracking only
6. **Create "Bars & Hooks" rap crossover playlist** — balance high-speech verses with melodic hooks

### Medium-term (3-6 months)
7. **Develop popularity prediction model** (XGBoost on audio features + genre) for pre-release scoring
8. **Genre momentum tracker** — 30-day popularity velocity by genre (requires temporal data)
9. **Market-share weighted reporting** — apply real genre weights before executive dashboards

---

## ⚠️ Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Temporal blindness** | Certain | High | P0: API enrichment for release_date |
| **Balanced dataset bias** | Certain | Medium | Apply market-share weights; label charts as "comparative only" |
| **Niche artist marginalization** | Medium | Medium | Functional audio verticals; sync/wellness monetization |
| **Genre homogenization pressure** | Medium | High | Genre-specific success metrics; protect niche verticals |
| **Over-reliance on weak features** | Medium | Medium | Remove loudness/energy/danceability from A&R scorecards |

---

## 💡 Recommendations — Priority Order

| Priority | Recommendation | Owner | Timeline | Success Metric |
|----------|----------------|-------|----------|----------------|
| **P0** | Enrich all tracks with `release_date` via Spotify API | Data Engineering | Week 1 | 100% coverage |
| **P0** | Deploy genre-normalized popularity KPI | Analytics | Week 2 | Adoption by A&R |
| **P1** | Remove loudness/energy/danceability from A&R scorecards | A&R / Analytics | Month 1 | Scorecard updated |
| **P1** | Strengthen Acoustic/Instrumental functional verticals | Content | Month 2 | Vertical followers; sync revenue |
| **P2** | Unify Energy/Loudness → "Production Intensity" metric | ML Engineering | Month 2 | Single KPI in dashboard |
| **P2** | "Bars & Hooks" rap crossover playlist | Genre Lead | Month 3 | Crossover listener % |
| **P3** | Popularity prediction model (pre-release) | ML Engineering | Quarter 1 | AUC-ROC > 0.75 |

---

## 📈 Measurement Framework

| Strategic Goal | Leading Indicator | Lagging Indicator | Target |
|----------------|-------------------|-------------------|--------|
| **Algorithmic fairness** | Genre-normalized KPI adoption | Genre diversity in top playlists | 100% A&R adoption |
| **Hit rate improvement** | Feature-based signal retirement | A&R hit rate (signings → top 100) | Stable or improving |
| **Niche monetization** | Functional vertical followers | Sync/wellness revenue | $X ARR |
| **Temporal intelligence** | API enrichment coverage % | Trend detection lead time | 100% / 4 weeks |

---

## 📋 Data Limitations (Must Acknowledge)

1. **Balanced genre sampling** (~794 tracks/genre) — not market-representative
2. **No release_date** — cross-sectional only, no trends/seasonality
3. **Proprietary popularity metric** — algorithm undisclosed, relative only
4. **Audio features estimated** — ML model output, not ground truth
5. **Artist names not disambiguated** — semicolon format requires parsing
6. **Single snapshot** — no longitudinal view

> **All insights are comparative across genres within this dataset. Apply market-share weights before executive reporting.**

---

## 🚀 Next Steps for Leadership

1. **Approve P0 API enrichment** (Data Engineering sprint)
2. **Mandate genre-normalized KPIs** for all A&R reviews (Q1)
3. **Retire audio-feature-based A&R signals** (loudness/energy/danceability)
4. **Fund functional audio verticals** (Content budget Q1)
5. **Schedule monthly EDA refresh** with new release data

---

## Appendix: Methodology Snapshot

- **Cleaning**: Dropped 24,260 duplicate track_ids, 3 missing rows; engineered `duration_min`
- **Univariate**: 3 distribution charts (popularity, genres, 8 audio features)
- **Bivariate**: 6 regression plots (popularity vs features), genre violin, explicit box, interaction box
- **Multivariate**: 13×13 correlation heatmap, 5×5 pairplot, ANOVA on 4 interaction groups
- **Advanced**: Top artists/songs/genres, high-vs-low popularity profiles, explicit/key/mode analysis
- **Statistical**: Pearson correlations, ANOVA (F≈310, p<0.001), inter-feature correlations
- **Tools**: Python (Pandas, NumPy, SciPy), Matplotlib/Seaborn (static), Plotly (interactive dashboard)
- **Outputs**: 10 static visuals (300 DPI), 1 interactive Plotly dashboard, 4 report files, 1 reproducible build script

---

*End of Executive Summary*