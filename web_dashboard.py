import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Amazon Products Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('amazon.csv')
    df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
    df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
    df['discount_percentage'] = df['discount_percentage'].str.replace('%', '').astype(float)
    df['main_category'] = df['category'].str.split('|').str[0]
    df['clean_rating'] = pd.to_numeric(df['rating'].astype(str).str[:3], errors='coerce')
    return df

df = load_data()

# Title
st.markdown("<h1 style='text-align: center; color: #FF69B4;'>🛒 Interactive Amazon Products Dashboard</h1>", unsafe_allow_html=True)

# Category Filter
categories = ['All Categories'] + list(df['main_category'].unique())
selected_category = st.selectbox("🔽 Filter by Category:", categories)

# Filter data
if selected_category == 'All Categories':
    filtered_df = df
else:
    filtered_df = df[df['main_category'] == selected_category]

# Key Insights Boxes
col1, col2, col3 = st.columns(3)

with col1:
    top_category = filtered_df['main_category'].value_counts().index[0] if len(filtered_df) > 0 else 'N/A'
    st.markdown(f"""
    <div style='background-color: white; padding: 20px; border-radius: 10px; border: 2px solid #FF69B4; text-align: center;'>
        <h3 style='color: #FF69B4; margin: 0;'>Top Category</h3>
        <h2 style='color: #333; margin: 5px 0;'>{top_category}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_products = len(filtered_df)
    st.markdown(f"""
    <div style='background-color: white; padding: 20px; border-radius: 10px; border: 2px solid #FF69B4; text-align: center;'>
        <h3 style='color: #FF69B4; margin: 0;'>Total Products</h3>
        <h2 style='color: #333; margin: 5px 0;'>{total_products:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_rating = filtered_df['clean_rating'].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div style='background-color: white; padding: 20px; border-radius: 10px; border: 2px solid #FF69B4; text-align: center;'>
        <h3 style='color: #FF69B4; margin: 0;'>Avg Rating</h3>
        <h2 style='color: #333; margin: 5px 0;'>{avg_rating:.1f}/5</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts using matplotlib
col1, col2 = st.columns(2)

with col1:
    # Top Categories
    if len(filtered_df) > 0:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        cat_counts = filtered_df['main_category'].value_counts().head(5)
        ax1.bar(range(len(cat_counts)), cat_counts.values, color='hotpink')
        ax1.set_title('Top Categories', fontsize=16, fontweight='bold')
        ax1.set_xticks(range(len(cat_counts)))
        ax1.set_xticklabels(cat_counts.index, rotation=45, ha='right')
        ax1.set_ylabel('Count')
        plt.tight_layout()
        st.pyplot(fig1)
    
    # Average Price by Category
    if len(filtered_df) > 0:
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        cat_prices = filtered_df.groupby('main_category')['discounted_price'].mean().sort_values(ascending=False).head(5)
        ax3.bar(range(len(cat_prices)), cat_prices.values, color='lightpink')
        ax3.set_title('Avg Price by Category', fontsize=16, fontweight='bold')
        ax3.set_xticks(range(len(cat_prices)))
        ax3.set_xticklabels(cat_prices.index, rotation=45, ha='right')
        ax3.set_ylabel('Avg Price (₹)')
        plt.tight_layout()
        st.pyplot(fig3)

with col2:
    # Rating Distribution
    if len(filtered_df) > 0:
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        ax2.hist(filtered_df['clean_rating'].dropna(), bins=20, color='deeppink', alpha=0.7)
        ax2.set_title('Rating Distribution', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Rating')
        ax2.set_ylabel('Count')
        plt.tight_layout()
        st.pyplot(fig2)
    
    # Price Range Distribution
    if len(filtered_df) > 0:
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        price_ranges = ['<₹500', '₹500-2K', '₹2K-10K', '>₹10K']
        counts = [
            len(filtered_df[filtered_df['discounted_price'] < 500]),
            len(filtered_df[(filtered_df['discounted_price'] >= 500) & (filtered_df['discounted_price'] < 2000)]),
            len(filtered_df[(filtered_df['discounted_price'] >= 2000) & (filtered_df['discounted_price'] < 10000)]),
            len(filtered_df[filtered_df['discounted_price'] >= 10000])
        ]
        colors = ['pink', 'hotpink', 'deeppink', 'mediumvioletred']
        ax4.pie(counts, labels=price_ranges, autopct='%1.1f%%', colors=colors)
        ax4.set_title('Price Range Distribution', fontsize=16, fontweight='bold')
        st.pyplot(fig4)

# Discount vs Price Scatter Plot
if len(filtered_df) > 0:
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    ax5.scatter(filtered_df['discounted_price'], filtered_df['discount_percentage'], alpha=0.6, color='mediumvioletred')
    ax5.set_title('Discount vs Price', fontsize=16, fontweight='bold')
    ax5.set_xlabel('Price (₹)')
    ax5.set_ylabel('Discount %')
    plt.tight_layout()
    st.pyplot(fig5)

# Summary
st.markdown("### 📊 Detailed Insights")
if len(filtered_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Market Segments:**
        - Budget (<₹500): {len(filtered_df[filtered_df['discounted_price'] < 500])} products
        - Premium (>₹10K): {len(filtered_df[filtered_df['discounted_price'] >= 10000])} products
        
        **Price Range:**
        - Min: ₹{filtered_df['discounted_price'].min():.0f}
        - Max: ₹{filtered_df['discounted_price'].max():,.0f}
        """)
    
    with col2:
        st.markdown(f"""
        **Quality Score:**
        - Average Rating: {filtered_df['clean_rating'].mean():.1f}/5
        - Categories: {filtered_df['main_category'].nunique()} total
        
        **Current Filter:** {selected_category}
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #FF69B4;'>📈 Amazon Products Analytics Dashboard</p>", unsafe_allow_html=True)
