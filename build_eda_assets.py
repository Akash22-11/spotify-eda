import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Resolve paths relative to this script's location so the project is
# portable across machines, OSes, and clone locations.
ROOT = pathlib.Path(__file__).resolve().parent
DATA_PATH    = ROOT / "data"      / "spotify.csv"
VISUALS_DIR  = ROOT / "visuals"
DASHBOARD_DIR = ROOT / "dashboard"
REPORTS_DIR  = ROOT / "reports"

os.makedirs(VISUALS_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

print("Loading dataset...")
df_raw = pd.read_csv(DATA_PATH)
print(f"Raw Shape: {df_raw.shape}")

# Drop unnamed index column if present
if 'Unnamed: 0' in df_raw.columns:
    df_raw = df_raw.drop(columns=['Unnamed: 0'])

# Clean data
df_clean = df_raw.copy()
df_clean = df_clean.dropna(subset=['artists', 'album_name', 'track_name'])
df_clean = df_clean.drop_duplicates(subset=['track_id'])
df_clean['duration_min'] = df_clean['duration_ms'] / 60000.0

print(f"Cleaned Shape: {df_clean.shape}")

# 1. Popularity Analysis Plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df_clean['popularity'], bins=30, kde=True, ax=axes[0], color='#1DB954')
axes[0].set_title("Popularity Distribution (Histogram & KDE)", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Popularity (0-100)")

sns.kdeplot(df_clean['popularity'], fill=True, ax=axes[1], color='#1ED760')
axes[1].set_title("Popularity Density (KDE)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Popularity")

sns.boxplot(x=df_clean['popularity'], ax=axes[2], color='#1DB954')
axes[2].set_title("Popularity Box Plot (Outliers & Quartiles)", fontsize=12, fontweight='bold')
axes[2].set_xlabel("Popularity")

plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "01_popularity_distribution.png"), dpi=300)
plt.close()

# 2. Top Genres Count & Distribution
top_genres = df_clean['track_genre'].value_counts().head(20)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette="viridis", ax=ax, legend=False)
ax.set_title("Top 20 Track Genres by Count", fontsize=14, fontweight='bold')
ax.set_xlabel("Number of Tracks")
ax.set_ylabel("Genre")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "02_top_genres_count.png"), dpi=300)
plt.close()

# 3. Audio Features Distribution Grid
audio_cols = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()

for i, col in enumerate(audio_cols):
    sns.histplot(df_clean[col], kde=True, ax=axes[i], color='#1DB954', bins=25)
    axes[i].set_title(f"{col.capitalize()} Distribution", fontsize=12, fontweight='bold')
    axes[i].set_xlabel(col)

plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "03_audio_features_distribution.png"), dpi=300)
plt.close()

# 4. Bivariate: Popularity vs Audio Features (Scatter + Reg plots)
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
axes = axes.flatten()
sample_df = df_clean.sample(5000, random_state=42)

bivar_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
for i, col in enumerate(bivar_cols):
    sns.regplot(data=sample_df, x=col, y='popularity', ax=axes[i],
                scatter_kws={'alpha':0.15, 'color':'#2E86AB'}, line_kws={'color':'#E63946', 'linewidth':2})
    axes[i].set_title(f"Popularity vs {col.capitalize()}", fontsize=12, fontweight='bold')
    axes[i].set_ylabel("Popularity")
    axes[i].set_xlabel(col)

plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "04_popularity_vs_audio_features.png"), dpi=300)
plt.close()

# 5. Genre vs Popularity (Top 15 Genres Violin Plot)
top15_genres = df_clean['track_genre'].value_counts().head(15).index
df_top15 = df_clean[df_clean['track_genre'].isin(top15_genres)]

fig, ax = plt.subplots(figsize=(14, 7))
sns.violinplot(data=df_top15, x="track_genre", y="popularity", hue="track_genre", palette="magma", ax=ax, inner="quartile", legend=False)
ax.set_title("Popularity Distribution across Top 15 Genres (Violin Plot)", fontsize=14, fontweight='bold')
ax.set_xlabel("Genre")
ax.set_ylabel("Popularity")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "05_genre_vs_popularity_violin.png"), dpi=300)
plt.close()

# 6. Correlation Heatmap
num_cols = ['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness',
            'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
corr_matrix = df_clean[num_cols].corr()

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, cbar_kws={'label': 'Pearson Correlation'})
ax.set_title("Spotify Audio Features Correlation Heatmap", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "06_correlation_heatmap.png"), dpi=300)
plt.close()

# 7. Pairplot of Key Features
pair_cols = ['popularity', 'danceability', 'energy', 'valence', 'loudness']
pairplot_fig = sns.pairplot(sample_df[pair_cols], diag_kind='kde', plot_kws={'alpha': 0.2, 'color': '#1DB954'})
pairplot_fig.fig.suptitle("Pairplot of Key Audio Features & Popularity", y=1.02, fontsize=14, fontweight='bold')
pairplot_fig.savefig(os.path.join(VISUALS_DIR, "07_key_features_pairplot.png"), dpi=300)
plt.close()

# 8. High Danceability + High Energy interaction analysis
# Guard against re-runs: only build the group column if it does not already exist.
if 'dance_energy_group' not in df_clean.columns:
    df_clean['dance_energy_group'] = 'Low Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'High Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] <= 0.6), 'dance_energy_group'] = 'High Dance / Low Energy'
    df_clean.loc[(df_clean['danceability'] <= 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'Low Dance / High Energy'

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_clean, x='dance_energy_group', y='popularity',
            hue='dance_energy_group', palette='Set2', ax=ax, legend=False)
ax.set_title("Popularity Impact: Danceability & Energy Interaction", fontsize=14, fontweight='bold')
ax.set_xlabel("Danceability & Energy Combination")
ax.set_ylabel("Popularity Score")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "08_dance_energy_interaction.png"), dpi=300)
plt.close()

# 9. Explicit Content vs Popularity
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_clean, x='explicit', y='popularity',
            hue='explicit', palette=['#2EC4B6', '#E71D36'], ax=ax, legend=False)
ax.set_title("Popularity Comparison: Explicit vs Clean Tracks", fontsize=14, fontweight='bold')
ax.set_xticks([0, 1])
ax.set_xticklabels(['Clean (False)', 'Explicit (True)'])
ax.set_xlabel("Track Type")
ax.set_ylabel("Popularity")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "09_explicit_vs_popularity.png"), dpi=300)
plt.close()

# 10. Top 15 Highest Average Popularity Genres
avg_pop_genre = df_clean.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).head(15)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=avg_pop_genre.values, y=avg_pop_genre.index,
            hue=avg_pop_genre.index, palette='crest', ax=ax, legend=False)
ax.set_title("Top 15 Genres by Average Track Popularity", fontsize=14, fontweight='bold')
ax.set_xlabel("Mean Popularity Score")
ax.set_ylabel("Genre")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "10_top_genres_by_avg_popularity.png"), dpi=300)
plt.close()

print("All static visual charts generated successfully.")

# Generate Interactive Plotly Dashboard HTML
print("Building interactive Plotly Dashboard...")

fig_dash = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Top 10 Genres by Average Popularity",
        "Popularity vs Energy (Scatter with Trend)",
        "Audio Feature Correlations",
        "Popularity Distribution",
        "Explicit Content Breakdown",
        "Key Musical Key Distribution"
    ),
    specs=[[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "heatmap"}, {"type": "histogram"}],
           [{"type": "pie"}, {"type": "bar"}]]
)

# 1. Top 10 Genres
top10_pop_g = df_clean.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).head(10)
fig_dash.add_trace(go.Bar(
    x=top10_pop_g.index, y=top10_pop_g.values,
    marker_color='#1DB954', name="Avg Popularity"
), row=1, col=1)

# 2. Scatter Energy vs Popularity
sample_dash = df_clean.sample(1000, random_state=42)
fig_dash.add_trace(go.Scatter(
    x=sample_dash['energy'], y=sample_dash['popularity'],
    mode='markers', marker=dict(color='#1ED760', opacity=0.5),
    name="Track Energy"
), row=1, col=2)

# 3. Heatmap
fig_dash.add_trace(go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.index,
    colorscale='Viridis', name="Correlation"
), row=2, col=1)

# 4. Popularity Histogram
fig_dash.add_trace(go.Histogram(
    x=df_clean['popularity'],
    nbinsx=30, marker_color='#2E86AB', name="Popularity Count"
), row=2, col=2)

# 5. Explicit Pie
explicit_counts = df_clean['explicit'].value_counts()
fig_dash.add_trace(go.Pie(
    labels=['Clean', 'Explicit'], values=explicit_counts.values,
    marker_colors=['#2EC4B6', '#E71D36'], name="Explicit Ratio"
), row=3, col=1)

# 6. Key Distribution
key_map = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}
df_clean['key_name'] = df_clean['key'].map(key_map)
key_counts = df_clean['key_name'].value_counts()
fig_dash.add_trace(go.Bar(
    x=key_counts.index, y=key_counts.values,
    marker_color='#FF9F1C', name="Key Count"
), row=3, col=2)

fig_dash.update_layout(
    title_text="<b>Spotify Music EDA Interactive Intelligence Dashboard</b>",
    template="plotly_dark",
    height=1200,
    showlegend=False
)

dashboard_html_path = os.path.join(DASHBOARD_DIR, "spotify_dashboard.html")
fig_dash.write_html(dashboard_html_path)
print(f"Interactive Dashboard saved to {dashboard_html_path}")

print("Assets build step complete.")
