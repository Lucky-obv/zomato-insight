import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Zomato | Top 10 Restaurants by Rating & Approx Cost")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Clean data (same as your code)
df = df.drop(['url','online_order','book_table','phone','rest_type','dish_liked',
              'menu_item','reviews_list','listed_in(type)','listed_in(city)','address'], axis=1)

df = df.rename(columns={'approx_cost(for two people)': 'approx_cost'})
df = df.fillna(0)

df['approx_cost'] = df['approx_cost'].astype(str).replace('[,]', '', regex=True).astype('int64')
df['rate'] = df['rate'].astype(str).replace('NEW', '0').replace('-', '0')
df['rate'] = df['rate'].replace('[/5]', '', regex=True).astype(float)

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
fig, ax = plt.subplots(figsize=(20, 8))
sns.barplot(x=gr['name'], y=gr['approx_cost'], palette='summer', ax=ax)
plt.xticks(rotation=90)

st.pyplot(fig)
