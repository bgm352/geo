import streamlit as st
import pandas as pd
import datetime
import random
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from urllib.parse import quote
from collections import Counter

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
            "patient_rating": 4.8,
            "speaking_events": ["American Heart Association Annual Conference 2024",
                              "New England Cardiology Symposium",
                              "International Congress of Cardiology"],
            "publications": 78,
            "citations": 3450,
            "h_index": 32,
            "affiliations": ["Harvard Medical School", "American College of Cardiology"],
            "bio": "Dr. Chen is a renowned interventional cardiologist specializing in complex coronary interventions and structural heart disease. She completed her medical education at Harvard Medical School and her residency at Massachusetts General Hospital.",
            "image_verified": True,
            "research_areas": ["Coronary artery disease", "Valvular heart disease", "Transcatheter interventions"],
            "collaborators": ["Dr. James Wilson", "Dr. Michael Rodriguez", "Dr. Richard Brown"],
            "clinical_trials": ["STEMI Outcomes Study", "Novel Stent Technology Trial", "Post-MI Management Protocol"]
        },
        {
            "name": "Dr. James Wilson",
            "role": "Director of Oncology",
            "specialty": "Hematologic Oncology",
            "hospital
