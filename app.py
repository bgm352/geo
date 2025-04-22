# /mount/src/geo/app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css'])
server = app.server

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
trend_data = pd.DataFrame([
    {"month": "Jan", "COVID vaccine": 8000, "Diabetes management": 6000, "Mental health": 5000},
    {"month": "Feb", "COVID vaccine": 9200, "Diabetes management": 6100, "Mental health": 5200},
    {"month": "Mar", "COVID vaccine": 9800, "Diabetes management": 6500, "Mental health": 5800},
    {"month": "Apr", "COVID vaccine": 10500, "Diabetes management": 7100, "Mental health": 6300},
    {"month": "May", "COVID vaccine": 11200, "Diabetes management": 7800, "Mental health": 6800},
    {"month": "Jun", "COVID vaccine": 12500, "Diabetes management": 8700, "Mental health": 7800}
])

# Colors
colors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A259FF']

# App layout
app.layout = html.Div(
    className="bg-gray-100 min-h-screen",
    children=[
        # Header
        html.Header(
            className="bg-blue-600 text-white shadow-md p-4",
            children=[
                html.Div(
                    className="container mx-auto flex items-center justify-between",
                    children=[
                        html.Div(
                            className="flex items-center",
                            children=[
                                html.H1("Healthcare Search Trends Dashboard", className="text-2xl font-bold")
                            ]
                        ),
                        html.Div(
                            children=[
                                html.P(f"Last updated: {datetime.now().strftime('%B %d, %Y')}", className="text-sm opacity-80")
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # Main content
        html.Main(
            className="container mx-auto p-4",
            children=[
                # Region selector
                html.Div(
                    className="bg-white rounded-lg shadow-md p-4 mb-6",
                    children=[
                        html.H2("Select Region", className="text-lg font-semibold mb-3"),
                        dcc.RadioItems(
                            id='region-selector',
                            options=[{'label': region, 'value': region} for region in regions],
                            value='North America',
                            className="flex flex-wrap gap-2",
                            labelClassName="px-4 py-2 rounded-full bg-gray-200 hover:bg-gray-300 cursor-pointer",
                            inputClassName="hidden"
                        )
                    ]
                ),
                
                # Dashboard grid
                html.Div(
                    className="grid grid-cols-1 lg:grid-cols-2 gap-6",
                    children=[
                        # Top search terms bar chart
                        html.Div(
                            className="bg-white rounded-lg shadow-md p-4",
                            children=[
                                html.H2(id="bar-chart-title", className="text-lg font-semibold mb-4"),
                                dcc.Graph(id='bar-chart')
                            ]
                        ),
                        
                        # Distribution pie chart
                        html.Div(
                            className="bg-white rounded-lg shadow-md p-4",
                            children=[
                                html.H2(id="pie-chart-title", className="text-lg font-semibold mb-4"),
                                dcc.Graph(id='pie-chart')
                            ]
                        ),
                        
                        # Search trends over time
                        html.Div(
                            className="bg-white rounded-lg shadow-md p-4 lg:col-span-2",
                            children=[
                                html.H2("Search Trends Over Time (Top 3 Terms)", className="text-lg font-semibold mb-4"),
                                dcc.Graph(id='line-chart')
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # Footer
        html.Footer(
            className="bg-gray-800 text-white p-4 mt-8",
            children=[
                html.Div(
                    className="container mx-auto text-center",
                    children=[
                        html.P("© 2025 Healthcare Search Trends Dashboard. Data is for demonstration purposes only.")
                    ]
                )
            ]
        )
    ]
)

# Callbacks for interactivity
@app.callback(
    [
        Output('bar-chart-title', 'children'),
        Output('bar-chart', 'figure'),
        Output('pie-chart-title', 'children'),
        Output('pie-chart', 'figure'),
        Output('line-chart', 'figure')
    ],
    [Input('region-selector', 'value')]
)
def update_charts(selected_region):
    # Convert region data to DataFrame
    df = pd.DataFrame(search_terms_data[selected_region])
    
    # Create bar chart
    bar_fig = px.bar(
        df, 
        y='term', 
        x='count',
        orientation='h',
        title=f"Top Healthcare Search Terms in {selected_region}",
        labels={'count': 'Search Count', 'term': 'Search Term'},
        color_discrete_sequence=colors
    )
    
    # Create pie chart
    pie_fig = px.pie(
        df, 
        values='count', 
        names='term',
        title=f"Search Distribution in {selected_region}",
        color_discrete_sequence=colors
    )
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Create line chart
    line_fig = px.line(
        trend_data, 
        x='month', 
        y=['COVID vaccine', 'Diabetes management', 'Mental health'],
        title="Search Trends Over Time (Top 3 Terms)",
        labels={'value': 'Search Count', 'variable': 'Search Term'},
        color_discrete_sequence=colors
    )
    
    bar_title = f"Top Healthcare Search Terms in {selected_region}"
    pie_title = f"Search Distribution in {selected_region}"
    
    return bar_title, bar_fig, pie_title, pie_fig, line_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
