// src/App.jsx
import React, { useState, useEffect } from 'react';
import { LineChart, BarChart, PieChart, Area, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Pie } from 'recharts';
import { Globe } from 'lucide-react';
import './App.css';

// Mock data - replace with real API calls in production
const mockRegions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia'];

const mockData = {
  'North America': [
    { term: 'COVID vaccine', count: 12500 },
    { term: 'Diabetes management', count: 8700 },
    { term: 'Mental health therapy', count: 7800 },
    { term: 'Heart disease prevention', count: 5400 },
    { term: 'Telehealth services', count: 4300 }
  ],
  'Europe': [
    { term: 'COVID booster', count: 9800 },
    { term: 'Universal healthcare', count: 7600 },
    { term: 'Stress management', count: 6500 },
    { term: 'Preventive care', count: 5100 },
    { term: 'Digital health apps', count: 4700 }
  ],
  'Asia': [
    { term: 'Traditional medicine', count: 11300 },
    { term: 'Pandemic response', count: 9200 },
    { term: 'Respiratory health', count: 7100 },
    { term: 'Telemedicine platforms', count: 6800 },
    { term: 'Healthcare AI', count: 5900 }
  ],
  'South America': [
    { term: 'Dengue prevention', count: 8900 },
    { term: 'Affordable healthcare', count: 7300 },
    { term: 'Vaccination programs', count: 6200 },
    { term: 'Maternal care', count: 5700 },
    { term: 'Healthcare access', count: 4800 }
  ],
  'Africa': [
    { term: 'Malaria treatment', count: 10200 },
    { term: 'Mobile health clinics', count: 8100 },
    { term: 'HIV prevention', count: 7400 },
    { term: 'Clean water access', count: 6100 },
    { term: 'Community health workers', count: 5300 }
  ],
  'Australia': [
    { term: 'Mental wellness', count: 7900 },
    { term: 'Rural healthcare', count: 6700 },
    { term: 'Medicare benefits', count: 5800 },
    { term: 'Skin cancer screening', count: 5200 },
    { term: 'Digital health records', count: 4600 }
  ]
};

// Time series data for trends
const trendData = [
  { month: 'Jan', 'COVID vaccine': 8000, 'Diabetes management': 6000, 'Mental health': 5000 },
  { month: 'Feb', 'COVID vaccine': 9200, 'Diabetes management': 6100, 'Mental health': 5200 },
  { month: 'Mar', 'COVID vaccine': 9800, 'Diabetes management': 6500, 'Mental health': 5800 },
  { month: 'Apr', 'COVID vaccine': 10500, 'Diabetes management': 7100, 'Mental health': 6300 },
  { month: 'May', 'COVID vaccine': 11200, 'Diabetes management': 7800, 'Mental health': 6800 },
  { month: 'Jun', 'COVID vaccine': 12500, 'Diabetes management': 8700, 'Mental health': 7800 },
];

// COLORS
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A259FF'];

function App() {
  const [selectedRegion, setSelectedRegion] = useState('North America');
  const [searchTerms, setSearchTerms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setSearchTerms(mockData[selectedRegion]);
      setLoading(false);
    }, 500);
  }, [selectedRegion]);

  const handleRegionChange = (region) => {
    setLoading(true);
    setSelectedRegion(region);
  };

  // Calculate total searches for pie chart
  const totalSearches = searchTerms.reduce((sum, item) => sum + item.count, 0);

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-blue-600 text-white shadow-md p-4">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <Globe className="mr-2" size={24} />
            <h1 className="text-2xl font-bold">Healthcare Search Trends Dashboard</h1>
          </div>
          <div>
            <p className="text-sm opacity-80">Last updated: April 22, 2025</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto p-4">
        {/* Region selector */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <h2 className="text-lg font-semibold mb-3">Select Region</h2>
          <div className="flex flex-wrap gap-2">
            {mockRegions.map((region) => (
              <button
                key={region}
                onClick={() => handleRegionChange(region)}
                className={`px-4 py-2 rounded-full ${
                  selectedRegion === region
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 hover:bg-gray-300'
                }`}
              >
                {region}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <p className="text-xl">Loading data...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top search terms */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <h2 className="text-lg font-semibold mb-4">Top Healthcare Search Terms in {selectedRegion}</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={searchTerms} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="term" type="category" width={100} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" name="Search Count" fill="#0088FE" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Distribution pie chart */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <h2 className="text-lg font-semibold mb-4">Search Distribution in {selectedRegion}</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={searchTerms}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="count"
                    nameKey="term"
                    label={({term, count}) => `${term}: ${Math.round((count/totalSearches)*100)}%`}
                  >
                    {searchTerms.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value} searches (${Math.round((value/totalSearches)*100)}%)`} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Search trends over time */}
            <div className="bg-white rounded-lg shadow-md p-4 lg:col-span-2">
              <h2 className="text-lg font-semibold mb-4">Search Trends Over Time (Top 3 Terms)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trendData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <LineChart.Line type="monotone" dataKey="COVID vaccine" stroke="#0088FE" activeDot={{ r: 8 }} />
                  <LineChart.Line type="monotone" dataKey="Diabetes management" stroke="#00C49F" />
                  <LineChart.Line type="monotone" dataKey="Mental health" stroke="#FFBB28" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto text-center">
          <p>2025 Healthcare Search Trends Dashboard. Data is for demonstration purposes only.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
