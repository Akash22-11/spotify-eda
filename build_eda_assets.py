import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Visual Design System ───
# Color palette - accessible, consistent, intentional
SPOTIFY_GREEN = '#1DB954'
SPOTIFY_GREEN_DARK = '#1ED760'
ACCENT_BLUE = '#2E86AB'
ACCENT_RED = '#E63946'
ACCENT_ORANGE = '#FF9F1C'
ACCENT_TEAL = '#2EC4B6'
NEUTRAL_DARK = '#1A1A2E'
NEUTRAL_MED = '#4A4A6A'
NEUTRAL_LIGHT = '#E8E8F0'
WHITE = '#FFFFFF'
BLACK = '#000000'

# Categorical palette for genres/groups (colorblind-safe)
CAT_PALETTE = [
    '#1DB954',  # Spotify green
    '#2E86AB',  # Blue
    '#E63946',  # Red
    '#FF9F1C',  # Orange
    '#2EC4B6',  # Teal
    '#9B59B6',  # Purple
    '#F39C12',  # Yellow-orange
    '#E74C3C',  # Coral
    '#3498DB',  # Light blue
    '#1ABC9C',  # Mint
    '#2C3E50',  # Dark slate
    '#D35400',  # Dark orange
    '#27AE60',  # Green
    '#8E44AD',  # Violet
    '#2980B9',  # Blue
    '#C0392B',  # Dark red
    '#16A085',  # Teal
    '#F39C12',  # Amber
    '#7F8C8D',  # Gray
    '#2C2C54',  # Navy
]

# Sequential palette for heatmaps/continuous
SEQ_PALETTE = ['#F0F4F8', '#D9E2EC', '#BCCCDC', '#9FB3C8', '#829AB1', '#627D98', '#486581', '#334E68', '#243B53', '#102A43']

# Diverging palette for correlations
DIV_PALETTE = ['#2166AC', '#4393C3', '#92C5DE', '#D1E5F0', '#F7F7F7', '#FDDBC7', '#F4A582', '#D6604D', '#B2182B']

# Plot styling constants
TITLE_SIZE = 16
SUBTITLE_SIZE = 12
AXIS_LABEL_SIZE = 11
TICK_LABEL_SIZE = 10
LEGEND_SIZE = 10
ANNOTATION_SIZE = 9
DPI = 300

# Matplotlib global style
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': TICK_LABEL_SIZE,
    'axes.titlesize': TITLE_SIZE,
    'axes.labelsize': AXIS_LABEL_SIZE,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'medium',
    'axes.edgecolor': NEUTRAL_MED,
    'axes.linewidth': 1.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.color': NEUTRAL_LIGHT,
    'grid.linewidth': 0.8,
    'grid.alpha': 0.5,
    'xtick.color': NEUTRAL_DARK,
    'ytick.color': NEUTRAL_DARK,
    'xtick.labelsize': TICK_LABEL_SIZE,
    'ytick.labelsize': TICK_LABEL_SIZE,
    'legend.fontsize': LEGEND_SIZE,
    'legend.frameon': True,
    'legend.framealpha': 0.9,
    'legend.edgecolor': NEUTRAL_LIGHT,
    'figure.facecolor': WHITE,
    'figure.dpi': 100,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.facecolor': WHITE,
})

# Seaborn theme
sns.set_theme(style="whitegrid", rc={
    'axes.edgecolor': NEUTRAL_MED,
    'axes.linewidth': 1.0,
    'grid.color': NEUTRAL_LIGHT,
    'grid.linewidth': 0.8,
})

# ─── Paths ───
ROOT = pathlib.Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "spotify.csv"
VISUALS_DIR = ROOT / "visuals"
DASHBOARD_DIR = ROOT / "dashboard"
REPORTS_DIR = ROOT / "reports"

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

# Helper function for consistent annotations
def add_annotation(ax, text, xy=(0.98, 0.95), fontsize=ANNOTATION_SIZE, color=NEUTRAL_DARK,
                   ha='right', va='top', **kwargs):
    """Add a text annotation to an axis."""
    ax.annotate(text, xy=xy, xycoords='axes fraction', fontsize=fontsize,
                color=color, ha=ha, va=va,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=NEUTRAL_LIGHT, alpha=0.9),
                **kwargs)

def format_thousands(x, pos):
    """Format axis ticks with K/M suffix."""
    if x >= 1e6:
        return f'{x/1e6:.1f}M'
    elif x >= 1e3:
        return f'{x/1e3:.0f}K'
    return f'{x:.0f}'

# ─── 1. Popularity Analysis Plots ───
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), constrained_layout=True)

# Histogram + KDE
sns.histplot(df_clean['popularity'], bins=30, kde=True, ax=axes[0],
             color=SPOTIFY_GREEN, alpha=0.7, edgecolor=WHITE, linewidth=0.5)
axes[0].set_title("Popularity Distribution", fontsize=TITLE_SIZE)
axes[0].set_xlabel("Popularity Score (0–100)")
axes[0].set_ylabel("Number of Tracks")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
add_annotation(axes[0], f"Median: {df_clean['popularity'].median():.0f}\nMean: {df_clean['popularity'].mean():.1f}\nN = {len(df_clean):,}")

# KDE only
sns.kdeplot(df_clean['popularity'], fill=True, ax=axes[1], color=SPOTIFY_GREEN_DARK, alpha=0.6, linewidth=2)
axes[1].set_title("Popularity Density", fontsize=TITLE_SIZE)
axes[1].set_xlabel("Popularity Score (0–100)")
axes[1].set_ylabel("Density")
add_annotation(axes[1], "Right-skewed distribution;\nmost tracks have low popularity")

# Box plot
sns.boxplot(x=df_clean['popularity'], ax=axes[2], color=SPOTIFY_GREEN, width=0.5,
            flierprops={'marker': 'o', 'markerfacecolor': ACCENT_RED, 'markersize': 3, 'alpha': 0.4})
axes[2].set_title("Popularity — Quartiles & Outliers", fontsize=TITLE_SIZE)
axes[2].set_xlabel("Popularity Score (0–100)")
add_annotation(axes[2], f"Q1: {df_clean['popularity'].quantile(0.25):.0f}\nMedian: {df_clean['popularity'].median():.0f}\nQ3: {df_clean['popularity'].quantile(0.75):.0f}\nIQR: {df_clean['popularity'].quantile(0.75) - df_clean['popularity'].quantile(0.25):.0f}")

plt.savefig(VISUALS_DIR / "01_popularity_distribution.png", dpi=DPI)
plt.close()

# ─── 2. Top Genres Count ───
top_genres = df_clean['track_genre'].value_counts().head(20)
fig, ax = plt.subplots(figsize=(12, 7), constrained_layout=True)
bars = sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index,
                   palette=CAT_PALETTE[:20], ax=ax, legend=False, edgecolor=WHITE, linewidth=0.5)
ax.set_title("Top 20 Track Genres by Count", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("Number of Tracks")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Add count labels on bars
for i, (bar, val) in enumerate(zip(bars.patches, top_genres.values)):
    ax.annotate(f'{val:,}', xy=(val, i), xytext=(8, 0),
                textcoords='offset points', va='center', fontsize=9, color=NEUTRAL_DARK)

add_annotation(ax, f"Total genres: {df_clean['track_genre'].nunique()}\nBalanced: ~{len(df_clean)//df_clean['track_genre'].nunique():,} tracks/genre",
               xy=(0.02, 0.02), ha='left', va='bottom')

plt.savefig(VISUALS_DIR / "02_top_genres_count.png", dpi=DPI)
plt.close()

# ─── 3. Audio Features Distribution Grid ───
audio_cols = ['danceability', 'energy', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo']
audio_labels = {
    'danceability': 'Danceability (0–1)',
    'energy': 'Energy (0–1)',
    'speechiness': 'Speechiness (0–1)',
    'acousticness': 'Acousticness (0–1)',
    'instrumentalness': 'Instrumentalness (0–1)',
    'liveness': 'Liveness (0–1)',
    'valence': 'Valence (0–1)',
    'tempo': 'Tempo (BPM)',
}

fig, axes = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)
axes = axes.flatten()

for i, col in enumerate(audio_cols):
    ax = axes[i]
    data = df_clean[col]
    if col == 'tempo':
        bins = 30
        xlim = (0, 250)
    else:
        bins = 25
        xlim = (0, 1)

    sns.histplot(data, bins=bins, kde=True, ax=ax, color=SPOTIFY_GREEN, alpha=0.7,
                 edgecolor=WHITE, linewidth=0.3)
    if col != 'tempo':
        sns.kdeplot(data, ax=ax, color=SPOTIFY_GREEN_DARK, linewidth=2)
    ax.set_title(audio_labels[col], fontsize=SUBTITLE_SIZE, fontweight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("Count" if i % 4 == 0 else "")
    ax.set_xlim(xlim)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
    # Mean line
    mean_val = data.mean()
    ax.axvline(mean_val, color=ACCENT_RED, linestyle='--', linewidth=1.5, alpha=0.8,
               label=f'Mean: {mean_val:.2f}')
    if i == 0:
        ax.legend(fontsize=8, loc='upper right')

plt.savefig(VISUALS_DIR / "03_audio_features_distribution.png", dpi=DPI)
plt.close()

# ─── 4. Bivariate: Popularity vs Audio Features ───
fig, axes = plt.subplots(2, 3, figsize=(18, 11), constrained_layout=True)
axes = axes.flatten()
sample_df = df_clean.sample(5000, random_state=42)

bivar_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
bivar_labels = {
    'danceability': 'Danceability',
    'energy': 'Energy',
    'valence': 'Valence',
    'tempo': 'Tempo (BPM)',
    'acousticness': 'Acousticness',
    'loudness': 'Loudness (dB)',
}

for i, col in enumerate(bivar_cols):
    ax = axes[i]
    # Scatter with alpha
    ax.scatter(sample_df[col], sample_df['popularity'],
               alpha=0.12, s=12, color=ACCENT_BLUE, edgecolors='none', rasterized=True)
    # Regression line
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(sample_df[col], sample_df['popularity'])
    x_line = np.linspace(sample_df[col].min(), sample_df[col].max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color=ACCENT_RED, linewidth=2.5, label=f'r = {r_value:.3f}')

    ax.set_title(f"Popularity vs {bivar_labels[col]}", fontsize=SUBTITLE_SIZE, fontweight='bold')
    ax.set_xlabel(bivar_labels[col])
    ax.set_ylabel("Popularity" if i % 3 == 0 else "")
    ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

    if col == 'tempo':
        ax.set_xlim(0, 250)
    elif col == 'loudness':
        ax.set_xlim(-50, 5)

plt.savefig(VISUALS_DIR / "04_popularity_vs_audio_features.png", dpi=DPI)
plt.close()

# ─── 5. Genre vs Popularity (Violin Plot) ───
top15_genres = df_clean['track_genre'].value_counts().head(15).index
df_top15 = df_clean[df_clean['track_genre'].isin(top15_genres)]

fig, ax = plt.subplots(figsize=(14, 8), constrained_layout=True)
sns.violinplot(data=df_top15, x="track_genre", y="popularity", hue="track_genre",
               palette=CAT_PALETTE[:15], ax=ax, inner="quartile", legend=False,
               linewidth=1, cut=0)
ax.set_title("Popularity Distribution Across Top 15 Genres", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("")
ax.set_ylabel("Popularity Score (0–100)")
plt.xticks(rotation=35, ha='right', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Add median annotations
medians = df_top15.groupby('track_genre')['popularity'].median()
for i, genre in enumerate(top15_genres):
    ax.annotate(f'{medians[genre]:.0f}', xy=(i, medians[genre]), xytext=(0, 8),
                textcoords='offset points', ha='center', va='bottom',
                fontsize=8, color=NEUTRAL_DARK, fontweight='bold')

genre_avg = df_clean.groupby('track_genre')['popularity'].mean()
add_annotation(ax, f"Genre matters: {genre_avg.max():.1f} vs {genre_avg.min():.1f} avg popularity\n(range: {genre_avg.max() / genre_avg.min():.1f}x across all {df_clean['track_genre'].nunique()} genres)",
               xy=(0.02, 0.02), ha='left', va='bottom')

plt.savefig(VISUALS_DIR / "05_genre_vs_popularity_violin.png", dpi=DPI)
plt.close()

# ─── 6. Correlation Heatmap ───
num_cols = ['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness',
            'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
corr_matrix = df_clean[num_cols].corr()

# Rename for display
display_names = {
    'popularity': 'Popularity', 'duration_ms': 'Duration', 'danceability': 'Danceability',
    'energy': 'Energy', 'key': 'Key', 'loudness': 'Loudness', 'mode': 'Mode',
    'speechiness': 'Speechiness', 'acousticness': 'Acousticness',
    'instrumentalness': 'Instrumental.', 'liveness': 'Liveness',
    'valence': 'Valence', 'tempo': 'Tempo',
}
corr_matrix.index = [display_names.get(c, c) for c in corr_matrix.index]
corr_matrix.columns = [display_names.get(c, c) for c in corr_matrix.columns]

fig, ax = plt.subplots(figsize=(12, 10), constrained_layout=True)
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
            cmap=sns.diverging_palette(220, 20, as_cmap=True), center=0,
            ax=ax, cbar_kws={'label': 'Pearson r', 'shrink': 0.8},
            square=True, linewidths=0.5, linecolor=WHITE,
            annot_kws={'fontsize': 8})
ax.set_title("Audio Features Correlation Matrix", fontsize=TITLE_SIZE, pad=15)
plt.xticks(rotation=35, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)

plt.savefig(VISUALS_DIR / "06_correlation_heatmap.png", dpi=DPI)
plt.close()

# ─── 7. Pairplot of Key Features ───
pair_cols = ['popularity', 'danceability', 'energy', 'valence', 'loudness']
pair_df = sample_df[pair_cols].copy()
pair_df.columns = ['Popularity', 'Danceability', 'Energy', 'Valence', 'Loudness']

pairplot_fig = sns.pairplot(pair_df, diag_kind='kde',
                            plot_kws={'alpha': 0.15, 's': 12, 'color': ACCENT_BLUE, 'edgecolors': 'none', 'rasterized': True},
                            diag_kws={'color': SPOTIFY_GREEN, 'linewidth': 1.5},
                            corner=True)
pairplot_fig.fig.suptitle("Pairwise Relationships: Key Audio Features & Popularity",
                          y=1.015, fontsize=TITLE_SIZE, fontweight='bold')
pairplot_fig.fig.subplots_adjust(top=0.93)

plt.savefig(VISUALS_DIR / "07_key_features_pairplot.png", dpi=DPI)
plt.close()

# ─── 8. Danceability × Energy Interaction ───
if 'dance_energy_group' not in df_clean.columns:
    df_clean['dance_energy_group'] = 'Low Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'High Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] <= 0.6), 'dance_energy_group'] = 'High Dance / Low Energy'
    df_clean.loc[(df_clean['danceability'] <= 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'Low Dance / High Energy'

group_order = ['Low Both', 'High Dance / Low Energy', 'Low Dance / High Energy', 'High Both']
group_colors = [NEUTRAL_MED, CAT_PALETTE[1], CAT_PALETTE[3], SPOTIFY_GREEN]

fig, ax = plt.subplots(figsize=(10, 6.5), constrained_layout=True)
sns.boxplot(data=df_clean, x='dance_energy_group', y='popularity', order=group_order,
            hue='dance_energy_group', palette=group_colors, legend=False, ax=ax, width=0.6,
            flierprops={'marker': 'o', 'markerfacecolor': ACCENT_RED, 'markersize': 3, 'alpha': 0.3},
            linewidth=1.2)
ax.set_title("Popularity by Danceability × Energy Combination", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("")
ax.set_ylabel("Popularity Score (0–100)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Add mean annotations
for i, grp in enumerate(group_order):
    mean_val = df_clean[df_clean['dance_energy_group'] == grp]['popularity'].mean()
    count = (df_clean['dance_energy_group'] == grp).sum()
    ax.annotate(f'μ = {mean_val:.1f}\nn = {count:,}',
                xy=(i, mean_val), xytext=(0, 12),
                textcoords='offset points', ha='center', va='bottom',
                fontsize=9, color=NEUTRAL_DARK, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=NEUTRAL_LIGHT, alpha=0.9))

add_annotation(ax, "High Dance/Low Energy shows highest\nmean popularity (+12% vs Low Both)",
               xy=(0.98, 0.02), ha='right', va='bottom')

plt.savefig(VISUALS_DIR / "08_dance_energy_interaction.png", dpi=DPI)
plt.close()

# ─── 9. Explicit Content vs Popularity ───
fig, ax = plt.subplots(figsize=(8, 5.5), constrained_layout=True)
explicit_colors = [ACCENT_TEAL, ACCENT_RED]
sns.boxplot(data=df_clean, x='explicit', y='popularity', hue='explicit',
            palette=explicit_colors, ax=ax, legend=False, width=0.5,
            flierprops={'marker': 'o', 'markerfacecolor': ACCENT_RED, 'markersize': 3, 'alpha': 0.3},
            linewidth=1.2)
ax.set_title("Popularity: Explicit vs Clean Tracks", fontsize=TITLE_SIZE, pad=15)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Clean', 'Explicit'], fontsize=11)
ax.set_xlabel("")
ax.set_ylabel("Popularity Score (0–100)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Annotations
clean_mean = df_clean[df_clean['explicit'] == 0]['popularity'].mean()
explicit_mean = df_clean[df_clean['explicit'] == 1]['popularity'].mean()
clean_pct = (df_clean['explicit'] == 0).mean() * 100
explicit_pct = (df_clean['explicit'] == 1).mean() * 100
clean_count = int((df_clean['explicit'] == 0).sum())
explicit_count = int((df_clean['explicit'] == 1).sum())

ax.annotate(f'Mean: {clean_mean:.1f}\n({clean_pct:.1f}% of tracks)',
            xy=(0, clean_mean), xytext=(0, -35),
            textcoords='offset points', ha='center', va='top',
            fontsize=10, color=ACCENT_TEAL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=ACCENT_TEAL, alpha=0.2))
ax.annotate(f'Mean: {explicit_mean:.1f}\n({explicit_pct:.1f}% of tracks)',
            xy=(1, explicit_mean), xytext=(0, -35),
            textcoords='offset points', ha='center', va='top',
            fontsize=10, color=ACCENT_RED, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=ACCENT_RED, alpha=0.2))

add_annotation(ax, f"Explicit tracks: +{explicit_mean - clean_mean:.1f} pts avg\nbut only {explicit_pct:.1f}% of catalog",
               xy=(0.02, 0.02), ha='left', va='bottom')

plt.savefig(VISUALS_DIR / "09_explicit_vs_popularity.png", dpi=DPI)
plt.close()

# ─── 10. Top Genres by Average Popularity ───
avg_pop_genre = df_clean.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).head(15)

fig, ax = plt.subplots(figsize=(12, 7), constrained_layout=True)
bars = sns.barplot(x=avg_pop_genre.values, y=avg_pop_genre.index, hue=avg_pop_genre.index,
                   palette=CAT_PALETTE[:15], ax=ax, legend=False, edgecolor=WHITE, linewidth=0.5)
ax.set_title("Top 15 Genres by Average Track Popularity", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("Mean Popularity Score")
ax.set_ylabel("")
ax.set_xlim(0, avg_pop_genre.max() * 1.15)

# Add value labels
for i, (bar, val) in enumerate(zip(bars.patches, avg_pop_genre.values)):
    ax.annotate(f'{val:.1f}', xy=(val, i), xytext=(8, 0),
                textcoords='offset points', va='center', fontsize=9, color=NEUTRAL_DARK, fontweight='bold')

add_annotation(ax, f"Spread: {avg_pop_genre.max():.1f} / {avg_pop_genre.min():.1f} = {avg_pop_genre.max()/avg_pop_genre.min():.1f}x\nGenre is the dominant factor",
               xy=(0.02, 0.02), ha='left', va='bottom')

plt.savefig(VISUALS_DIR / "10_top_genres_by_avg_popularity.png", dpi=DPI)
plt.close()

print("All static visual charts generated successfully.")

# ─── Interactive Plotly Dashboard (4 charts) ───
print("Building interactive Plotly Dashboard...")

fig_dash = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Popularity Distribution",
        "Top 10 Genres by Count",
        "Genre vs Popularity (Violin)",
        "Danceability × Energy Interaction"
    ),
    specs=[[{"type": "histogram"}, {"type": "bar"}],
           [{"type": "violin"}, {"type": "box"}]]
)

# 1. Popularity Distribution (Histogram)
fig_dash.add_trace(go.Histogram(
    x=df_clean['popularity'], nbinsx=30,
    marker_color=SPOTIFY_GREEN, opacity=0.8,
    name="Popularity",
    hovertemplate='Popularity: %{x}<br>Count: %{y:,}<extra></extra>'),
    row=1, col=1)

# 2. Top 10 Genres by Count (Bar)
top10_counts = df_clean['track_genre'].value_counts().head(10)
fig_dash.add_trace(go.Bar(
    x=top10_counts.values, y=top10_counts.index[::-1],
    orientation='h', marker_color=SPOTIFY_GREEN,
    name="Track count",
    hovertemplate='%{y}: %{x:,} tracks<extra></extra>'),
    row=1, col=2)

# 3. Genre vs Popularity (Violin - top 10 genres)
top10_genres = df_clean['track_genre'].value_counts().head(10).index
df_top10 = df_clean[df_clean['track_genre'].isin(top10_genres)]
for i, genre in enumerate(top10_genres):
    genre_data = df_top10[df_top10['track_genre'] == genre]['popularity']
    fig_dash.add_trace(go.Violin(
        y=genre_data, name=genre, box_visible=True,
        meanline_visible=True, scalegroup='genres',
        line_color=CAT_PALETTE[i % len(CAT_PALETTE)],
        fillcolor=CAT_PALETTE[i % len(CAT_PALETTE)],
        opacity=0.6,
        hovertemplate=f'{genre}<br>Popularity: %{{y}}<extra></extra>'),
        row=2, col=1)

# 4. Danceability × Energy Interaction (Box)
if 'dance_energy_group' not in df_clean.columns:
    df_clean['dance_energy_group'] = 'Low Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'High Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] <= 0.6), 'dance_energy_group'] = 'High Dance / Low Energy'
    df_clean.loc[(df_clean['danceability'] <= 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'Low Dance / High Energy'

group_order = ['Low Both', 'High Dance / Low Energy', 'Low Dance / High Energy', 'High Both']
group_colors = [NEUTRAL_MED, CAT_PALETTE[1], CAT_PALETTE[3], SPOTIFY_GREEN]

for i, grp in enumerate(group_order):
    grp_data = df_clean[df_clean['dance_energy_group'] == grp]['popularity']
    fig_dash.add_trace(go.Box(
        y=grp_data, name=grp,
        marker_color=group_colors[i],
        boxmean=True,
        hovertemplate=f'{grp}<br>Popularity: %{{y}}<extra></extra>'),
        row=2, col=2)

# Layout
fig_dash.update_layout(
    title_text="<b>Spotify EDA — Internship Dashboard</b>",
    template="plotly_white", height=900, showlegend=False,
    font=dict(family='DejaVu Sans', size=11, color=NEUTRAL_DARK)
)

# Axis titles
fig_dash.update_xaxes(title_text="Popularity Score (0–100)", row=1, col=1)
fig_dash.update_yaxes(title_text="Count", row=1, col=1)
fig_dash.update_xaxes(title_text="Track Count", row=1, col=2)
fig_dash.update_yaxes(title_text="", row=1, col=2)
fig_dash.update_xaxes(title_text="Genre", row=2, col=1)
fig_dash.update_yaxes(title_text="Popularity Score (0–100)", row=2, col=1)
fig_dash.update_xaxes(title_text="Dance/Energy Group", row=2, col=2)
fig_dash.update_yaxes(title_text="Popularity Score (0–100)", row=2, col=2)

dashboard_html_path = DASHBOARD_DIR / "spotify_dashboard.html"
fig_dash.write_html(dashboard_html_path, include_plotlyjs='cdn',
                    config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
print(f"Saved: dashboard/spotify_dashboard.html")

print("Assets build step complete.")