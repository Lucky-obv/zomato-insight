import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Zomato Data Dashboard", 
                   layout="wide",
                   page_icon="🍽️")

st.title("🍽️ Zomato Data Interactive Dashboard")
st.write("Explore restaurant ratings, cost, and insights using an interactive interface.")

# -------------------------------
# Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Live.csv")
    df = df.drop(['url','online_order','book_table','phone','rest_type','dish_liked',
                  'menu_item','reviews_list','listed_in(type)','listed_in(city)','address'], axis=1)
    df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
    
    df = df.fillna(0)
    df['approx_cost'] = df['approx_cost'].replace('[,]', '', regex=True).astype('int64')
    
    df['rate'] = df['rate'].replace('NEW', 0)
    df['rate'] = df['rate'].replace('-', 0)
    df['rate'] = df['rate'].replace('[/5]', '', regex=True)
    df['rate'] = df['rate'].astype('float64')

    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Options")

locations = sorted(df['location'].unique())
selected_location = st.sidebar.selectbox("Choose a Location", locations)

filtered_df = df[df['location'] == selected_location]

st.subheader(f"📍 Showing results for: **{selected_location}**")
st.write(filtered_df.head())

# -------------------------------
# Top 10 Restaurants by Rating
# -------------------------------
st.markdown("### ⭐ Top 10 Restaurants by Rating")

top10 = (
    filtered_df.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig1 = plt.figure(figsize=(10, 5))
    sns.barplot(data=top10, x='name', y='rate', palette='viridis')
    plt.xticks(rotation=90)
    plt.title("Top 10 Restaurants (Rating)")
    plt.ylabel("Average Rating")
    st.pyplot(fig1)

with col2:
    fig2 = plt.figure(figsize=(10, 5))
    sns.barplot(data=top10, x='name', y='approx_cost', palette='magma')
    plt.xticks(rotation=90)
    plt.title("Top 10 Restaurants (Approx Cost)")
    plt.ylabel("Average Cost for Two")
    st.pyplot(fig2)

# -------------------------------
# Distribution Charts
# -------------------------------
st.markdown("### 📊 Distribution Insights")

col3, col4 = st.columns(2)

with col3:
    fig3 = plt.figure(figsize=(8, 5))
    sns.histplot(filtered_df['rate'], kde=True, color='green')
    plt.title("Rating Distribution")
    st.pyplot(fig3)

with col4:
    fig4 = plt.figure(figsize=(8, 5))
    sns.histplot(filtered_df['approx_cost'], kde=True, color='purple')
    plt.title("Cost Distribution")
    st.pyplot(fig4)

# -------------------------------
# Heatmap
# -------------------------------
st.markdown("### 🔥 Cost vs Rating Heatmap")

fig5 = plt.figure(figsize=(8, 6))
sns.heatmap(filtered_df[['rate', 'approx_cost']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
st.pyplot(fig5)

# -------------------------------
# End
# -------------------------------
st.success("Dashboard Loaded Successfully 🎉")
