import streamlit as st
import pandas as pd
import json
import datetime
import altair as alt  # Altair is included with Streamlit by default

# Set page configuration
st.set_page_config(
    page_title="Healthcare Search Terms Dashboard",
    layout="wide"
)

# Mock data - replace with real API calls in production
regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']

search_terms_data = {
    'North America': [
        {"term": "COVID vaccine", "count": 12500},
        {"term": "Diabetes management", "count": 8700},
        {"term": "Mental health therapy", "count": 7800},
        {"term": "Heart disease prevention", "count": 5400},
        {"term": "Telehealth services", "count": 4300}
    ],
    'Europe': [
        {"term": "COVID booster", "count": 9800},
        {"term": "Universal healthcare", "count": 7600},
        {"term": "Stress management", "count": 6500},
        {"term": "Preventive care", "count": 5100},
        {"term": "Digital health apps", "count": 4700}
    ],
    'Asia': [
        {"term": "Traditional medicine", "count": 11300},
        {"term": "Pandemic response", "count": 9200},
        {"term": "Respiratory health", "count": 7100},
        {"term": "Telemedicine platforms", "count": 6800},
        {"term": "Healthcare AI", "count": 5900}
    ],
    'South America': [
        {"term": "Dengue prevention", "count": 8900},
        {"term": "Affordable healthcare", "count": 7300},
        {"term": "Vaccination programs", "count": 6200},
        {"term": "Maternal care", "count": 5700},
        {"term": "Healthcare access", "count": 4800}
    ],
    'Africa': [
        {"term": "Malaria treatment", "count": 10200},
        {"term": "Mobile health clinics", "count": 8100},
        {"term": "HIV prevention", "count": 7400},
        {"term": "Clean water access", "count": 6100},
        {"term": "Community health workers", "count": 5300}
    ],
    'Australia': [
        {"term": "Mental wellness", "count": 7900},
        {"term": "Rural healthcare", "count": 6700},
        {"term": "Medicare benefits", "count": 5800},
        {"term": "Skin cancer screening", "count": 5200},
        {"term": "Digital health records", "count": 4600}
    ]
}

# Time series data for trends
trend_data = [
    {"month": "Jan", "COVID vaccine": 8000, "Diabetes management": 6000, "Mental health": 5000},
    {"month": "Feb", "COVID vaccine": 9200, "Diabetes management": 6100, "Mental health": 5200},
    {"month": "Mar", "COVID vaccine": 9800, "Diabetes management": 6500, "Mental health": 5800},
    {"month": "Apr", "COVID vaccine": 10500, "Diabetes management": 7100, "Mental health": 6300},
    {"month": "May", "COVID vaccine": 11200, "Diabetes management": 7800, "Mental health": 6800},
    {"month": "Jun", "COVID vaccine": 12500, "Diabetes management": 8700, "Mental health": 7800}
]

# Convert trend data to DataFrame for easier plotting with Altair
trend_df = pd.DataFrame(trend_data)

# Transform the trend data for Altair
trend_df_long = pd.melt(
    trend_df, 
    id_vars=['month'], 
    value_vars=['COVID vaccine', 'Diabetes management', 'Mental health'],
    var_name='category', 
    value_name='count'
)

# Header with title and date
st.header("Healthcare Search Terms Dashboard")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%B %d, %Y')}")

# Region selector
region = st.selectbox("Select Region", regions)

# Create columns for layout
col1, col2 = st.columns(2)

# Get data for the selected region
region_data = search_terms_data[region]
region_df = pd.DataFrame(region_data)

# Top search terms bar chart using native Streamlit chart
with col1:
    st.subheader(f"Top Healthcare Search Terms in {region}")
    
    # Create horizontal bar chart with Altair
    bar_chart = alt.Chart(region_df).mark_bar().encode(
        y=alt.Y('term:N', sort='-x', title=None),
        x=alt.X('count:Q', title='Search Count'),
        color=alt.Color('term:N', legend=None)
    ).properties(height=400)
    
    st.altair_chart(bar_chart, use_container_width=True)

# Distribution pie chart using native Streamlit chart
with col2:
    st.subheader(f"Search Distribution in {region}")
    
    # Streamlit's native pie chart
    st.dataframe(
        region_df,
        column_config={
            "term": "Search Term",
            "count": st.column_config.ProgressColumn(
                "Search Distribution",
                format="%d",
                min_value=0,
                max_value=region_df["count"].max()
            ),
        },
        hide_index=True,
    )
    
    # Simple bar chart as alternative to pie
    chart = alt.Chart(region_df).mark_arc().encode(
        theta=alt.Theta('count:Q'),
        color=alt.Color('term:N')
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

# Search trends over time using native Streamlit chart
st.subheader("Search Trends Over Time (Top 3 Terms)")

# Create line chart with Altair
line_chart = alt.Chart(trend_df_long).mark_line(point=True).encode(
    x=alt.X('month:N', title='Month'),
    y=alt.Y('count:Q', title='Search Count'),
    color=alt.Color('category:N', title='Search Term'),
    tooltip=['month', 'category', 'count']
).properties(height=400)

st.altair_chart(line_chart, use_container_width=True)

# Add footer
st.markdown("---")
st.caption("© 2025 Healthcare Search Trends Dashboard. Data is for demonstration purposes only.")

# Export data functionality
if st.button("Export Data"):
    # Create a function to convert data to downloadable format
    def convert_df_to_csv(df):
        return df.to_csv().encode('utf-8')
    
    # Create downloadable CSVs
    region_csv = convert_df_to_csv(region_df)
    trend_csv = convert_df_to_csv(trend_df)
    
    # Add download buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Region Data",
            data=region_csv,
            file_name=f'healthcare_search_terms_{region}.csv',
            mime='text/csv',
        )
    with col2:
        st.download_button(
            label="Download Trend Data",
            data=trend_csv,
            file_name='healthcare_trends.csv',
            mime='text/csv',
        )
