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
            "hospital": hospital,
            "address": full_address,
            "search_count": random.randint(1000, 2700),
            "patient_rating": round(random.uniform(4.0, 5.0), 1),
            "speaking_events": speaking_
        "speaking_events": speaking_history,
            "publications": random.randint(20, 100),
            "citations": random.randint(1000, 5000),
            "h_index": random.randint(15, 40),
            "affiliations": affiliations,
            "bio": f"Specializing in {specific_specialty} with a focus on patient-centered care and innovative treatments. Graduated from {affiliations[0]} and is an active member of {affiliations[1]}.",
            "image_verified": random.choice([True, True, True, False]),  # Most have verified images
            "research_areas": doctor_research,
            "collaborators": collaborators,  # Will be filled later
            "clinical_trials": clinical_trials
        })

# Add collaborators after all doctors are generated
all_doctors = []
for city_doctors in doctors_data.values():
    all_doctors.extend(city_doctors)

for doctor in all_doctors:
    if not doctor["collaborators"]:  # Only fill empty collaborator lists
        # Select 2-3 random doctors as collaborators
        potential_collaborators = [d["name"] for d in all_doctors if d["name"] != doctor["name"]]
        if potential_collaborators:
            num_collaborators = min(random.randint(2, 3), len(potential_collaborators))
            doctor["collaborators"] = random.sample(potential_collaborators, num_collaborators)

# Function to get all doctors as a dataframe
def get_doctors_df():
    doctors_list = []
    for city, city_doctors in doctors_data.items():
        for doctor in city_doctors:
            doctor_copy = doctor.copy()
            doctor_copy["city"] = city
            for region, cities in usa_regions.items():
                if city in cities:
                    doctor_copy["region"] = region
                    break
            doctors_list.append(doctor_copy)
    
    return pd.DataFrame(doctors_list)

# Processing functions
def extract_specialty_category(role):
    """Extract specialty from role title"""
    if "of" in role:
        return role.split("of")[1].strip()
    return role

def count_doctors_by_region(df):
    """Count doctors by region"""
    return df.groupby("region").size().reset_index(name="count")

def count_doctors_by_specialty(df):
    """Count doctors by specialty category"""
    df["specialty_category"] = df["role"].apply(extract_specialty_category)
    return df.groupby("specialty_category").size().reset_index(name="count")

def count_doctors_by_hospital(df):
    """Count doctors by hospital"""
    return df.groupby("hospital").size().reset_index(name="count").sort_values("count", ascending=False).head(10)

def get_top_doctors(df, n=10):
    """Get top N doctors by search count"""
    return df.sort_values("search_count", ascending=False).head(n)

def get_region_for_city(city):
    """Find region for a city"""
    for region, cities in usa_regions.items():
        if city in cities:
            return region
    return "Unknown"

def create_doctor_network(df, min_connections=2):
    """Create network graph of doctor collaborations"""
    G = nx.Graph()
    
    # Add nodes
    for _, doctor in df.iterrows():
        G.add_node(doctor["name"], 
                  specialty=doctor["specialty"],
                  hospital=doctor["hospital"],
                  city=doctor["city"],
                  citations=doctor["citations"])
    
    # Add edges based on collaborations
    for _, doctor in df.iterrows():
        for collaborator in doctor["collaborators"]:
            if G.has_node(doctor["name"]) and G.has_node(collaborator):
                G.add_edge(doctor["name"], collaborator)
    
    # Filter to keep only nodes with minimum connections
    nodes_to_keep = [node for node, degree in dict(G.degree()).items() if degree >= min_connections]
    return G.subgraph(nodes_to_keep)

# Layout functions
def create_sidebar():
    st.sidebar.title("Filters")
    
    df = get_doctors_df()
    
    # Region filter
    all_regions = list(usa_regions.keys())
    selected_regions = st.sidebar.multiselect("Regions", all_regions, default=all_regions)
    
    # City filter based on selected regions
    available_cities = [city for region in selected_regions for city in usa_regions[region]]
    selected_cities = st.sidebar.multiselect("Cities", available_cities, default=available_cities[:5])
    
    # Specialty filter
    specialties = df["specialty"].unique().tolist()
    selected_specialties = st.sidebar.multiselect("Specialties", specialties, default=specialties[:5])
    
    # Rating filter
    min_rating = st.sidebar.slider("Minimum Rating", 4.0, 5.0, 4.0, 0.1)
    
    # Publications filter
    min_publications = st.sidebar.slider("Minimum Publications", 0, 100, 20)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]
    
    if selected_cities:
        filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]
    
    if selected_specialties:
        filtered_df = filtered_df[filtered_df["specialty"].isin(selected_specialties)]
    
    filtered_df = filtered_df[filtered_df["patient_rating"] >= min_rating]
    filtered_df = filtered_df[filtered_df["publications"] >= min_publications]
    
    return filtered_df

def show_dashboard(df):
    st.title("USA Physicians Directory")
    
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Physicians", len(df))
    
    with col2:
        avg_rating = round(df["patient_rating"].mean(), 2)
        st.metric("Average Rating", avg_rating)
    
    with col3:
        avg_publications = round(df["publications"].mean(), 1)
        st.metric("Avg Publications", avg_publications)
    
    with col4:
        top_region = df.groupby("region").size().idxmax()
        st.metric("Most Active Region", top_region)
    
    # Geographic Distribution
    st.header("Geographic Distribution")
    region_counts = count_doctors_by_region(df)
    
    fig = px.bar(region_counts, x="region", y="count", 
                title="Physicians by Region",
                color="region")
    st.plotly_chart(fig, use_container_width=True)
    
    # Specialty Distribution
    st.header("Specialty Distribution")
    specialty_counts = count_doctors_by_specialty(df)
    
    fig = px.pie(specialty_counts, values="count", names="specialty_category", 
                title="Physicians by Specialty",
                hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Hospitals
    st.header("Top Hospitals")
    hospital_counts = count_doctors_by_hospital(df)
    
    fig = px.bar(hospital_counts, x="hospital", y="count", 
                title="Top Hospitals by Number of Physicians",
                color="count")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Physicians
    st.header("Top Physicians by Search Count")
    top_doctors = get_top_doctors(df)
    
    fig = px.bar(top_doctors, x="name", y="search_count", 
                title="Most Searched Physicians",
                color="specialty",
                hover_data=["hospital", "patient_rating", "publications"])
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Physician Network Analysis
    st.header("Physician Collaboration Network")
    network_df = df.copy()
    
    if len(network_df) > 0:
        G = create_doctor_network(network_df)
        
        if len(G.nodes()) > 0:
            # Convert NetworkX graph to Plotly figure
            pos = nx.spring_layout(G, seed=42)
            
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            node_x = []
            node_y = []
            node_text = []
            node_size = []
            node_color = []
            
            specialty_colors = {}
            color_idx = 0
            
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                
                specialty = G.nodes[node]['specialty']
                hospital = G.nodes[node]['hospital']
                city = G.nodes[node]['city']
                citations = G.nodes[node]['citations']
                
                node_text.append(f"Name: {node}<br>Specialty: {specialty}<br>Hospital: {hospital}<br>City: {city}<br>Citations: {citations}")
                
                # Node size based on citations
                node_size.append(min(citations/100, 20))
                
                # Node color based on specialty
                if specialty not in specialty_colors:
                    specialty_colors[specialty] = color_idx
                    color_idx += 1
                node_color.append(specialty_colors[specialty])
            
            # Create edge trace
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines')
            
            # Create node trace
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
                text=node_text,
                marker=dict(
                    showscale=True,
                    colorscale='Viridis',
                    size=node_size,
                    color=node_color,
                    line_width=2))
            
            # Create network figure
            fig = go.Figure(data=[edge_trace, node_trace],
                         layout=go.Layout(
                            title='Physician Collaboration Network',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("Node size represents citation count, color represents different specialties")
        else:
            st.write("Not enough connected physicians to create network visualization.")
    else:
        st.write("No physicians data available for network visualization.")

def show_physician_directory(df):
    st.header("Physician Directory")
    
    # Search
    search_term = st.text_input("Search physicians by name, specialty, or hospital")
    
    if search_term:
        search_term = search_term.lower()
        search_results = df[
            df["name"].str.lower().str.contains(search_term) | 
            df["specialty"].str.lower().str.contains(search_term) | 
            df["hospital"].str.lower().str.contains(search_term)
        ]
        display_df = search_results
    else:
        display_df = df
    
    # Sort options
    sort_option = st.selectbox(
        "Sort by",
        ["Search Count (High to Low)", "Rating (High to Low)", "Publications (High to Low)", "Name (A-Z)"]
    )
    
    if sort_option == "Search Count (High to Low)":
        display_df = display_df.sort_values("search_count", ascending=False)
    elif sort_option == "Rating (High to Low)":
        display_df = display_df.sort_values("patient_rating", ascending=False)
    elif sort_option == "Publications (High to Low)":
        display_df = display_df.sort_values("publications", ascending=False)
    else:  # Name (A-Z)
        display_df = display_df.sort_values("name")
    
    # Display results with pagination
    items_per_page = 5
    total_pages = max(1, len(display_df) // items_per_page + (1 if len(display_df) % items_per_page > 0 else 0))
    
    col1, col2 = st.columns([8, 2])
    with col2:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    with col1:
        st.write(f"Showing {min((page-1)*items_per_page+1, len(display_df))} to {min(page*items_per_page, len(display_df))} of {len(display_df)} physicians")
    
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(display_df))
    
    for i in range(start_idx, end_idx):
        doctor = display_df.iloc[i]
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Profile image placeholder
            if doctor["image_verified"]:
                st.image("https://placehold.co/150x150.png", caption="Verified Profile")
            else:
                st.image("https://placehold.co/150x150/CCCCCC/FFFFFF.png", caption="No Image")
        
        with col2:
            st.subheader(doctor["name"])
            st.write(f"**Role:** {doctor['role']}")
            st.write(f"**Specialty:** {doctor['specialty']}")
            st.write(f"**Hospital:** {doctor['hospital']}")
            st.write(f"**Location:** {doctor['city']}")
            
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.write(f"⭐ **Rating:** {doctor['patient_rating']}/5.0")
            with col2b:
                st.write(f"📊 **Publications:** {doctor['publications']}")
            with col2c:
                st.write(f"🔍 **Searches:** {doctor['search_count']}")
            
            with st.expander("See Details"):
                st.write(f"**Biography:** {doctor['bio']}")
                st.write(f"**Address:** {doctor['address']}")
                
                st.write("**Research Areas:**")
                for area in doctor["research_areas"]:
                    st.write(f"- {area}")
                
                st.write("**Speaking Events:**")
                for event in doctor["speaking_events"]:
                    st.write(f"- {event}")
                
                st.write("**Collaborators:**")
                for collaborator in doctor["collaborators"]:
                    st.write(f"- {collaborator}")
                
                st.write("**Clinical Trials:**")
                for trial in doctor["clinical_trials"]:
                    st.write(f"- {trial}")
                
                st.write(f"**H-Index:** {doctor['h_index']}")
                st.write(f"**Total Citations:** {doctor['citations']}")
                
                st.write("**Academic Affiliations:**")
                for affiliation in doctor["affiliations"]:
                    st.write(f"- {affiliation}")
        
        st.markdown("---")

def show_analytics(df):
    st.header("Analytics Dashboard")
    
    # Ratings Distribution
    st.subheader("Physician Ratings Distribution")
    
    fig = px.histogram(df, x="patient_rating", nbins=10, 
                      title="Distribution of Physician Ratings",
                      color_discrete_sequence=['#3366CC'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Research Impact
    st.subheader("Research Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df, x="publications", y="citations",
                        color="specialty", size="h_index",
                        hover_data=["name", "hospital", "city"],
                        title="Research Impact: Publications vs Citations")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Aggregate research metrics by specialty
        specialty_metrics = df.groupby("specialty").agg({
            "publications": "mean",
            "citations": "mean",
            "h_index": "mean"
        }).reset_index()
        
        specialty_metrics["publications"] = specialty_metrics["publications"].round(1)
        specialty_metrics["citations"] = specialty_metrics["citations"].round(1)
        specialty_metrics["h_index"] = specialty_metrics["h_index"].round(1)
        
        fig = px.bar(specialty_metrics.sort_values("h_index", ascending=False).head(10), 
                    x="specialty", y="h_index",
                    title="Average H-Index by Top 10 Specialties",
                    color="h_index")
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Heatmap
    st.subheader("Correlation Analysis")
    
    numeric_cols = ["search_count", "patient_rating", "publications", "citations", "h_index"]
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(corr_matrix, 
                   labels=dict(x="Metric", y="Metric", color="Correlation"),
                   x=corr_matrix.columns,
                   y=corr_matrix.columns,
                   color_continuous_scale="RdBu_r")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional Comparison
    st.subheader("Regional Comparison")
    
    region_metrics = df.groupby("region").agg({
        "patient_rating": "mean",
        "publications": "mean",
        "citations": "mean",
        "h_index": "mean",
        "search_count": "mean"
    }).reset_index()
    
    # Round values for display
    for col in region_metrics.columns:
        if col != "region":
            region_metrics[col] = region_metrics[col].round(2)
    
    # Multi-metric comparison radar chart
    categories = ["Patient Rating", "Publications", "Citations", "H-Index", "Search Count"]
    
    fig = go.Figure()
    
    for i, region in enumerate(region_metrics["region"]):
        values = [
            region_metrics.loc[i, "patient_rating"] / region_metrics["patient_rating"].max(),
            region_metrics.loc[i, "publications"] / region_metrics["publications"].max(),
            region_metrics.loc[i, "citations"] / region_metrics["citations"].max(),
            region_metrics.loc[i, "h_index"] / region_metrics["h_index"].max(),
            region_metrics.loc[i, "search_count"] / region_metrics["search_count"].max()
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=region
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Regional Performance Comparison (Normalized)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Hospital Rankings
    st.subheader("Top Hospitals Analysis")
    
    # Get top hospitals with at least 3 physicians
    hospital_counts = df.groupby("hospital").size()
    top_hospitals = hospital_counts[hospital_counts >= 3].index.tolist()
    
    if top_hospitals:
        top_hospital_df = df[df["hospital"].isin(top_hospitals)]
        
        hospital_metrics = top_hospital_df.groupby("hospital").agg({
            "patient_rating": "mean",
            "publications": "mean",
            "citations": "mean",
            "h_index": "mean"
        }).reset_index()
        
        for col in hospital_metrics.columns:
            if col != "hospital":
                hospital_metrics[col] = hospital_metrics[col].round(2)
        
        metric_option = st.selectbox(
            "Select metric for hospital comparison",
            ["Average Rating", "Average Publications", "Average Citations", "Average H-Index"]
        )
        
        if metric_option == "Average Rating":
            col_name = "patient_rating"
            title = "Top Hospitals by Average Physician Rating"
        elif metric_option == "Average Publications":
            col_name = "publications"
            title = "Top Hospitals by Average Physician Publications"
        elif metric_option == "Average Citations":
            col_name = "citations"
            title = "Top Hospitals by Average Physician Citations" 
        else:
            col_name = "h_index"
            title = "Top Hospitals by Average Physician H-Index"
        
        # Create sorted bar chart
        fig = px.bar(
            hospital_metrics.sort_values(col_name, ascending=False).head(10),
            x="hospital",
            y=col_name,
            title=title,
            color=col_name,
            text_auto='.2f'
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Not enough data for meaningful hospital comparisons.")

# Main app
def main():
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Physician Directory", "Analytics"])
    
    # Filter data
    filtered_df = create_sidebar()
    
    # Populate tabs
    with tab1:
        show_dashboard(filtered_df)
    
    with tab2:
        show_physician_directory(filtered_df)
    
    with tab3:
        show_analytics(filtered_df)

if __name__ == "__main__":
    main()
