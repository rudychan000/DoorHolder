import random
import json

diseases = [
    "cancer",
    "diabetes",
    "heart disease",
    "stroke",
    "asthma",
    "arthritis",
    "HIV/AIDS",
    "influenza",
]

common_medications = [
    "Acetaminophen (Paracetamol)",
    "Ibuprofen",
    "Amoxicillin",
    "Loratadine",
    "Esomeprazole",
    "Metoprolol",
    "Atorvastatin",
    "Lisinopril",
    "Metformin",
    "Omeprazole",
]

meal_styles = [
    "Vegetarian",
    "Vegan",
    "Pescatarian",
    "Carnivore (Meat-based)",
    "Mediterranean Diet",
    "Keto (Ketogenic Diet)",
    "Paleo (Paleolithic Diet)",
    "Gluten-Free",
    "Low-Carb",
    "Intermittent Fasting",
]
mood = ["Happy", "Sad", "Anxious", "Excited", "Angry", "Calm"]
frequency = [
    "Rarely",
    "Sometimes",
    "Normal",
    "Frequently",
]  # exercise, alcohol, smoking
quant = [
    "Very little",
    "little",
    "Normal",
    "High",
    "Very High",
]  # sleep, blood pressure, blood sugar, stress, cholestrol
symptoms = [
    "Fever",
    "Cough",
    "Sore throat",
    "Headache",
    "Muscle pain",
    "Joint pain",
    "Fatigue",
    "Loss of appetite",
    "Stomach pain",
    "Nausea",
    "Diarrhea",
    "Constipation",
    "Chest pain",
    "Shortness of breath",
    "Dizziness",
    "Rash",
    "Runny nose",
    "Nasal congestion",
    "Chills",
    "Blurred vision",
]

patients_feature_list = [
    "age",
    "gender",
    "height",
    "weight",
    "disease",
    "medicines",
    "diet",
    "exercise",
    "sleep",
    "alcohol",
    "smoking",
    "blood_pressure",
    "blood_sugar_levels",
    "cho_levels",
    "stress",
    "mood",
    "symptoms",
]
patients_number = 10
frequency_list = ["exercise", "alcohol", "smoking"]
big_dic = {}
for i in range(patients_number):
    dic = {}
    for x in patients_feature_list:
        if x == "age":
            dic[x] = random.randint(20, 100)
        elif x == "gender":
            dic[x] = random.choice(["male", "female"])
        elif x == "height":
            dic[x] = random.randint(150, 200)
        elif x == "weight":
            dic[x] = random.randint(40, 150)
        elif x == "disease":
            dic[x] = random.choice(diseases)
        elif x == "medicines":
            dic[x] = random.choice(common_medications)
        elif x == "diet":
            dic[x] = random.choice(meal_styles)
        elif x in frequency_list:
            dic[x] = random.choice(frequency)
        elif x == "mood":
            dic[x] = random.choice(mood)
        elif x == "symptoms":
            n = 5
            s1 = set()
            for j in range(n):
                s1.add(random.choice(symptoms))
            dic[x] = list(s1)
        else:
            dic[x] = random.choice(quant)
    big_dic[f"p{i}"] = dic

# 辞書をJSONファイルに書き込む
with open("data.json", "w") as json_file:
    json.dump(big_dic, json_file, indent=4)
