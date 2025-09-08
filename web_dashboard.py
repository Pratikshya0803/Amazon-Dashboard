import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Amazon Products Dashboard", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_data():
    df = pd.read_csv('amazon.csv')  # Fixed path for Streamlit Cloud
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
selected_category = st.selectbox("🔽 Filter by Category:", categories, key="category_filter")

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

# Charts
col1, col2 = st.columns(2)

with col1:
    # Top Categories
    if len(filtered_df) > 0:
        cat_counts = filtered_df['main_category'].value_counts().head(5)
        fig1 = px.bar(x=cat_counts.index, y=cat_counts.values, 
                     title="Top Categories", color_discrete_sequence=['#FF69B4'])
        fig1.update_layout(xaxis_title="Category", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)
    
    # Average Price by Category
    if len(filtered_df) > 0:
        cat_prices = filtered_df.groupby('main_category')['discounted_price'].mean().sort_values(ascending=False).head(5)
        fig3 = px.bar(x=cat_prices.index, y=cat_prices.values,
                     title="Avg Price by Category", color_discrete_sequence=['#FFB6C1'])
        fig3.update_layout(xaxis_title="Category", yaxis_title="Avg Price (₹)")
        st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Rating Distribution
    if len(filtered_df) > 0:
        fig2 = px.histogram(filtered_df, x='clean_rating', nbins=20,
                           title="Rating Distribution", color_discrete_sequence=['#FF1493'])
        fig2.update_layout(xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Price Range Distribution
    if len(filtered_df) > 0:
        price_ranges = ['<₹500', '₹500-2K', '₹2K-10K', '>₹10K']
        counts = [
            len(filtered_df[filtered_df['discounted_price'] < 500]),
            len(filtered_df[(filtered_df['discounted_price'] >= 500) & (filtered_df['discounted_price'] < 2000)]),
            len(filtered_df[(filtered_df['discounted_price'] >= 2000) & (filtered_df['discounted_price'] < 10000)]),
            len(filtered_df[filtered_df['discounted_price'] >= 10000])
        ]
        fig4 = px.pie(values=counts, names=price_ranges, title="Price Range Distribution",
                     color_discrete_sequence=['#FFC0CB', '#FF69B4', '#FF1493', '#C71585'])
        st.plotly_chart(fig4, use_container_width=True)

# Discount vs Price Scatter Plot
if len(filtered_df) > 0:
    fig5 = px.scatter(filtered_df, x='discounted_price', y='discount_percentage',
                     title="Discount vs Price", color_discrete_sequence=['#DB7093'])
    fig5.update_layout(xaxis_title="Price (₹)", yaxis_title="Discount %")
    st.plotly_chart(fig5, use_container_width=True)

# Summary Box
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
else:
    st.warning("No data available for selected filter")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #FF69B4;'>📈 Amazon Products Analytics Dashboard</p>", unsafe_allow_html=True)
