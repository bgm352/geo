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
            "hospital": "Dana-Farber Cancer Institute",
            "address": "450 Brookline Avenue, Boston, MA 02215",
            "search_count": 1980,
            "patient_rating": 4.7,
            "speaking_events": ["American Society of Clinical Oncology Annual Meeting", 
                              "European Hematology Association Congress", 
                              "World Oncology Forum"],
            "publications": 92,
            "citations": 4120,
            "h_index": 38,
            "affiliations": ["Harvard Medical School", "American Society of Hematology"],
            "bio": "Dr. Wilson specializes in hematologic malignancies with a focus on leukemia and lymphoma. His research has pioneered several targeted therapies that have significantly improved patient outcomes.",
            "image_verified": True,
            "research_areas": ["Lymphoma therapeutics", "CAR-T cell therapy", "Hematopoietic stem cell transplantation"],
            "collaborators": ["Dr. Elizabeth Chen", "Dr. Sarah Johnson", "Dr. Robert Chang"],
            "clinical_trials": ["CAR-T Cell Therapy in Refractory Lymphoma", "Novel Approaches to AML", "Immunotherapy in Lymphoma"]
        },
        {
            "name": "Dr. Sarah Johnson", 
            "role": "Pediatric Surgeon",
            "specialty": "Pediatric Cardiothoracic Surgery",
            "hospital": "Boston Children's Hospital",
            "address": "300 Longwood Avenue, Boston, MA 02115",
            "search_count": 1750,
            "patient_rating": 4.9,
            "speaking_events": ["Society of Thoracic Surgeons Annual Meeting", 
                              "World Congress of Pediatric Cardiology and Cardiac Surgery", 
                              "American Academy of Pediatrics National Conference"],
            "publications": 65,
            "citations": 2890,
            "h_index": 28,
            "affiliations": ["Harvard Medical School", "American Academy of Pediatrics"],
            "bio": "Dr. Johnson is a leading pediatric cardiothoracic surgeon specializing in complex congenital heart defect repairs. She has developed innovative surgical techniques for neonatal heart surgery.",
            "image_verified": True,
            "research_areas": ["Congenital heart defects", "Minimally invasive techniques", "Post-surgical outcomes"],
            "collaborators": ["Dr. James Wilson", "Dr. Jennifer Williams", "Dr. Lisa Martinez"],
            "clinical_trials": ["Pediatric Heart Valve Development", "Congenital Heart Defect Registry", "Minimally Invasive Approaches in Children"]
        },
        {
            "name": "Dr. Michael Rodriguez", 
            "role": "Neurosurgery Department Head",
            "specialty": "Spine and Brain Surgery",
            "hospital": "Brigham and Women's Hospital",
            "address": "75 Francis Street, Boston, MA 02115",
            "search_count": 1680,
            "patient_rating": 4.6,
            "speaking_events": ["Congress of Neurological Surgeons Annual Meeting", 
                              "American Association of Neurological Surgeons", 
                              "World Federation of Neurosurgical Societies Symposium"],
            "publications": 71,
            "citations": 3280,
            "h_index": 30,
            "affiliations": ["Harvard Medical School", "American Board of Neurological Surgery"],
            "bio": "Dr. Rodriguez is recognized for his expertise in complex spine surgeries and skull base neurosurgery. He has pioneered minimally invasive approaches to previously inoperable brain tumors.",
            "image_verified": True,
            "research_areas": ["Brain tumor surgery", "Skull base approaches", "Spine biomechanics"],
            "collaborators": ["Dr. Elizabeth Chen", "Dr. Kevin Park", "Dr. Maria Sanchez"],
            "clinical_trials": ["Advanced Neurosurgical Navigation Techniques", "Brain Tumor Immunotherapy", "Spine Fusion Outcomes"]
        },
        {
            "name": "Dr. Rebecca Liu", 
            "role": "Chief of Endocrinology",
            "specialty": "Diabetes Management",
            "hospital": "Tufts Medical Center",
            "address": "800 Washington Street, Boston, MA 02111",
            "search_count": 1420,
            "patient_rating": 4.5,
            "speaking_events": ["American Diabetes Association Scientific Sessions", 
                              "Endocrine Society Annual Meeting", 
                              "International Diabetes Federation Congress"],
            "publications": 58,
            "citations": 2140,
            "h_index": 25,
            "affiliations": ["Tufts University School of Medicine", "American Diabetes Association"],
            "bio": "Dr. Liu specializes in complex diabetes management and insulin resistance syndromes. Her research focuses on novel therapeutic approaches for type 1 diabetes and technological innovations in glucose monitoring.",
            "image_verified": True,
            "research_areas": ["Diabetes technology", "Insulin resistance", "Artificial pancreas development"],
            "collaborators": ["Dr. Nicole Adams", "Dr. Richard Brown", "Dr. Thomas Jackson"],
            "clinical_trials": ["Closed-Loop Insulin Delivery Systems", "Diabetes Prevention Program", "Artificial Pancreas Development"]
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
            "patient_rating": 4.9,
            "speaking_events": ["American College of Cardiology Annual Meeting", 
                              "Society of Thoracic Surgeons Convention", 
                              "International Society for Minimally Invasive Cardiothoracic Surgery"],
            "publications": 84,
            "citations": 3980,
            "h_index": 36,
            "affiliations": ["Weill Cornell Medicine", "American Association for Thoracic Surgery"],
            "bio": "Dr. Goldstein is internationally recognized for pioneering minimally invasive cardiac surgical techniques. He has performed over 5,000 cardiac procedures and trained surgeons worldwide.",
            "image_verified": True,
            "research_areas": ["Robotic cardiac surgery", "Aortic valve repair", "Minimally invasive bypass"],
            "collaborators": ["Dr. Elizabeth Chen", "Dr. Thomas Jackson", "Dr. Robert Chang"],
            "clinical_trials": ["Minimally Invasive Valve Outcomes Study", "Robotic Cardiac Surgery Trial", "Post-Operative Recovery Enhancement"]
        },
        {
            "name": "Dr. Maria Sanchez", 
            "role": "Director of Neurology",
            "specialty": "Movement Disorders",
            "hospital": "NYU Langone Medical Center",
            "address": "550 First Avenue, New York, NY 10016",
            "search_count": 2240,
            "patient_rating": 4.7,
            "speaking_events": ["American Academy of Neurology Annual Meeting", 
                              "International Congress of Parkinson's Disease and Movement Disorders", 
                              "World Neurology Congress"],
            "publications": 76,
            "citations": 3120,
            "h_index": 29,
            "affiliations": ["NYU School of Medicine", "Movement Disorder Society"],
            "bio": "Dr. Sanchez is a leading expert in Parkinson's disease and movement disorders. Her research has contributed to new understanding of the pathophysiology of tremor disorders and novel therapeutic approaches.",
            "image_verified": True,
            "research_areas": ["Parkinson's disease", "Essential tremor", "Deep brain stimulation"],
            "collaborators": ["Dr. Michael Rodriguez", "Dr. Kevin Park", "Dr. Jennifer Williams"],
            "clinical_trials": ["Deep Brain Stimulation in Treatment-Resistant Tremor", "Novel Therapeutics for Parkinson's", "Biomarker Development for Movement Disorders"]
        },
        {
            "name": "Dr. Robert Chang", 
            "role": "Chief Surgical Oncologist",
            "specialty": "Gastrointestinal Cancer",
            "hospital": "Memorial Sloan Kettering Cancer Center",
            "address": "1275 York Avenue, New York, NY 10065",
            "search_count": 2190,
            "patient_rating": 4.8,
            "speaking_events": ["American Society of Clinical Oncology", 
                              "Society of Surgical Oncology Annual Cancer Symposium", 
                              "International Gastric Cancer Congress"],
            "publications": 103,
            "citations": 5240,
            "h_index": 42,
            "affiliations": ["Weill Cornell Medicine", "American College of Surgeons"],
            "bio": "Dr. Chang specializes in complex surgical oncology procedures for gastrointestinal malignancies. His research has advanced the field of molecular markers in gastric cancer and minimally invasive approaches.",
            "image_verified": True,
            "research_areas": ["Gastric cancer", "Hepatobiliary malignancies", "Minimally invasive oncologic surgery"],
            "collaborators": ["Dr. James Wilson", "Dr. David Goldstein", "Dr. Amanda Patel"],
            "clinical_trials": ["Gastric Cancer Molecular Profiling", "Immunotherapy in Gastrointestinal Malignancies", "Minimally Invasive Approaches to Hepatic Tumors"]
        },
        {
            "name": "Dr. Jennifer Williams", 
            "role": "Pediatric Neurologist",
            "specialty": "Pediatric Epilepsy",
            "hospital": "Mount Sinai Hospital",
            "address": "1 Gustave L. Levy Place, New York, NY 10029",
            "search_count": 1870,
            "patient_rating": 4.6,
            "speaking_events": ["American Epilepsy Society Annual Meeting", 
                              "Child Neurology Society Annual Meeting", 
                              "International Child Neurology Congress"],
            "publications": 61,
            "citations": 2460,
            "h_index": 26,
            "affiliations": ["Icahn School of Medicine at Mount Sinai", "American Epilepsy Society"],
            "bio": "Dr. Williams is a renowned pediatric epileptologist specializing in difficult-to-treat childhood seizure disorders. Her research has led to improved diagnostic approaches for rare epilepsy syndromes.",
            "image_verified": True,
            "research_areas": ["Pediatric epilepsy", "Neurogenetics", "Ketogenic diet therapy"],
            "collaborators": ["Dr. Sarah Johnson", "Dr. Maria Sanchez", "Dr. Lisa Martinez"],
            "clinical_trials": ["Pediatric Epilepsy Genetics Study", "Novel Anti-Seizure Medications", "Ketogenic Diet Protocol"]
        },
        {
            "name": "Dr. Thomas Jackson", 
            "role": "Head of Orthopedic Surgery",
            "specialty": "Sports Medicine",
            "hospital": "Hospital for Special Surgery",
            "address": "535 East 70th Street, New York, NY 10021",
            "search_count": 1730,
            "patient_rating": 4.8,
            "speaking_events": ["American Academy of Orthopaedic Surgeons Annual Meeting", 
                              "American Orthopaedic Society for Sports Medicine", 
                              "International Society of Arthroscopy, Knee Surgery and Orthopaedic Sports Medicine"],
            "publications": 68,
            "citations": 2950,
            "h_index": 27,
            "affiliations": ["Weill Cornell Medicine", "American Orthopaedic Association"],
            "bio": "Dr. Jackson is a leading sports medicine specialist who has served as team physician for several professional sports organizations. His innovative techniques in ACL reconstruction have transformed the field.",
            "image_verified": True,
            "research_areas": ["Knee ligament repair", "Cartilage restoration", "Return-to-play protocols"],
            "collaborators": ["Dr. David Goldstein", "Dr. Rebecca Liu", "Dr. Nicole Adams"],
            "clinical_trials": ["ACL Reconstruction Techniques", "Cartilage Regeneration Approaches", "Return to Sport Protocols"]
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
            "patient_rating": 4.9,
            "speaking_events": ["American Transplant Congress", 
                              "International Liver Transplantation Society Annual Meeting", 
                              "World Transplant Congress"],
            "publications": 87,
            "citations": 3870,
            "h_index": 34,
            "affiliations": ["Northwestern University Feinberg School of Medicine", "American Society of Transplant Surgeons"],
            "bio": "Dr. Patel is a pioneer in living donor liver transplantation and has developed novel immunosuppression protocols that have improved graft survival rates significantly.",
            "image_verified": True,
            "research_areas": ["Transplant immunology", "Living donor outcomes", "Transplant infectious diseases"],
            "collaborators": ["Dr. Robert Chang", "Dr. Richard Brown", "Dr. Kevin Park"],
            "clinical_trials": ["Novel Immunosuppression Protocols", "Living Donor Outcome Study", "Transplant Infectious Disease Management"]
        },
        {
            "name": "Dr. Richard Brown", 
            "role": "Director of Cardiology",
            "specialty": "Preventive Cardiology",
            "hospital": "University of Chicago Medical Center",
            "address": "5841 S Maryland Avenue, Chicago, IL 60637",
            "search_count": 2150,
            "patient_rating": 4.7,
            "speaking_events": ["American Heart Association Scientific Sessions", 
                              "American College of Cardiology Annual Meeting", 
                              "World Congress of Cardiology"],
            "publications": 79,
            "citations": 3340,
            "h_index": 31,
            "affiliations": ["University of Chicago Pritzker School of Medicine", "American Society of Preventive Cardiology"],
            "bio": "Dr. Brown is a leading researcher in cardiovascular disease prevention. His work on novel lipid-lowering therapies has been instrumental in developing new approaches to atherosclerosis management.",
            "image_verified": True,
            "research_areas": ["Preventive cardiology", "Lipid disorders", "Cardiovascular risk prediction"],
            "collaborators": ["Dr. Elizabeth Chen", "Dr. Rebecca Liu", "Dr. Amanda Patel"],
            "clinical_trials": ["Cardiovascular Risk Reduction Strategy", "Lipid-Lowering Therapeutic Trial", "Atherosclerosis Prevention Study"]
        },
        {
            "name": "Dr. Lisa Martinez", 
            "role": "Chief of Pediatric Oncology",
            "specialty": "Childhood Leukemia",
            "hospital": "Ann & Robert H. Lurie Children's Hospital",
            "address": "225 E Chicago Avenue, Chicago, IL 60611",
            "search_count": 1950,
            "patient_rating": 4.8,
            "speaking_events": ["American Society of Pediatric Hematology/Oncology Conference", 
                              "International Society of Paediatric Oncology Congress", 
                              "American Society of Hematology Annual Meeting"],
            "publications": 73,
            "citations": 3210,
            "h_index": 30,
            "affiliations": ["Northwestern University Feinberg School of Medicine", "Children's Oncology Group"],
            "bio": "Dr. Martinez has dedicated her career to improving outcomes for children with leukemia. Her research has contributed to the development of targeted therapies that have significantly improved survival rates.",
            "image_verified": True,
            "research_areas": ["Acute lymphoblastic leukemia", "Pediatric cancer genomics", "Targeted therapy development"],
            "collaborators": ["Dr. Sarah Johnson", "Dr. Jennifer Williams", "Dr. James Wilson"],
            "clinical_trials": ["Pediatric Leukemia Genomics", "Novel Targeted Therapies in ALL", "Survivorship Protocol Development"]
        },
        {
            "name": "Dr. Kevin Park", 
            "role": "Head of Neurosurgery",
            "specialty": "Brain Tumor Surgery",
            "hospital": "Rush University Medical Center",
            "address": "1653 W Congress Parkway, Chicago, IL 60612",
            "search_count": 1790,
            "patient_rating": 4.6,
            "speaking_events": ["Congress of Neurological Surgeons Annual Meeting", 
                              "Society for Neuro-Oncology Annual Meeting", 
                              "World Federation of Neurosurgical Societies Symposium"],
            "publications": 64,
            "citations": 2780,
            "h_index": 27,
            "affiliations": ["Rush Medical College", "American Association of Neurological Surgeons"],
            "bio": "Dr. Park is renowned for his expertise in complex brain tumor surgeries, particularly in eloquent brain regions. He has pioneered the use of intraoperative mapping techniques to maximize tumor removal while preserving function.",
            "image_verified": True,
            "research_areas": ["Glioma surgery", "Intraoperative brain mapping", "Surgical neuro-oncology"],
            "collaborators": ["Dr. Michael Rodriguez", "Dr. Maria Sanchez", "Dr. Amanda Patel"],
            "clinical_trials": ["Advanced Brain Mapping Techniques", "Novel Approaches to Glioblastoma", "Neuro-Oncology Combined Therapy Trial"]
        },
        {
            "name": "Dr. Nicole Adams", 
            "role": "Director of Pulmonary Medicine",
            "specialty": "COPD and Asthma",
            "hospital": "University of Illinois Hospital",
            "address": "1740 W Taylor Street, Chicago, IL 60612",
            "search_count": 1680,
            "patient_rating": 4.5,
            "speaking_events": ["American Thoracic Society International Conference", 
                              "European Respiratory Society Annual Congress", 
                              "World Congress on COPD and Lung Health"],
            "publications": 56,
            "citations": 2350,
            "h_index": 25,
            "affiliations": ["University of Illinois College of Medicine", "American College of Chest Physicians"],
            "bio": "Dr. Adams specializes in advanced diagnostic and treatment approaches for complex respiratory conditions. Her research focuses on personalized medicine approaches to severe asthma and COPD.",
            "image_verified": True,
            "research_areas": ["Severe asthma phenotypes", "COPD exacerbation prevention", "Pulmonary rehabilitation"],
            "collaborators": ["Dr. Rebecca Liu", "Dr. Thomas Jackson", "Dr. Richard Brown"],
            "clinical_trials": ["Severe Asthma Phenotyping Study", "COPD Exacerbation Prevention Protocol", "Pulmonary Rehabilitation Outcomes Assessment"]
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
    
    # Conferences by specialty
    conferences = {
        "Cardiology": ["American Heart Association Scientific Sessions", "American College of Cardiology Annual Meeting", 
                     "European Society of Cardiology Congress", "World Congress of Cardiology"],
        "Oncology": ["American Society of Clinical Oncology Annual Meeting", "European Society for Medical Oncology Congress", 
                   "World Cancer Congress", "American Association for Cancer Research Annual Meeting"],
        "Neurology": ["American Academy of Neurology Annual Meeting", "World Congress of Neurology", 
                    "International Stroke Conference", "Congress of Neurological Surgeons Annual Meeting"],
        "Pediatrics": ["American Academy of Pediatrics National Conference", "Pediatric Academic Societies Meeting", 
                     "World Congress of Pediatrics", "International Pediatric Association Congress"],
        "Orthopedics": ["American Academy of Orthopaedic Surgeons Annual Meeting", "Orthopaedic Research Society Annual Meeting", 
                      "International Society of Orthopaedic Surgery and Traumatology", "American Orthopaedic Society for Sports Medicine"],
        "Surgery": ["American College of Surgeons Clinical Congress", "Society of American Gastrointestinal and Endoscopic Surgeons", 
                  "International Surgical Week", "European Society for Surgical Research"],
        "Internal Medicine": ["American College of Physicians Internal Medicine Meeting", "Society of General Internal Medicine Annual Meeting", 
                           "International Society of Internal Medicine Congress", "European Federation of Internal Medicine"]
    }
    
    # Research areas by specialty
    research_areas = {
        "Cardiology": ["Coronary artery disease", "Heart failure mechanisms", "Arrhythmia management", 
                     "Valvular heart disease", "Preventive cardiology", "Cardiovascular imaging"],
        "Oncology": ["Cancer immunotherapy", "Precision oncology", "Tumor microenvironment", 
                   "Cancer genomics", "Novel therapeutic targets", "Radiation oncology advances"],
        "Neurology": ["Neurodegenerative disorders", "Stroke treatment and prevention", "Neuroinflammation", 
                    "Headache disorders", "Multiple sclerosis", "Neurological complications of systemic disease"],
        "Pediatrics": ["Developmental disorders", "Pediatric infectious diseases", "Neonatal medicine", 
                     "Childhood obesity", "Adolescent medicine", "Genetic disorders in children"],
        "Orthopedics": ["Joint replacement outcomes", "Sports injury prevention", "Bone and cartilage regeneration", 
                      "Spinal deformities", "Orthopedic biomaterials", "Musculoskeletal trauma"],
        "Surgery": ["Minimally invasive techniques", "Transplantation outcomes", "Surgical oncology", 
                  "Trauma systems", "Robotic surgery applications", "Surgical education"],
        "Internal Medicine": ["Chronic disease management", "Diagnostic decision making", "Hospital medicine", 
                           "Medical education", "Patient safety", "Health services research"]
    }
    
    # Medical schools and professional organizations
    medical_schools = ["Harvard Medical School", "Johns Hopkins School of Medicine", "Stanford School of Medicine", 
                     "UCSF School of Medicine", "Yale School of Medicine", "Columbia University Vagelos College of Physicians & Surgeons",
                     "Perelman School of Medicine at the University of Pennsylvania", "Duke University School of Medicine",
                     "Washington University School of Medicine", "University of Michigan Medical School"]
                     
    professional_orgs = ["American Medical Association", "American Board of Medical Specialties", 
                       "American College of Physicians", "American Academy of Family Physicians",
                       "American Society of Clinical Oncology", "American College of Surgeons",
                       "American Academy of Pediatrics", "American College of Cardiology",
                       "American Neurological Association", "American College of Obstetricians and Gynecologists"]
    
    # Define potential clinical trials
    clinical_trials_templates = {
        "Cardiology": ["Novel Anticoagulation Therapy", "Heart Failure Management Protocol", "Coronary Stent Evaluation"],
        "Oncology": ["Immunotherapy Combination Trial", "Targeted Therapy for Metastatic Disease", "Cancer Genomics Study"],
        "Neurology": ["Multiple Sclerosis Treatment Protocol", "Alzheimer's Disease Biomarker Study", "Stroke Recovery Assessment"],
        "Pediatrics": ["Childhood Asthma Management", "Adolescent Mental Health Intervention", "Neonatal Care Protocol"],
        "Orthopedics": ["Joint Replacement Outcomes", "Fracture Healing Enhancement", "Sports Injury Prevention"],
        "Surgery": ["Post-Surgical Recovery Enhancement", "Minimally Invasive Technique Assessment", "Surgical Wound Management"],
        "Internal Medicine": ["Diabetes Management Protocol", "Hypertension Control Study", "COPD Exacerbation Prevention"]
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
        
        # Generate speaking events
        speaking_history = []
        for _ in range(3):
            if specialty_category in conferences:
                speaking_history.append(random.choice(conferences[specialty_category]))
            else:
                speaking_history.append("Annual Medical Conference")
        
        # Generate research areas
        doctor_research = []
        if specialty_category in research_areas:
            areas = research_areas[specialty_category]
            for _ in range(3):
                area = random.choice(areas)
                if area not in doctor_research:
                    doctor_research.append(area)
        else:
            doctor_research = ["Clinical outcomes", "Patient care improvement", "Medical education"]
        
        # Generate affiliations
        affiliations = []
        affiliations.append(random.choice(medical_schools))
        affiliations.append(random.choice(professional_orgs))
        
        # Generate clinical trials
        clinical_trials = []
        if specialty_category in clinical_trials_templates:
            templates = clinical_trials_templates[specialty_category]
            for _ in range(3):
                trial = random.choice(templates)
                if trial not in clinical_trials:
                    clinical_trials.append(trial)
        else:
            clinical_trials = ["Clinical Outcomes Assessment", "Patient Care Improvement Study", "Medical Practice Evaluation"]
        
        # Generate potential collaborators (will be populated later)
        collaborators = []
        
        # Create doctor record
        doctors_data[city].append({
            "name": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
            "role": role_title,
            "specialty": specific_specialty,
            "hospital
