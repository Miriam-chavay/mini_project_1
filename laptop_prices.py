import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore


# import dataset
df = pd.read_csv(r"C:\Users\miric\OneDrive\Documents\notebooks OneNote\year 2 semester A\python\mini_project_1\laptop_price_dataset.csv")


# plot the prices of all laptops
fig = px.box(df, x="Company", y="Price (Euro)")
fig.update_layout(
  title="Distribution of laptop prices",
  xaxis_title="Company",
  yaxis_title="Price (Euro)",
  width=1100,
  height=700,
)
fig.show()


# average prices, from the most expensive to cheapest
avg_prices = df.groupby('Company')['Price (Euro)'].mean().sort_values(ascending=False)

print(avg_prices)


# Merging same operating systems by string comparisons
def clean_opsys(os):
    os = os.lower()
    if 'windows' in os:
        return 'Windows'
    if 'mac' in os:
        return 'Mac'
    if 'no os' in os:
        return 'No OS'
    if 'linux' in os:
        return 'Linux'
    if 'chrome' in os:
        return 'Chrome'
    if 'android' in os:
        return 'Android'
    else:
        return 'other'

# Use cleaning function
df['OpSys_Clean'] = df['OpSys'].apply(clean_opsys)

# printing the different operating systems after cleaning the values
print(df.OpSys_Clean.value_counts())


fig = px.box(
    df,
    y="Price (Euro)",
    facet_col="OpSys_Clean",
    points="all",
    color="OpSys_Clean"
)

fig.update_layout(
    title="Distribution of Laptop Prices by Operating System",
    yaxis_title="Price (Euro)",
    showlegend=False,
    width=1200,
    height=700
)

fig.show()


def ram_price(data):

    # Sort RAM values so they appear in the correct order on the x-axis
    ram_levels = sorted(data['RAM (GB)'].unique())

    # Calculate Spearman correlation
    corr_value = data['RAM (GB)'].corr(data['Price (Euro)'], method='spearman')
    print(f"Spearman correlation (RAM vs Price): {corr_value:.3f}")

    # Box Plot: RAM vs Price
    plt.figure(figsize=(11, 5))

    sns.boxplot(
        x='RAM (GB)',
        y='Price (Euro)',
        data=data,
        order=ram_levels,
        color='skyblue'
    )

    plt.title('The relationship between RAM and computer price')
    plt.xlabel('RAM (GB)')
    plt.ylabel('Price (Euro)')
    plt.tight_layout()
    plt.show()

    # Z-score detection of outliers
    # Create a copy of the data to avoid changing the original DataFrame
    temp_df = data.copy()
    temp_df['price_z'] = zscore(temp_df['Price (Euro)'])

    # Define outliers by |Z-score| > 3
    price_outliers = temp_df[temp_df['price_z'].abs() > 3]

    print("\nOutliers detected using Z-score:")
    print(
        price_outliers[['RAM (GB)', 'Price (Euro)', 'price_z']]
        .sort_values(by='Price (Euro)', ascending=False)
    )


def extract_storage_type(memory):
    memory = memory.upper()
    if 'SSD' in memory and 'HDD' in memory:
        return 'SSD + HDD'
    elif 'SSD' in memory:
        return 'SSD'
    elif 'HDD' in memory:
        return 'HDD'
    elif 'FLASH' in memory:
        return 'Flash Storage'
    else:
        return 'Other'

df["Storage type"] = df["Memory"].apply(extract_storage_type)

df








