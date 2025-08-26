# Data Analysis Examples

This page demonstrates how to use PyEPISuite for comprehensive data analysis workflows, from basic property exploration to advanced statistical analysis.

## Setup

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import (
    episuite_to_dataframe,
    ecosar_to_dataframe,
    combine_episuite_ecosar_dataframes,
    create_summary_statistics
)

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

## Dataset Preparation

Let's analyze a diverse set of chemicals including pharmaceuticals, pesticides, and industrial chemicals:

```python
# Define a comprehensive dataset
chemicals = {
    'pharmaceuticals': ['50-78-2', '58-08-2', '50-02-2'],  # Aspirin, Caffeine, Dexamethasone
    'pesticides': ['50-29-3', '72-20-8', '309-00-2'],      # DDT, Endrin, Aldrin
    'industrial': ['100-41-4', '108-88-3', '71-43-2'],     # Ethylbenzene, Toluene, Benzene
    'solvents': ['67-56-1', '64-17-5', '67-64-1'],         # Methanol, Ethanol, Acetone
}

# Flatten the list
all_cas = [cas for category in chemicals.values() for cas in category]

# Get data
print(f"Analyzing {len(all_cas)} chemicals...")
ids = search_episuite_by_cas(all_cas)
epi_results, ecosar_results = submit_to_episuite(ids)

# Convert to DataFrames
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)
combined_df = combine_episuite_ecosar_dataframes(epi_df, ecosar_df)

# Add chemical categories
category_map = {}
for category, cas_list in chemicals.items():
    for cas in cas_list:
        category_map[cas] = category

epi_df['category'] = epi_df['cas'].map(category_map)
combined_df['category'] = combined_df['cas'].map(category_map)

print(f"Successfully analyzed {len(epi_df)} chemicals")
print(f"Categories: {epi_df['category'].value_counts().to_dict()}")
```

## Exploratory Data Analysis

### Property Distributions by Category

```python
# Select key properties for analysis
key_properties = [
    'log_kow_estimated',
    'water_solubility_logkow_estimated',
    'log_bioconcentration_factor',
    'atmospheric_half_life_estimated',
    'vapor_pressure_estimated'
]

# Create subplots for each property
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for i, prop in enumerate(key_properties):
    ax = axes[i]
    
    # Box plot by category
    epi_df.boxplot(column=prop, by='category', ax=ax)
    ax.set_title(f'{prop.replace("_", " ").title()}')
    ax.set_xlabel('Chemical Category')
    ax.set_ylabel('Value')
    
    # Rotate x-axis labels
    ax.tick_params(axis='x', rotation=45)

# Remove empty subplot
if len(key_properties) < len(axes):
    fig.delaxes(axes[-1])

plt.tight_layout()
plt.suptitle('Property Distributions by Chemical Category', y=1.02)
plt.show()
```

### Correlation Analysis

```python
# Calculate correlations for numeric properties
numeric_props = epi_df.select_dtypes(include=[np.number]).columns.tolist()
numeric_props = [col for col in numeric_props if 'estimated' in col or col in ['molecular_weight']]

# Create correlation matrix
corr_matrix = epi_df[numeric_props].corr()

# Plot enhanced heatmap
plt.figure(figsize=(14, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix, 
    mask=mask,
    annot=True, 
    cmap='RdBu_r', 
    center=0,
    square=True,
    linewidths=0.5,
    cbar_kws={"shrink": 0.8}
)
plt.title('Property Correlation Matrix', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Find strongest correlations
corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_pairs.append({
            'property1': corr_matrix.columns[i],
            'property2': corr_matrix.columns[j],
            'correlation': corr_matrix.iloc[i, j]
        })

corr_df = pd.DataFrame(corr_pairs)
print("\\nStrongest correlations (|r| > 0.7):")
strong_corr = corr_df[abs(corr_df['correlation']) > 0.7].sort_values('correlation', key=abs, ascending=False)
print(strong_corr.head(10).to_string(index=False))
```

## Advanced Analysis

### Principal Component Analysis

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Prepare data for PCA
pca_props = [
    'log_kow_estimated', 'water_solubility_logkow_estimated',
    'log_bioconcentration_factor', 'atmospheric_half_life_estimated',
    'vapor_pressure_estimated', 'molecular_weight'
]

# Remove rows with missing values
pca_data = epi_df[pca_props + ['category', 'name']].dropna()

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(pca_data[pca_props])

# Perform PCA
pca = PCA()
pca_result = pca.fit_transform(scaled_features)

# Create DataFrame with PCA results
pca_df = pd.DataFrame(
    pca_result[:, :3], 
    columns=['PC1', 'PC2', 'PC3'],
    index=pca_data.index
)
pca_df['category'] = pca_data['category']
pca_df['name'] = pca_data['name']

# Plot explained variance
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('PCA Explained Variance')

plt.subplot(1, 2, 2)
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), 
         np.cumsum(pca.explained_variance_ratio_), 'bo-')
plt.xlabel('Principal Component')
plt.ylabel('Cumulative Explained Variance')
plt.title('Cumulative Explained Variance')
plt.axhline(y=0.8, color='r', linestyle='--', alpha=0.7, label='80%')
plt.legend()

plt.tight_layout()
plt.show()

print(f"First 3 components explain {sum(pca.explained_variance_ratio_[:3]):.1%} of variance")

# Plot PCA results
plt.figure(figsize=(12, 8))
categories = pca_df['category'].unique()
colors = plt.cm.Set1(np.linspace(0, 1, len(categories)))

for category, color in zip(categories, colors):
    mask = pca_df['category'] == category
    plt.scatter(pca_df.loc[mask, 'PC1'], pca_df.loc[mask, 'PC2'], 
                c=[color], label=category, alpha=0.7, s=100)

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('PCA of Chemical Properties')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Feature loadings
loadings = pd.DataFrame(
    pca.components_[:3].T,
    columns=['PC1', 'PC2', 'PC3'],
    index=pca_props
)
print("\\nFeature loadings (first 3 components):")
print(loadings.round(3))
```

### Clustering Analysis

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Determine optimal number of clusters
k_range = range(2, 8)
silhouette_scores = []
inertias = []

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_features)
    silhouette_avg = silhouette_score(scaled_features, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    inertias.append(kmeans.inertia_)

# Plot elbow curve and silhouette scores
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(k_range, inertias, 'bo-')
ax1.set_xlabel('Number of Clusters (k)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method')
ax1.grid(True, alpha=0.3)

ax2.plot(k_range, silhouette_scores, 'ro-')
ax2.set_xlabel('Number of Clusters (k)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Analysis')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Perform clustering with optimal k
optimal_k = k_range[np.argmax(silhouette_scores)]
print(f"Optimal number of clusters: {optimal_k}")

kmeans = KMeans(n_clusters=optimal_k, random_state=42)
cluster_labels = kmeans.fit_predict(scaled_features)

# Add cluster labels to DataFrame
pca_data_clustered = pca_data.copy()
pca_data_clustered['cluster'] = cluster_labels

# Visualize clusters in PCA space
plt.figure(figsize=(12, 8))
scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], 
                     c=cluster_labels, cmap='viridis', alpha=0.7, s=100)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Chemical Clusters in PCA Space')
plt.colorbar(scatter, label='Cluster')

# Add cluster centers
centers_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(centers_pca[:, 0], centers_pca[:, 1], 
           c='red', marker='x', s=200, linewidths=3, label='Centroids')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Analyze cluster characteristics
print("\\nCluster Characteristics:")
cluster_summary = pca_data_clustered.groupby('cluster')[pca_props].mean()
print(cluster_summary.round(3))

print("\\nChemicals by cluster:")
for cluster in range(optimal_k):
    chemicals_in_cluster = pca_data_clustered[pca_data_clustered['cluster'] == cluster]['name'].tolist()
    print(f"Cluster {cluster}: {', '.join(chemicals_in_cluster)}")
```

## Environmental Risk Assessment

### Bioaccumulation Potential

```python
# Classify chemicals by bioaccumulation potential
def classify_bioaccumulation(log_bcf):
    if pd.isna(log_bcf):
        return 'Unknown'
    elif log_bcf < 2:
        return 'Low'
    elif log_bcf < 3:
        return 'Moderate'
    else:
        return 'High'

epi_df['bcf_category'] = epi_df['log_bioconcentration_factor'].apply(classify_bioaccumulation)

# Plot bioaccumulation categories
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Overall distribution
bcf_counts = epi_df['bcf_category'].value_counts()
ax1.pie(bcf_counts.values, labels=bcf_counts.index, autopct='%1.1f%%', startangle=90)
ax1.set_title('Bioaccumulation Potential Distribution')

# By chemical category
bcf_by_category = pd.crosstab(epi_df['category'], epi_df['bcf_category'])
bcf_by_category.plot(kind='bar', stacked=True, ax=ax2)
ax2.set_title('Bioaccumulation Potential by Chemical Category')
ax2.set_xlabel('Chemical Category')
ax2.set_ylabel('Number of Chemicals')
ax2.legend(title='BCF Category')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

print("Bioaccumulation classification:")
print(bcf_by_category)
```

### Persistence Assessment

```python
# Classify persistence based on atmospheric half-life
def classify_persistence(half_life_hours):
    if pd.isna(half_life_hours):
        return 'Unknown'
    elif half_life_hours < 24:
        return 'Non-persistent'
    elif half_life_hours < 168:  # 1 week
        return 'Moderately persistent'
    else:
        return 'Persistent'

epi_df['persistence_category'] = epi_df['atmospheric_half_life_estimated'].apply(classify_persistence)

# Create risk matrix
risk_matrix = pd.crosstab(epi_df['persistence_category'], epi_df['bcf_category'])

# Plot risk matrix heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(risk_matrix, annot=True, fmt='d', cmap='Reds', 
            cbar_kws={'label': 'Number of Chemicals'})
plt.title('Environmental Risk Matrix\\n(Persistence vs Bioaccumulation)')
plt.xlabel('Bioaccumulation Potential')
plt.ylabel('Persistence')
plt.tight_layout()
plt.show()

print("Environmental Risk Matrix:")
print(risk_matrix)

# Identify high-risk chemicals
high_risk = epi_df[
    (epi_df['persistence_category'] == 'Persistent') & 
    (epi_df['bcf_category'] == 'High')
]

if len(high_risk) > 0:
    print(f"\\nHigh-risk chemicals (Persistent + High BCF): {len(high_risk)}")
    print(high_risk[['name', 'cas', 'log_bioconcentration_factor', 
                     'atmospheric_half_life_estimated']].to_string(index=False))
else:
    print("\\nNo chemicals classified as high-risk (Persistent + High BCF)")
```

## Ecotoxicity Analysis

```python
# Analyze EcoSAR predictions
print("EcoSAR Analysis Summary:")
print(f"Total predictions: {len(ecosar_df)}")
print(f"Unique chemicals: {ecosar_df['cas'].nunique()}")
print(f"Organisms: {', '.join(ecosar_df['organism'].unique())}")
print(f"Endpoints: {', '.join(ecosar_df['endpoint'].unique())}")

# Plot toxicity distributions by organism
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

organisms = ecosar_df['organism'].unique()
for i, organism in enumerate(organisms):
    org_data = ecosar_df[ecosar_df['organism'] == organism]
    
    # Log-transform concentrations for better visualization
    log_conc = np.log10(org_data['concentration'])
    
    axes[i].hist(log_conc, bins=15, alpha=0.7, edgecolor='black')
    axes[i].set_title(f'{organism.title()} Toxicity')
    axes[i].set_xlabel('Log10 Concentration (mg/L)')
    axes[i].set_ylabel('Frequency')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Most toxic chemicals (lowest concentrations)
print("\\nMost toxic chemicals by organism:")
for organism in organisms:
    org_data = ecosar_df[ecosar_df['organism'] == organism]
    most_toxic = org_data.nsmallest(3, 'concentration')[['cas', 'concentration', 'endpoint']]
    print(f"\\n{organism.title()}:")
    for _, row in most_toxic.iterrows():
        chemical_name = epi_df[epi_df['cas'] == row['cas']]['name'].iloc[0] if len(epi_df[epi_df['cas'] == row['cas']]) > 0 else 'Unknown'
        print(f"  {chemical_name} (CAS: {row['cas']}): {row['concentration']:.3f} mg/L ({row['endpoint']})")
```

## Statistical Analysis

### ANOVA: Property Differences Between Categories

```python
from scipy import stats

# Perform ANOVA for each property
properties_for_anova = [
    'log_kow_estimated', 'water_solubility_logkow_estimated',
    'log_bioconcentration_factor', 'atmospheric_half_life_estimated'
]

anova_results = []

for prop in properties_for_anova:
    # Prepare data for ANOVA (remove NaN values)
    clean_data = epi_df[[prop, 'category']].dropna()
    
    # Group by category
    groups = [group[prop].values for name, group in clean_data.groupby('category')]
    
    # Perform ANOVA
    f_stat, p_value = stats.f_oneway(*groups)
    
    anova_results.append({
        'property': prop,
        'f_statistic': f_stat,
        'p_value': p_value,
        'significant': p_value < 0.05
    })

anova_df = pd.DataFrame(anova_results)
print("ANOVA Results (Property differences between chemical categories):")
print(anova_df.round(4))

# Post-hoc analysis for significant results
significant_props = anova_df[anova_df['significant']]['property'].tolist()

if significant_props:
    print(f"\\nSignificant differences found in: {', '.join(significant_props)}")
    
    # Perform Tukey's HSD test for significant properties
    from scipy.stats import tukey_hsd
    
    for prop in significant_props[:2]:  # Limit to first 2 for brevity
        clean_data = epi_df[[prop, 'category']].dropna()
        groups = [group[prop].values for name, group in clean_data.groupby('category')]
        categories = list(clean_data.groupby('category').groups.keys())
        
        try:
            tukey_result = tukey_hsd(*groups)
            print(f"\\nTukey HSD test for {prop}:")
            
            # Create pairwise comparison table
            n_groups = len(categories)
            for i in range(n_groups):
                for j in range(i+1, n_groups):
                    pvalue = tukey_result.pvalue[i, j]
                    if pvalue < 0.05:
                        print(f"  {categories[i]} vs {categories[j]}: p = {pvalue:.4f} (significant)")
        except:
            print(f"Could not perform Tukey test for {prop}")
```

## Report Generation

```python
def generate_analysis_report(epi_df, ecosar_df):
    """Generate a comprehensive analysis report."""
    
    report = {
        'dataset_summary': {
            'total_chemicals': len(epi_df),
            'chemical_categories': epi_df['category'].value_counts().to_dict(),
            'properties_analyzed': len([col for col in epi_df.columns if 'estimated' in col])
        },
        'property_statistics': {},
        'risk_assessment': {},
        'ecotoxicity_summary': {}
    }
    
    # Property statistics
    numeric_props = epi_df.select_dtypes(include=[np.number]).columns
    for prop in numeric_props:
        if 'estimated' in prop:
            report['property_statistics'][prop] = {
                'mean': float(epi_df[prop].mean()) if not pd.isna(epi_df[prop].mean()) else None,
                'std': float(epi_df[prop].std()) if not pd.isna(epi_df[prop].std()) else None,
                'min': float(epi_df[prop].min()) if not pd.isna(epi_df[prop].min()) else None,
                'max': float(epi_df[prop].max()) if not pd.isna(epi_df[prop].max()) else None,
                'missing_pct': float((epi_df[prop].isna().sum() / len(epi_df)) * 100)
            }
    
    # Risk assessment summary
    if 'bcf_category' in epi_df.columns:
        report['risk_assessment']['bioaccumulation'] = epi_df['bcf_category'].value_counts().to_dict()
    
    if 'persistence_category' in epi_df.columns:
        report['risk_assessment']['persistence'] = epi_df['persistence_category'].value_counts().to_dict()
    
    # Ecotoxicity summary
    if len(ecosar_df) > 0:
        report['ecotoxicity_summary'] = {
            'total_predictions': len(ecosar_df),
            'organisms': ecosar_df['organism'].value_counts().to_dict(),
            'endpoints': ecosar_df['endpoint'].value_counts().to_dict(),
            'concentration_stats': {
                'mean': float(ecosar_df['concentration'].mean()),
                'median': float(ecosar_df['concentration'].median()),
                'min': float(ecosar_df['concentration'].min()),
                'max': float(ecosar_df['concentration'].max())
            }
        }
    
    return report

# Generate and display report
analysis_report = generate_analysis_report(epi_df, ecosar_df)

print("=== ANALYSIS REPORT ===\\n")

print("Dataset Summary:")
for key, value in analysis_report['dataset_summary'].items():
    print(f"  {key.replace('_', ' ').title()}: {value}")

print("\\nProperty Statistics (top 5 by completeness):")
prop_stats = analysis_report['property_statistics']
complete_props = sorted(prop_stats.items(), key=lambda x: x[1]['missing_pct'])[:5]

for prop, stats in complete_props:
    print(f"  {prop}:")
    print(f"    Mean ± SD: {stats['mean']:.3f} ± {stats['std']:.3f}")
    print(f"    Range: {stats['min']:.3f} to {stats['max']:.3f}")
    print(f"    Missing: {stats['missing_pct']:.1f}%")

if 'bioaccumulation' in analysis_report['risk_assessment']:
    print("\\nBioaccumulation Risk Distribution:")
    for category, count in analysis_report['risk_assessment']['bioaccumulation'].items():
        print(f"  {category}: {count} chemicals")

if analysis_report['ecotoxicity_summary']:
    print("\\nEcotoxicity Summary:")
    eco_stats = analysis_report['ecotoxicity_summary']['concentration_stats']
    print(f"  Concentration range: {eco_stats['min']:.3f} - {eco_stats['max']:.3f} mg/L")
    print(f"  Median toxicity: {eco_stats['median']:.3f} mg/L")
```

## Exporting Results

```python
# Prepare comprehensive export
export_data = {
    'Summary': create_summary_statistics(epi_df),
    'Chemical_Properties': epi_df,
    'Ecotoxicity_Predictions': ecosar_df,
    'Risk_Classification': epi_df[['name', 'cas', 'category', 'bcf_category', 'persistence_category']],
    'Correlation_Matrix': corr_matrix,
    'PCA_Results': pca_df,
    'Cluster_Analysis': pca_data_clustered
}

# Export to Excel
from pyepisuite.dataframe_utils import export_to_excel
export_to_excel(export_data, 'comprehensive_chemical_analysis.xlsx')

print("\\nAnalysis complete! Results exported to 'comprehensive_chemical_analysis.xlsx'")
print("\\nKey findings:")
print(f"- Analyzed {len(epi_df)} chemicals across {len(epi_df['category'].unique())} categories")
print(f"- Generated {len(ecosar_df)} ecotoxicity predictions")
print(f"- Identified {len(epi_df[epi_df['bcf_category'] == 'High'])} chemicals with high bioaccumulation potential")
print(f"- Found {len(strong_corr)} strong property correlations (|r| > 0.7)")
```

This comprehensive example demonstrates how PyEPISuite can be used for sophisticated environmental data analysis, combining chemical property predictions, statistical analysis, and risk assessment in a cohesive workflow.
