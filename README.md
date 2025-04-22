# Healthcare Search Terms Dashboard

A Python-based dashboard that visualizes the top healthcare search terms by geographical region. This interactive dashboard provides insights into healthcare trends across different parts of the world.

## Features

- Interactive region selection
- Bar chart visualization of top search terms by region
- Pie chart showing search term distribution
- Line chart displaying search trends over time
- Responsive design that works on desktop and mobile devices

## Technology Stack

- Python 3.10+
- Dash & Plotly for interactive visualization
- Pandas for data manipulation
- Tailwind CSS for styling

## Directory Structure

```
healthcare-search-dashboard/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── Dockerfile            # For containerized deployment
└── README.md            # Documentation
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/healthcare-search-dashboard.git
cd healthcare-search-dashboard
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to http://localhost:8050

## Docker Deployment

To run the dashboard using Docker:

1. Build the Docker image:
```bash
docker build -t healthcare-dashboard .
```

2. Run the container:
```bash
docker run -p 8050:8050 healthcare-dashboard
```

3. Access the dashboard at http://localhost:8050

## Data Sources

The current implementation uses mock data for demonstration purposes. In a production environment, you would connect to a real API endpoint to fetch healthcare search data.

To connect to a real data source:
1. Update the data loading logic in app.py
2. Adjust the data processing as needed

## Deployment on GitHub

1. Initialize a Git repository in your project directory:
```bash
git init
```

2. Add all files to the repository:
```bash
git add .
```

3. Commit the changes:
```bash
git commit -m "Initial commit: Healthcare Search Dashboard"
```

4. Create a new repository on GitHub through the web interface

5. Link your local repository to GitHub:
```bash
git remote add origin https://github.com/your-username/healthcare-search-dashboard.git
git branch -M main
git push -u origin main
```

## Future Enhancements

- Add filters for date ranges
- Implement data export functionality
- Add more detailed geographical breakdown (countries, states, cities)
- Include demographic information when available
- Add user authentication for accessing sensitive data

## License

This project is licensed under the MIT License - see the LICENSE file for details.
