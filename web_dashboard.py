import streamlit as st
import pandas as pd

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
st.markdown("<h1 style='text-align: center; color: #FF69B4;'>🛒 Interactive Amazon Products Dashboard <span style='font-size: 14px; font-style: italic; color: #888;'>by Pratikshya Priyadarshini</span></h1>", unsafe_allow_html=True)

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

# Charts using Streamlit built-in functions
col1, col2 = st.columns(2)

with col1:
    # Top Categories
    if len(filtered_df) > 0:
        st.subheader("📊 Top Categories")
        cat_counts = filtered_df['main_category'].value_counts().head(5)
        st.bar_chart(cat_counts)
    
    # Average Price by Category
    if len(filtered_df) > 0:
        st.subheader("💰 Avg Price by Category")
        cat_prices = filtered_df.groupby('main_category')['discounted_price'].mean().sort_values(ascending=False).head(5)
        st.bar_chart(cat_prices)

with col2:
    # Rating Distribution
    if len(filtered_df) > 0:
        st.subheader("⭐ Rating Distribution")
        rating_hist = filtered_df['clean_rating'].value_counts().sort_index()
        st.bar_chart(rating_hist)
    
    # Discount vs Price Scatter
    if len(filtered_df) > 0:
        st.subheader("🎯 Discount vs Price")
        chart_data = filtered_df[['discounted_price', 'discount_percentage']].dropna()
        st.scatter_chart(chart_data.set_index('discounted_price'))

# Price Range Analysis
if len(filtered_df) > 0:
    st.subheader("💸 Price Range Analysis")
    price_ranges = {
        'Under ₹500': len(filtered_df[filtered_df['discounted_price'] < 500]),
        '₹500-2000': len(filtered_df[(filtered_df['discounted_price'] >= 500) & (filtered_df['discounted_price'] < 2000)]),
        '₹2000-10000': len(filtered_df[(filtered_df['discounted_price'] >= 2000) & (filtered_df['discounted_price'] < 10000)]),
        'Above ₹10000': len(filtered_df[filtered_df['discounted_price'] >= 10000])
    }
    price_df = pd.DataFrame(list(price_ranges.items()), columns=['Range', 'Count'])
    st.bar_chart(price_df.set_index('Range'))

# Summary
st.markdown("---")
st.markdown("### 📊 Detailed Insights")

if len(filtered_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **📈 Market Segments:**
        - Budget (<₹500): **{len(filtered_df[filtered_df['discounted_price'] < 500])}** products
        - Premium (>₹10K): **{len(filtered_df[filtered_df['discounted_price'] >= 10000])}** products
        
        **💵 Price Range:**
        - Min: **₹{filtered_df['discounted_price'].min():.0f}**
        - Max: **₹{filtered_df['discounted_price'].max():,.0f}**
        - Average: **₹{filtered_df['discounted_price'].mean():.0f}**
        """)
    
    with col2:
        st.markdown(f"""
        **⭐ Quality Metrics:**
        - Average Rating: **{filtered_df['clean_rating'].mean():.1f}/5**
        - Total Categories: **{filtered_df['main_category'].nunique()}**
        - Average Discount: **{filtered_df['discount_percentage'].mean():.1f}%**
        
        **🔍 Current Filter:** **{selected_category}**
        """)
else:
    st.warning("No data available for selected filter")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #FF69B4; font-size: 18px;'>📈 Amazon Products Analytics Dashboard</p>", unsafe_allow_html=True)
