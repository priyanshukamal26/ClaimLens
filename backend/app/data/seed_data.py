"""
ClaimLens Nexus — Indian Insurance Seed Data

Real Indian states, cities, insurer names, hospital names, and line-of-business
categories for generating realistic synthetic data.

Per DATA.md: No India-specific claim-level fraud dataset exists publicly.
This seed data is used to generate synthetic data that looks realistic.
"""

# Indian states (28 states + 8 UTs — using major ones for data distribution)
STATES = [
    "Maharashtra", "Tamil Nadu", "Karnataka", "Delhi", "Uttar Pradesh",
    "Gujarat", "Rajasthan", "West Bengal", "Telangana", "Kerala",
    "Madhya Pradesh", "Andhra Pradesh", "Punjab", "Haryana", "Bihar",
    "Odisha", "Jharkhand", "Assam", "Chhattisgarh", "Uttarakhand",
    "Goa", "Himachal Pradesh", "Chandigarh", "Puducherry",
]

# Major cities per state (for hospitals/garages)
STATE_CITIES = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Trichy"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangalore", "Belgaum"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur", "Agra", "Varanasi"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur", "Asansol"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Nellore"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Sambalpur", "Puri"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat", "Tezpur"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Haldwani", "Roorkee", "Rishikesh"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
    "Himachal Pradesh": ["Shimla", "Dharamshala", "Manali", "Solan", "Mandi"],
    "Chandigarh": ["Chandigarh"],
    "Puducherry": ["Puducherry"],
}

# Lines of business (per REQUIREMENTS.md FR-002)
LINES_OF_BUSINESS = ["Health", "Motor", "Fire", "Marine", "Miscellaneous"]

# LOB weight distribution (roughly mirrors Indian non-life market)
LOB_WEIGHTS = {
    "Health": 0.35,
    "Motor": 0.35,
    "Fire": 0.10,
    "Marine": 0.05,
    "Miscellaneous": 0.15,
}

# Claim types per LOB
LOB_CLAIM_TYPES = {
    "Health": ["Cashless", "Reimbursement"],
    "Motor": ["Own Damage", "Third-Party"],
    "Fire": ["Reimbursement"],
    "Marine": ["Reimbursement"],
    "Miscellaneous": ["Reimbursement", "Third-Party"],
}

# Major non-life insurers (real names, public knowledge)
INSURERS = [
    "New India Assurance", "United India Insurance", "National Insurance",
    "Oriental Insurance", "ICICI Lombard", "HDFC ERGO", "Bajaj Allianz",
    "SBI General", "Tata AIG", "Reliance General", "Cholamandalam MS",
    "IFFCO Tokio", "Bharti AXA", "Future Generali", "Kotak Mahindra General",
    "Star Health", "Care Health", "Niva Bupa", "Aditya Birla Health",
    "Max Bupa",
]

# TPA networks (for hospitals)
TPA_NETWORKS = [
    "Medi Assist", "Paramount Health Services", "MD India",
    "Vidal Health", "Heritage Health", "FHPL", "Raksha TPA",
    "Good Health TPA", "United Healthcare", "Ericson TPA",
]

# Hospital name prefixes/patterns
HOSPITAL_PREFIXES = [
    "Apollo", "Fortis", "Max", "Manipal", "Narayana", "Medanta",
    "Columbia Asia", "Aster", "KIMS", "Yashoda", "Global", "City",
    "Metro", "Sai", "Lotus", "Rainbow", "Care", "Sunshine", "Sakra",
    "Lilavati",
]

HOSPITAL_SUFFIXES = [
    "Hospital", "Medical Center", "Healthcare", "Super Specialty Hospital",
    "Multispecialty Hospital", "Clinic & Hospital",
]

# Garage name patterns
GARAGE_PREFIXES = [
    "Maruti Authorized", "Hyundai Authorized", "Tata Motors",
    "Mahindra First Choice", "Honda Cars", "Toyota Authorized",
    "Quick Fit", "Auto Care", "Speed Motors", "Metro Auto",
    "National Auto", "City Motors", "Star Auto", "Royal Motors",
    "Prime Auto",
]

GARAGE_TYPES = ["Authorized", "Multi-brand", "Specialist"]

# Agent name patterns (common Indian names)
FIRST_NAMES = [
    "Rajesh", "Priya", "Amit", "Sunita", "Vikram", "Anita", "Suresh",
    "Deepa", "Arun", "Kavita", "Manoj", "Rekha", "Sanjay", "Meena",
    "Rahul", "Pooja", "Vivek", "Nisha", "Ajay", "Geeta", "Rohit",
    "Sneha", "Vijay", "Archana", "Nitin", "Swati", "Ashok", "Ritu",
    "Kiran", "Naveen",
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Reddy", "Nair", "Gupta",
    "Jain", "Verma", "Mehta", "Shah", "Pillai", "Iyer", "Rao",
    "Das", "Mukherjee", "Chatterjee", "Banerjee", "Desai", "Patil",
    "Kulkarni", "Joshi", "Mishra", "Pandey", "Tiwari", "Saxena",
    "Agarwal", "Bose", "Thakur", "Malhotra",
]

# Premium ranges by LOB (annual, in INR)
PREMIUM_RANGES = {
    "Health": (5000, 150000),
    "Motor": (3000, 80000),
    "Fire": (10000, 500000),
    "Marine": (15000, 300000),
    "Miscellaneous": (5000, 200000),
}

# Claim amount ranges by LOB (in INR)
CLAIM_AMOUNT_RANGES = {
    "Health": (5000, 2000000),
    "Motor": (5000, 1500000),
    "Fire": (50000, 5000000),
    "Marine": (100000, 3000000),
    "Miscellaneous": (10000, 1000000),
}

# Fraud patterns (for P4 held-out evaluation)
# These are deliberately realistic patterns that the anomaly detection should catch
FRAUD_PATTERNS = {
    "rapid_repeat": "Multiple claims from same policyholder within 30 days",
    "amount_spike": "Claim amount > 5x average for that LOB",
    "weekend_holiday": "Claim filed on weekend/holiday with immediate settlement",
    "agent_ring": "Cluster of claims through the same agent-hospital pair",
    "new_policy_claim": "Claim filed within 15 days of policy start date",
    "mismatched_lob": "Health claim routed through a garage, or motor claim through a hospital",
}
