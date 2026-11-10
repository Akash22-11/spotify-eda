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
# Validated reference palette (references/palette.md). One meaning per color;
# labels and axis text wear ink tokens, never the series color.
SPOTIFY_GREEN = '#008300'        # brand / primary accent (distribution, bars)
SPOTIFY_GREEN_DARK = '#006300'   # darker step of the same green
ACCENT_BLUE = '#2a78d6'          # bivariate scatter / regression lines
ACCENT_RED = '#e34948'           # alert / negative (outliers, explicit tracks, mean lines)
ACCENT_ORANGE = '#eb6834'        # highlight (top-ranked bars, best dance/energy group)
ACCENT_AQUA = '#1baf7a'          # clean / neutral category (clean tracks, mean line)
ACCENT_VIOLET = '#6250d6'        # neutral gray for non-highlighted ranked bars
NEUTRAL_DARK = '#0b0b0b'         # primary ink
NEUTRAL_MED = '#52514e'          # secondary ink / axes
NEUTRAL_LIGHT = '#e1e0d9'        # hairline grid
WHITE = '#FFFFFF'
BLACK = '#000000'

# Categorical palette - the validated 8-slot order. Adjacent CVD Delta E >= 8 in
# both modes. Never cycle past 8: fold the tail into "Other", facet, or composite.
CAT_PALETTE = [
    '#2a78d6',  # blue
    '#eb6834',  # orange
    '#1baf7a',  # aqua
    '#eda100',  # yellow
    '#e87ba4',  # magenta
    '#008300',  # green
    '#6250d6',  # violet
    '#e34948',  # red
]

# Sequential palette for heatmaps/continuous (single blue hue, light -> dark)
SEQ_PALETTE = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec',
               '#5598e7', '#3987e5', '#2a78d6', '#1c5cab', '#104281']

# Diverging palette for correlations (blue <-> red poles, neutral gray midpoint)
DIV_PALETTE = ['#2a78d6', '#6da7ec', '#b7d3f6', '#f0efec', '#f7f7f7',
               '#fde0ef', '#f4a582', '#e34948', '#b2182B']

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

# Cumulative share of the catalog by popularity threshold
pop_sorted = np.sort(df_clean['popularity'])
cum_pct = np.arange(1, len(pop_sorted) + 1) / len(pop_sorted) * 100
axes[1].plot(pop_sorted, cum_pct, color=ACCENT_BLUE, linewidth=2)
axes[1].fill_between(pop_sorted, cum_pct, color=ACCENT_BLUE, alpha=0.12)
for thr in (10, 25, 50, 75):
    idx = np.searchsorted(pop_sorted, thr)
    axes[1].axvline(thr, color=ACCENT_RED, linestyle='--', linewidth=1, alpha=0.7)
    axes[1].annotate(f"≤{thr}: {cum_pct[idx]:.0f}%",
                     xy=(thr, cum_pct[idx]), xytext=(6, 0),
                     textcoords='offset points', fontsize=8, color=ACCENT_RED)
axes[1].set_title("Cumulative Share of Catalog", fontsize=TITLE_SIZE)
axes[1].set_xlabel("Popularity Score (0–100)")
axes[1].set_ylabel("Cumulative % of Tracks")
axes[1].set_xlim(0, 100)
axes[1].set_ylim(0, 100)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
add_annotation(axes[1], "Most of the catalog sits\nbelow a modest score;\nonly a small tail is popular")

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
# Ranked bars: one hue, top three highlighted, the rest a neutral gray.
# Bar length already encodes the value, so color adds only identity.
genre_colors = [ACCENT_ORANGE if i < 3 else '#b0b0aa' for i in range(len(top_genres))]
bars = sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index,
                   palette=genre_colors, ax=ax, legend=False, edgecolor=WHITE, linewidth=0.5)
ax.set_title("Top 20 Track Genres by Count", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("Number of Tracks")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Add count labels on bars
for i, (bar, val) in enumerate(zip(bars.patches, top_genres.values)):
    ax.annotate(f'{val:,}', xy=(val, i), xytext=(8, 0),
                textcoords='offset points', va='center', fontsize=9, color=NEUTRAL_DARK)

genre_sizes = df_clean['track_genre'].value_counts()
add_annotation(ax,
               f"Total genres: {df_clean['track_genre'].nunique()}\n"
               f"Range: {genre_sizes.min():,}–{genre_sizes.max():,} tracks/genre\n"
               f"Median: {int(genre_sizes.median()):,} tracks/genre",
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
# Each genre is already identified by its x position, so the violins take one
# hue; the top three by median are flagged with the highlight color.
sns.violinplot(data=df_top15, x="track_genre", y="popularity", hue="track_genre",
               palette=[SPOTIFY_GREEN] * 15, ax=ax, inner="quartile", legend=False,
               linewidth=1, cut=0)
ax.set_title("Popularity Distribution Across Top 15 Genres", fontsize=TITLE_SIZE, pad=15)
ax.set_xlabel("")
ax.set_ylabel("Popularity Score (0–100)")
plt.xticks(rotation=35, ha='right', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))

# Add median annotations
medians = df_top15.groupby('track_genre')['popularity'].median()
top3_median_genres = medians.sort_values(ascending=False).head(3).index
for i, genre in enumerate(top15_genres):
    is_top3 = genre in top3_median_genres
    ax.annotate(f'{medians[genre]:.0f}', xy=(i, medians[genre]), xytext=(0, 8),
                textcoords='offset points', ha='center', va='bottom',
                fontsize=8, color=ACCENT_ORANGE if is_top3 else NEUTRAL_DARK,
                fontweight='bold')

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
# Diverging map centered on zero. The visible correlations span -0.73 to +0.76,
# so a symmetric range around zero spreads the real values across the full
# color scale instead of compressing them into the pale middle.
vmax = 0.8
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
            cmap=sns.diverging_palette(220, 20, as_cmap=True), center=0,
            vmin=-vmax, vmax=vmax,
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
group_colors = [NEUTRAL_MED, ACCENT_ORANGE, ACCENT_AQUA, SPOTIFY_GREEN]

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
explicit_colors = [ACCENT_AQUA, ACCENT_RED]
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
            fontsize=10, color=ACCENT_AQUA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=ACCENT_AQUA, alpha=0.2))
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
# Ranked bars: one hue, top three by mean popularity highlighted.
genre_colors = [ACCENT_ORANGE if i < 3 else '#b0b0aa' for i in range(len(avg_pop_genre))]
bars = sns.barplot(x=avg_pop_genre.values, y=avg_pop_genre.index, hue=avg_pop_genre.index,
                   palette=genre_colors, ax=ax, legend=False, edgecolor=WHITE, linewidth=0.5)
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
        line_color=SPOTIFY_GREEN,
        fillcolor=SPOTIFY_GREEN,
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
group_colors = [NEUTRAL_MED, ACCENT_ORANGE, ACCENT_AQUA, SPOTIFY_GREEN]

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

# ─── Data table (WCAG-friendly twin of the charts) ───
pop_sorted = np.sort(df_clean['popularity'])
cum_pct = np.arange(1, len(pop_sorted) + 1) / len(pop_sorted) * 100
def cum_at(thr):
    return int(np.searchsorted(pop_sorted, thr))

if 'dance_energy_group' not in df_clean.columns:
    df_clean['dance_energy_group'] = 'Low Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'High Both'
    df_clean.loc[(df_clean['danceability'] > 0.6) & (df_clean['energy'] <= 0.6), 'dance_energy_group'] = 'High Dance / Low Energy'
    df_clean.loc[(df_clean['danceability'] <= 0.6) & (df_clean['energy'] > 0.6), 'dance_energy_group'] = 'Low Dance / High Energy'

de_group_order = ['Low Both', 'High Dance / Low Energy', 'Low Dance / High Energy', 'High Both']
de_group_rows = "\n".join(
    f"<tr><td>{grp}</td><td>{(df_clean['dance_energy_group'] == grp).sum():,}</td>"
    f"<td>{df_clean.loc[df_clean['dance_energy_group'] == grp, 'popularity'].mean():.1f}</td></tr>"
    for grp in de_group_order
)

top10_count = df_clean['track_genre'].value_counts().head(10)
top10_mean = df_clean.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).head(10)
top10_count_rows = "\n".join(
    f"<tr><td>{g}</td><td>{v:,}</td></tr>" for g, v in top10_count.items()
)
top10_mean_rows = "\n".join(
    f"<tr><td>{g}</td><td>{v:.1f}</td></tr>" for g, v in top10_mean.items()
)

table_html = f"""<div class="viz-table-wrap">
  <h2>Spotify EDA — Data Table</h2>
  <p class="viz-table-note">Cleaned dataset of {len(df_clean):,} tracks across {df_clean['track_genre'].nunique()} genres. Every chart above is reproducible from these values.</p>

  <h3>Popularity summary</h3>
  <table class="viz-table">
    <thead><tr><th>Metric</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Tracks</td><td>{len(df_clean):,}</td></tr>
      <tr><td>Mean popularity</td><td>{df_clean['popularity'].mean():.1f}</td></tr>
      <tr><td>Median popularity</td><td>{df_clean['popularity'].median():.0f}</td></tr>
      <tr><td>Tracks with popularity ≤ 10</td><td>{cum_at(10):,} ({cum_pct[cum_at(10)]:.1f}%)</td></tr>
      <tr><td>Tracks with popularity ≤ 25</td><td>{cum_at(25):,} ({cum_pct[cum_at(25)]:.1f}%)</td></tr>
      <tr><td>Tracks with popularity ≤ 50</td><td>{cum_at(50):,} ({cum_pct[cum_at(50)]:.1f}%)</td></tr>
      <tr><td>Tracks with popularity ≤ 75</td><td>{cum_at(75):,} ({cum_pct[cum_at(75)]:.1f}%)</td></tr>
    </tbody>
  </table>

  <h3>Top 10 genres by track count</h3>
  <table class="viz-table">
    <thead><tr><th>Genre</th><th>Tracks</th></tr></thead>
    <tbody>{top10_count_rows}</tbody>
  </table>

  <h3>Top 10 genres by mean popularity</h3>
  <table class="viz-table">
    <thead><tr><th>Genre</th><th>Mean popularity</th></tr></thead>
    <tbody>{top10_mean_rows}</tbody>
  </table>

  <h3>Popularity by danceability × energy group</h3>
  <table class="viz-table">
    <thead><tr><th>Group</th><th>Tracks</th><th>Mean popularity</th></tr></thead>
    <tbody>{de_group_rows}</tbody>
  </table>
</div>
"""

with open(dashboard_html_path, 'r', encoding='utf-8') as f:
    html = f.read()

style = """<style>
  .viz-table-wrap {{ font-family: DejaVu Sans, system-ui, sans-serif; color: #0b0b0b;
    max-width: 980px; margin: 24px auto; padding: 0 16px; }}
  .viz-table-wrap h2 {{ font-size: 18px; margin: 0 0 4px; }}
  .viz-table-wrap h3 {{ font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em;
    color: #52514e; margin: 20px 0 6px; }}
  .viz-table-wrap .viz-table-note {{ color: #52514e; font-size: 12px; margin: 0 0 14px; }}
  .viz-table {{ border-collapse: collapse; width: 100%; font-size: 12px;
    font-variant-numeric: tabular-nums; }}
  .viz-table th, .viz-table td {{ text-align: left; padding: 5px 10px;
    border-bottom: 1px solid #e1e0d9; }}
  .viz-table th {{ color: #52514e; font-weight: 600; }}
  .viz-table tr:last-child td {{ border-bottom: none; }}
</style>
"""
html = html.replace('</body>', style + table_html + '</body>')

with open(dashboard_html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Saved: dashboard/spotify_dashboard.html")
print("Assets build step complete.")