# Healthcare Search Terms Dashboard

A React-based dashboard that visualizes the top healthcare search terms by geographical region. This interactive dashboard provides insights into healthcare trends across different parts of the world.

## Features

- Interactive region selection
- Bar chart visualization of top search terms by region
- Pie chart showing search term distribution
- Line chart displaying search trends over time
- Responsive design that works on desktop and mobile devices

## Screenshots

![Dashboard Preview](/screenshot.png)

## Technology Stack

- React.js
- Recharts for data visualization
- Tailwind CSS for styling
- Lucide React for icons

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/healthcare-search-dashboard.git
cd healthcare-search-dashboard
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm start
# or
yarn start
```

4. Open your browser and navigate to http://localhost:3000

## Data Sources

The current implementation uses mock data for demonstration purposes. In a production environment, you would connect to a real API endpoint to fetch healthcare search data.

To connect to a real data source:
1. Update the API endpoints in the useEffect hooks
2. Adjust the data processing logic if needed

## Deployment

To build the app for production:

```bash
npm run build
# or
yarn build
```

This will create an optimized build in the `build` folder that can be deployed to any static hosting service.

## Future Enhancements

- Add filters for date ranges
- Implement data export functionality
- Add more detailed geographical breakdown (countries, states, cities)
- Include demographic information when available
- Add user authentication for accessing sensitive data

## License

This project is licensed under the MIT License - see the LICENSE file for details.
