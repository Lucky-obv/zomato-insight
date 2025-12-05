import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Zomato | Top 10 Restaurants by Rating & Approx Cost")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Columns that MIGHT exist
cols_to_drop = [
    'url','online_order','book_table','phone','rest_type','dish_liked',
    'menu_item','reviews_list','listed_in(type)','listed_in(city)','address'
]

# Drop only if present
existing_cols = [c for c in cols_to_drop if c in df.columns]
df = df.drop(existing_cols, axis=1)

# Rename cost column safely
if 'approx_cost(for two people)' in df.columns:
    df = df.rename(columns={'approx_cost(for two people)': 'approx_cost'})

# Fill NA
df = df.fillna(0)

# Clean approx_cost
if 'approx_cost' in df.columns:
    df['approx_cost'] = df['approx_cost'].astype(str).replace('[,]', '', regex=True)
    df['approx_cost'] = pd.to_numeric(df['approx_cost'], errors='coerce').fillna(0).astype(int)

# Clean rate column
if 'rate' in df.columns:
    df['rate'] = df['rate'].astype(str)
    df['rate'] = df['rate'].str.replace('NEW', '0')
    df['rate'] = df['rate'].str.replace('-', '0')
    df['rate'] = df['rate'].str.replace('[/5]', '', regex=True)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0)

# -------------------------------
# Streamlit interactive input
# -------------------------------
st.write("### Select a Location")

locations = sorted(df['location'].unique())
selected_location = st.selectbox("Choose location", locations)

# Filter data
lo = df[df['location'] == selected_location]

# Group & top 10
gr = (
    lo.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

# -------------------------------
# Plot
# -------------------------------
st.write("### Top 10 Restaurants by Rating (Showing Approx Cost)")

if not gr.empty:
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.barplot(x=gr['name'], y=gr['approx_cost'], palette='summer', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)
else:
    st.error("No restaurants found for this location.")
