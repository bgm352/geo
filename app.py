import streamlit as st
import pandas as pd
import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="USA Physicians Directory Dashboard",
    layout="wide"
)

# USA regions with specific cities
usa_regions = {
    'Northeast': ['Boston', 'New York City', 'Philadelphia', 'Hartford'],
    'Southeast': ['Miami', 'Atlanta', 'Charlotte', 'Nashville'],
    'Midwest': ['Chicago', 'Detroit', 'Minneapolis', 'Cleveland'],
    'Southwest': ['Houston', 'Dallas', 'Phoenix', 'San Antonio'],
    'West Coast': ['Los Angeles', 'San Francisco', 'Seattle', 'Portland']
}

# Mock data for individual doctors with specific roles and hospital addresses
doctors_data = {
    'Boston': [
        {
            "name": "Dr. Elizabeth Chen", 
            "role": "Chief of Cardiology",
            "specialty": "Interventional Cardiology",
            "hospital": "Massachusetts General Hospital",
            "address": "55 Fruit Street, Boston, MA 02114",
            "search_count": 2350,
            "patient_rating": 4.8
        },
        {
            "name": "Dr. James Wilson", 
            "role": "Director of Oncology",
            "specialty": "Hematologic Oncology",
            "hospital": "Dana-Farber Cancer Institute",
            "address": "450 Brookline Avenue, Boston, MA 02215",
            "search_count": 1980,
            "patient_rating": 4.7
        },
        {
            "name": "Dr. Sarah Johnson", 
            "role": "Pediatric Surgeon",
            "specialty": "Pediatric Cardiothoracic Surgery",
            "hospital": "Boston Children's Hospital",
            "address": "300 Longwood Avenue, Boston, MA 02115",
            "search_count": 1750,
            "patient_rating": 4.9
        },
        {
            "name": "Dr. Michael Rodriguez", 
            "role": "Neurosurgery Department Head",
            "specialty": "Spine and Brain Surgery",
            "hospital": "Brigham and Women's Hospital",
            "address": "75 Francis Street, Boston, MA 02115",
            "search_count": 1680,
            "patient_rating": 4.6
        },
        {
            "name": "Dr. Rebecca Liu", 
            "role": "Chief of Endocrinology",
            "specialty": "Diabetes Management",
            "hospital": "Tufts Medical Center",
            "address": "800 Washington Street, Boston, MA 02111",
            "search_count": 1420,
            "patient_rating": 4.5
        }
    ],
    'New York City': [
        {
            "name": "Dr. David Goldstein", 
            "role": "Cardiothoracic Surgeon",
            "specialty": "Minimally Invasive Heart Surgery",
            "hospital": "New York-Presbyterian Hospital",
            "address": "525 East 68th Street, New York, NY 10065",
            "search_count": 2560,
            "patient_rating": 4.9
        },
        {
            "name": "Dr. Maria Sanchez", 
            "role": "Director of Neurology",
            "specialty": "Movement Disorders",
            "hospital": "NYU Langone Medical Center",
            "address": "550 First Avenue, New York, NY 10016",
            "search_count": 2240,
            "patient_rating": 4.7
        },
        {
            "name": "Dr. Robert Chang", 
            "role": "Chief Surgical Oncologist",
            "specialty": "Gastrointestinal Cancer",
            "hospital": "Memorial Sloan Kettering Cancer Center",
            "address": "1275 York Avenue, New York, NY 10065",
            "search_count": 2190,
            "patient_rating": 4.8
        },
        {
            "name": "Dr. Jennifer Williams", 
            "role": "Pediatric Neurologist",
            "specialty": "Pediatric Epilepsy",
            "hospital": "Mount Sinai Hospital",
            "address": "1 Gustave L. Levy Place, New York, NY 10029",
            "search_count": 1870,
            "patient_rating": 4.6
        },
        {
            "name": "Dr. Thomas Jackson", 
            "role": "Head of Orthopedic Surgery",
            "specialty": "Sports Medicine",
            "hospital": "Hospital for Special Surgery",
            "address": "535 East 70th Street, New York, NY 10021",
            "search_count": 1730,
            "patient_rating": 4.8
        }
    ],
    'Chicago': [
        {
            "name": "Dr. Amanda Patel", 
            "role": "Chief of Transplant Surgery",
            "specialty": "Liver and Kidney Transplantation",
            "hospital": "Northwestern Memorial Hospital",
            "address": "251 E Huron Street, Chicago, IL 60611",
            "search_count": 2310,
            "patient_rating": 4.9
        },
        {
            "name": "Dr. Richard Brown", 
            "role": "Director of Cardiology",
            "specialty": "Preventive Cardiology",
            "hospital": "University of Chicago Medical Center",
            "address": "5841 S Maryland Avenue, Chicago, IL 60637",
            "search_count": 2150,
            "patient_rating": 4.7
        },
        {
            "name": "Dr. Lisa Martinez", 
            "role": "Chief of Pediatric Oncology",
            "specialty": "Childhood Leukemia",
            "hospital": "Ann & Robert H. Lurie Children's Hospital",
            "address": "225 E Chicago Avenue, Chicago, IL 60611",
            "search_count": 1950,
            "patient_rating": 4.8
        },
        {
            "name": "Dr. Kevin Park", 
            "role": "Head of Neurosurgery",
            "specialty": "Brain Tumor Surgery",
            "hospital": "Rush University Medical Center",
            "address": "1653 W Congress Parkway, Chicago, IL 60612",
            "search_count": 1790,
            "patient_rating": 4.6
        },
        {
            "name": "Dr. Nicole Adams", 
            "role": "Director of Pulmonary Medicine",
            "specialty": "COPD and Asthma",
            "hospital": "University of Illinois Hospital",
            "address": "1740 W Taylor Street, Chicago, IL 60612",
            "search_count": 1680,
            "patient_rating": 4.5
        }
    ]
}

# Add more mock data for other cities
for city in [c for region in usa_regions.values() for c in region if c not in doctors_data.keys()]:
    doctors_data[city] = []
    hospital_names = [
        f"{city} General Hospital", f"{city} Medical Center", 
        f"University of {city} Hospital", f"{city} Children's Hospital",
        f"St. Mary's {city}", f"{city} Memorial Hospital"
    ]
    
    specialties = {
        "Cardiology": ["Heart Rhythm Specialist", "Interventional Cardiologist", "Heart Failure Specialist"],
        "Oncology": ["Medical Oncologist", "Radiation Oncologist", "Surgical Oncologist"],
        "Neurology": ["Movement Disorder Specialist", "Stroke Specialist", "Headache Specialist"],
        "Pediatrics": ["Pediatric Cardiologist", "Pediatric Neurologist", "Pediatric Oncologist"],
        "Orthopedics": ["Joint Replacement Surgeon", "Sports Medicine Specialist", "Spine Surgeon"],
        "Surgery": ["Trauma Surgeon", "Vascular Surgeon", "Transplant Surgeon"],
        "Internal Medicine": ["Gastroenterologist", "Pulmonologist", "Endocrinologist"]
    }
    
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
                  "William", "Elizabeth", "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah", 
                  "Thomas", "Karen", "Charles", "Nancy", "Christopher", "Lisa", "Daniel", "Margaret"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", 
                 "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee"]
    
    roles = ["Chief", "Director", "Head", "Lead", "Senior Attending", "Fellowship Director", "Research Director"]
    
    addresses = {
        "Boston": ["Massachusetts", "MA"],
        "New York City": ["New York", "NY"],
        "Philadelphia": ["Pennsylvania", "PA"],
        "Hartford": ["Connecticut", "CT"],
        "Miami": ["Florida", "FL"],
        "Atlanta": ["Georgia", "GA"],
        "Charlotte": ["North Carolina", "NC"],
        "Nashville": ["Tennessee", "TN"],
        "Chicago": ["Illinois", "IL"],
        "Detroit": ["Michigan", "MI"],
        "Minneapolis": ["Minnesota", "MN"],
        "Cleveland": ["Ohio", "OH"],
        "Houston": ["Texas", "TX"],
        "Dallas": ["Texas", "TX"],
        "Phoenix": ["Arizona", "AZ"],
        "San Antonio": ["Texas", "TX"],
        "Los Angeles": ["California", "CA"],
        "San Francisco": ["California", "CA"],
        "Seattle": ["Washington", "WA"],
        "Portland": ["Oregon", "OR"]
    }
    
    for i in range(5):
        specialty_category = random.choice(list(specialties.keys()))
        specific_specialty = random.choice(specialties[specialty_category])
        role_title = f"{random.choice(roles)} of {specialty_category}"
        hospital = random.choice(hospital_names)
        state_info = addresses[city]
        street_num = random.randint(100, 9999)
        streets = ["Main Street", "Oak Avenue", "Park Boulevard", "Medical Drive", "University Way", "Health Center Parkway"]
        street = random.choice(streets)
        zipcode = f"{random.randint(10000, 99999)}"
        full_address = f"{street_num} {street}, {city}, {state_info[1]} {zipcode}"
        
        doctors_data[city].append({
            "name": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
            "role": role_title,
            "specialty": specific_specialty,
            "hospital": hospital,
            "address": full_address,
            "search_count": random.randint(1000, 2700),
            "patient_rating": round(random.uniform(4.0, 5.0), 1)
        })

# Specialty trends data
specialty_trends = {
    "Cardiology": [2340, 2420, 2580, 2750, 2890, 3050],
    "Oncology": [2100, 2230, 2310, 2480, 2650, 2780],
    "Neurology": [1950, 2020, 2110, 2240, 2350, 2460],
    "Pediatrics": [1820, 1930, 2050, 2180, 2290, 2410],
    "Orthopedics": [1780, 1850, 1920, 2070, 2190, 2300],
    "Internal Medicine": [1690, 1740, 1830, 1950, 2040, 2180],
    "Surgery": [1880, 1950, 2050, 2190, 2340, 2490]
}

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
trend_data = []

for i, month in enumerate(months):
    trend_entry = {"month": month}
    for specialty, counts in specialty_trends.items():
        trend_entry[specialty] = counts[i]
    trend_data.append(trend_entry)

# Convert trend data to DataFrame
trend_df = pd.DataFrame(trend_data)

# Header with title and date
st.title("USA Physicians Directory Dashboard")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%B %d, %Y')}")

# Main tabs for different views
tab1, tab2 = st.tabs(["Physician Directory", "Search Trends Analysis"])

with tab1:
    # Region and city selector
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("Select USA Region", list(usa_regions.keys()), key="region_dir")
    with col2:
        cities = usa_regions[region]
        city = st.selectbox("Select City", cities, key="city_dir")
    
    # Get data for the selected city
    if city in doctors_data:
        city_doctors = doctors_data[city]
        doctors_df = pd.DataFrame(city_doctors)
        
        # Search/filter options
        st.subheader(f"Physician Directory for {city}, {region}")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            # Extract all specialties from the data
            all_specialties = set()
            for doctor in city_doctors:
                all_specialties.add(doctor["specialty"])
            specialty_filter = st.multiselect("Filter by Specialty", list(all_specialties))
            
        with col2:
            # Extract all hospitals from the data
            all_hospitals = set()
            for doctor in city_doctors:
                all_hospitals.add(doctor["hospital"])
            hospital_filter = st.multiselect("Filter by Hospital", list(all_hospitals))
            
        with col3:
            # Rating filter
            min_rating = st.slider("Minimum Patient Rating", 4.0, 5.0, 4.0, 0.1)
        
        # Apply filters
        filtered_doctors = doctors_df
        if specialty_filter:
            filtered_doctors = filtered_doctors[filtered_doctors['specialty'].isin(specialty_filter)]
        if hospital_filter:
            filtered_doctors = filtered_doctors[filtered_doctors['hospital'].isin(hospital_filter)]
        filtered_doctors = filtered_doctors[filtered_doctors['patient_rating'] >= min_rating]
        
        # Display filtered doctors
        if not filtered_doctors.empty:
            for i, doctor in filtered_doctors.iterrows():
                with st.expander(f"{doctor['name']} - {doctor['role']}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Specialty:** {doctor['specialty']}")
                        st.markdown(f"**Hospital:** {doctor['hospital']}")
                        st.markdown(f"**Address:** {doctor['address']}")
                        st.markdown(f"**Patient Rating:** {doctor['patient_rating']}/5.0")
                    with col2:
                        # Display a placeholder chart for patient satisfaction over time
                        chart_data = pd.DataFrame({
                            'Month': months,
                            'Rating': [round(min(5.0, max(3.8, doctor['patient_rating'] + random.uniform(-0.3, 0.3))), 1) for _ in range(6)]
                        })
                        st.write("Patient Satisfaction Trend")
                        st.line_chart(chart_data.set_index('Month'))
                        
                        # Mock appointment availability
                        st.write("Next Available Appointment:")
                        days_until = random.randint(1, 14)
                        next_date = (datetime.datetime.now() + datetime.timedelta(days=days_until)).strftime('%B %d, %Y')
                        st.info(f"{next_date}")
        else:
            st.warning("No physicians match your selected filters.")
    else:
        st.error(f"No physician data available for {city}")

with tab2:
    # Region and city selector for trends
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("Select USA Region", list(usa_regions.keys()), key="region_trend")
    with col2:
        cities = usa_regions[region]
        city = st.selectbox("Select City", cities, key="city_trend")
    
    # Create columns for layout
    col1, col2 = st.columns(2)
    
    # Most searched doctors
    with col1:
        st.subheader(f"Most Searched Physicians in {city}")
        if city in doctors_data:
            city_doctors = pd.DataFrame(doctors_data[city])
            top_doctors = city_doctors.sort_values('search_count', ascending=False).head(5)
            top_doctors_chart = pd.DataFrame({
                'Doctor': top_doctors['name'],
                'Searches': top_doctors['search_count']
            })
            st.bar_chart(top_doctors_chart.set_index('Doctor'))
            
            # Create a table with more details
            display_columns = ['name', 'role', 'hospital', 'search_count', 'patient_rating']
            display_df = top_doctors[display_columns].rename(columns={
                'name': 'Physician',
                'role': 'Role',
                'hospital': 'Hospital',
                'search_count': 'Search Count',
                'patient_rating': 'Rating'
            })
            st.table(display_df.set_index('Physician'))
        else:
            st.error(f"No data available for {city}")
            
    # Distribution by specialty
    with col2:
        st.subheader(f"Physician Search Distribution by Specialty in {city}")
        if city in doctors_data:
            city_doctors = pd.DataFrame(doctors_data[city])
            specialty_counts = city_doctors.groupby('specialty')['search_count'].sum().reset_index()
            specialty_counts = specialty_counts.sort_values('search_count', ascending=False)
            
            # Calculate percentages
            total_searches = specialty_counts['search_count'].sum()
            specialty_counts['percentage'] = ((specialty_counts['search_count'] / total_searches) * 100).round(1).astype(str) + '%'
            
            # Display chart
            st.bar_chart(specialty_counts.set_index('specialty')['search_count'])
            
            # Display table
            st.table(specialty_counts.rename(columns={
                'specialty': 'Specialty',
                'search_count': 'Search Count'
            }).set_index('Specialty'))
        else:
            st.error(f"No data available for {city}")
    
    # Specialty search trends over time
    st.subheader("Physician Specialty Search Trends Over Time")
    specialties = list(specialty_trends.keys())
    selected_specialties = st.multiselect("Select specialties to display", specialties, default=specialties[:3])
    
    if selected_specialties:
        filtered_cols = ['month'] + selected_specialties
        filtered_trend_df = trend_df[filtered_cols].set_index('month')
        st.line_chart(filtered_trend_df)
    else:
        st.warning("Please select at least one specialty to display the trend.")
    
    # Hospital popularity by city
    st.subheader(f"Hospital Search Distribution in {city}")
    if city in doctors_data:
        city_doctors = pd.DataFrame(doctors_data[city])
        hospital_counts = city_doctors.groupby('hospital')['search_count'].sum().reset_index()
        hospital_counts = hospital_counts.sort_values('search_count', ascending=False)
        
        st.bar_chart(hospital_counts.set_index('hospital'))
    else:
        st.error(f"No data available for {city}")

# Add detailed city comparison
st.header("City Comparison Analysis")
cities_to_compare = st.multiselect("Select cities to compare", 
                                  [c for region in usa_regions.values() for c in region],
                                  default=[list(usa_regions.values())[0][0], list(usa_regions.values())[1][0]])

if cities_to_compare:
    comparison_data = []
    for city in cities_to_compare:
        if city in doctors_data:
            city_doctors = doctors_data[city]
            # Get top specialties
            specialties = {}
            for doc in city_doctors:
                if doc["specialty"] not in specialties:
                    specialties[doc["specialty"]] = 0
                specialties[doc["specialty"]] += doc["search_count"]
            
            top_specialty = max(specialties.items(), key=lambda x: x[1])[0]
            avg_rating = sum(doc["patient_rating"] for doc in city_doctors) / len(city_doctors)
            total_searches = sum(doc["search_count"] for doc in city_doctors)
            
            comparison_data.append({
                "city": city,
                "total_searches": total_searches,
                "avg_rating": round(avg_rating, 2),
                "top_specialty": top_specialty,
                "doctor_count": len(city_doctors)
            })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Total Physician Searches by City")
            st.bar_chart(comparison_df.set_index('city')['total_searches'])
        
        with col2:
            st.subheader("Average Physician Rating by City")
            st.bar_chart(comparison_df.set_index('city')['avg_rating'])
        
        st.subheader("City Comparison Details")
        st.table(comparison_df.set_index('city'))

# Add footer
st.markdown("---")
st.caption("© 2025 USA Physicians Directory Dashboard. All data is mock data for demonstration purposes only.")

# Export data functionality
if st.button("Export Data"):
    # Create a function to convert data to downloadable format
    def convert_df_to_csv(df):
        return df.to_csv().encode('utf-8')
    
    # Create downloadable CSVs
    if city in doctors_data:
        city_csv = convert_df_to_csv(pd.DataFrame(doctors_data[city]))
        trend_csv = convert_df_to_csv(trend_df)
        
        # Add download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label=f"Download {city} Physician Data",
                data=city_csv,
                file_name=f'physicians_{city}.csv',
                mime='text/csv',
            )
        with col2:
            st.download_button(
                label="Download Specialty Trend Data",
                data=trend_csv,
                file_name='physician_specialty_trends.csv',
                mime='text/csv',
            )
