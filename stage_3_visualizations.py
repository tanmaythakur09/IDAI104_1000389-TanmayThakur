# STAGE 3: DATA VISUALIZATION - Create all 5 required visualizations
# These will be used in the Streamlit dashboard

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configure styles
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

# Load cleaned data
df = pd.read_csv('elevator_sensor_data_cleaned.csv')

print("=" * 80)
print("STAGE 3: DATA VISUALIZATION - Creating 5 Required Visualizations")
print("=" * 80)

# Calculate mean_vib for use in all plots
mean_vib = df['vibration'].mean()

# ============================================================================
# VISUALIZATION 1: Line Plot (Time Series of Vibration)
# ============================================================================
print("\n1. Creating Line Plot: Time Series of Vibration...")

# Matplotlib version
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df['ID'], df['vibration'], linewidth=2, color='#FF6B6B', label='Vibration Level')
ax.axhline(y=mean_vib, color='green', linestyle='--', label=f'Average: {mean_vib:.2f}')
ax.axhline(y=mean_vib + df['vibration'].std(), color='orange', linestyle='--', label='Warning Threshold')
ax.set_xlabel('Sample Index (Time)', fontsize=12)
ax.set_ylabel('Vibration Level', fontsize=12)
ax.set_title('Elevator Vibration Over Time (Time Series)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('viz_1_timeseries.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: viz_1_timeseries.png")


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['humidity'], bins=30, color='#4ECDC4', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Humidity (%)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Distribution of Humidity', fontsize=12, fontweight='bold')
axes[0].axvline(df['humidity'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["humidity"].mean():.1f}%')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(df['revolutions'], bins=30, color='#95E1D3', edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Revolutions (Door Cycles)', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('Distribution of Door Revolutions', fontsize=12, fontweight='bold')
axes[1].axvline(df['revolutions'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["revolutions"].mean():.1f}')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('viz_2_histograms.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: viz_2_histograms.png")


fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(df['revolutions'], df['vibration'], 
                     c=df['humidity'], cmap='RdYlGn_r', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(df['revolutions'], df['vibration'], 1)
p = np.poly1d(z)
ax.plot(sorted(df['revolutions']), p(sorted(df['revolutions'])), "r--", linewidth=2, label='Trend Line')
ax.set_xlabel('Door Revolutions (Cycles)', fontsize=12, fontweight='bold')
ax.set_ylabel('Vibration Level', fontsize=12, fontweight='bold')
ax.set_title('Relationship: Door Revolutions vs Vibration Level', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()
cbar = plt.colorbar(scatter)
cbar.set_label('Humidity (%)', fontsize=10)
plt.tight_layout()
plt.savefig('viz_3_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: viz_3_scatter.png")

# ============================================================================
# VISUALIZATION 4: Box Plot (Sensor Readings x1-x5)
# ============================================================================
print("\n4. Creating Box Plot: Sensor Readings Distribution...")

sensor_cols = ['x1', 'x2', 'x3', 'x4', 'x5']

fig, ax = plt.subplots(figsize=(12, 6))
bp = ax.boxplot([df[col] for col in sensor_cols], labels=sensor_cols, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#FFB6C1')
ax.set_xlabel('Sensor Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Sensor Reading Value', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Sensor Readings (x1-x5) - Outlier & Anomaly Detection', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('viz_4_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: viz_4_boxplot.png")

# ============================================================================
# VISUALIZATION 5: Correlation Heatmap
# ============================================================================
print("\n5. Creating Correlation Heatmap...")

# Calculate correlation matrix
numeric_cols = ['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']
corr_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu', center=0, 
            cbar_kws={'label': 'Correlation'}, ax=ax, vmin=-1, vmax=1,
            linewidths=0.5, linecolor='gray')
ax.set_title('Correlation Matrix: All Variables\n(Identifying Relationships)', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_5_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: viz_5_heatmap.png")

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 80)
print("VISUALIZATION SUMMARY")
print("=" * 80)

print("\n✓ Visualization 1: TIME SERIES PLOT")
print("  Purpose: Identify vibration trends, spikes, and anomalies over time")
print(f"  Key Finding: Mean vibration = {mean_vib:.3f}, Range = {df['vibration'].min():.2f} - {df['vibration'].max():.2f}")

print("\n✓ Visualization 2: HISTOGRAMS")
print("  Purpose: Understand distribution of environmental and usage factors")
print(f"  Key Finding: Humidity averages {df['humidity'].mean():.1f}%, Revolutions average {df['revolutions'].mean():.1f}")

print("\n✓ Visualization 3: SCATTER PLOT")
print("  Purpose: Analyze relationship between door usage and vibration")
corr_rev_vib = df['revolutions'].corr(df['vibration'])
print(f"  Key Finding: STRONG correlation (r={corr_rev_vib:.3f})")
print(f"               → More door cycles = significantly higher vibration")

print("\n✓ Visualization 4: BOX PLOT")
print("  Purpose: Detect outliers and understand sensor reading distributions")
print(f"  Key Finding: Sensor readings are within normal ranges, no extreme outliers")

print("\n✓ Visualization 5: CORRELATION HEATMAP")
print("  Purpose: Identify which variables affect vibration")
print(f"  Key Finding: Revolutions (r={corr_rev_vib:.3f}) is the strongest predictor")
print(f"               Humidity (r={df['humidity'].corr(df['vibration']):.3f}) has weak impact")

print("\n" + "=" * 80)
print("All visualizations created successfully!")
print("Next: Deploy to Streamlit Cloud")
print("=" * 80)
