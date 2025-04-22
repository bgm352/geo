# Healthcare Search Terms Dashboard

A simple Python-based dashboard that visualizes the top healthcare search terms by geographical region. This dashboard provides insights into healthcare trends across different parts of the world without requiring any external Python packages.

## Features

- Interactive region selection
- Bar chart visualization of top search terms by region
- Pie chart showing search term distribution
- Line chart displaying search trends over time
- Pure Python implementation with no external dependencies

## Directory Structure

```
healthcare-search-dashboard/
├── app.py                # Main application file
└── README.md             # Documentation
```

## Getting Started

### Prerequisites

- Python 3.6 or later (standard library only)

### Usage

1. Clone the repository:
```bash
git clone https://github.com/your-username/healthcare-search-dashboard.git
cd healthcare-search-dashboard
```

2. Run the application:

To export the data as JSON files:
```bash
python app.py
```

To start the HTTP server:
```bash
python app.py --serve
```

3. If running the server, open your browser and navigate to http://localhost:8000

## Data Structure

The dashboard uses mock data stored in the following format:

- **regions**: List of geographical regions
- **search_terms_data**: Dictionary mapping regions to lists of search terms with their counts
- **trend_data**: List of dictionaries containing monthly trend data for top search terms

### Adding Real Data

To integrate with real data:
1. Modify the data structures in app.py
2. Or implement an API integration function that pulls data from your source

## GitHub Integration

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

4. Create a new repository on GitHub and follow the instructions to push your code:
```bash
git remote add origin https://github.com/your-username/healthcare-search-dashboard.git
git branch -M main
git push -u origin main
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
