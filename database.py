from google import genai
from google.genai import types
from time import sleep
#importing python package for mongodb
from pymongo import MongoClient
#AIzaSyBG_DHAOhyNX9EybV3USvUvt4l5nga5t4Y AIzaSyB1MSHiCCh0G5Nbxk49LQJUWUcaCzVFSE8
ai_client = genai.Client(api_key="AIzaSyB1MSHiCCh0G5Nbxk49LQJUWUcaCzVFSE8")
mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client["Disease_Info_Database"]
collection = db["Diseases"]

class_names_PV =["Apple___Apple_scab","Apple___Black_rot", "Apple___Cedar_apple_rust","Apple___healthy","Blueberry___healthy","Cherry_(including_sour)___Powdery_mildew","Cherry_(including_sour)___healthy",    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot","Corn_(maize)___Common_rust_",  "Corn_(maize)___Northern_Leaf_Blight","Corn_(maize)___healthy",   "Grape___Black_rot","Grape___Esca_(Black_Measles)","Grape___Leaf_blight_(Isariopsis_Leaf_Spot)","Grape___healthy ","Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot","Peach___healthy",    "Pepper,_bell___Bacterial_spot","Pepper,_bell___healthy","Potato___Early_blight",'Potato___Late_blight',  "Potato___healthy","Raspberry___healthy",   "Soybean___healthy","Squash___Powdery_mildew","Strawberry___Leaf_scorch","Strawberry___healthy",  "Tomato___Bacterial_spot","Tomato___Early_blight", "Tomato___Late_blight","Tomato___Leaf_Mold",  "Tomato___Septoria_leaf_spot","Tomato___Spider_mites_Two-spotted_spider_mite","Tomato___Target_Spot" ,"Tomato___Tomato_Yellow_Leaf_Curl_Virus","Tomato___Tomato_mosaic_virus","Tomato___healthy"] 

data = {}
languages = ["English","Hindi","Marathi"]

for language in languages:
    data[language] = {}
    for i in class_names_PV:
        Plant_Class = i.split("_")[0].strip()
        Predicted_Class = (' ').join(i.split("_")[1:]).strip()
        info_prompt = f"You have deduced that {Plant_Class} plant has the disease {Predicted_Class}. Give Information about the disease. Selected Language is {language}"
        if Plant_Class not in data[language]:
            data[language][Plant_Class] = {}
        if "health" in Predicted_Class.lower():
            info_prompt = f"You have deduced that {Plant_Class} plant is healthy. Give some information about the plant in short. Selected Language is {language}"
        response = ai_client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
            system_instruction="You are deducing whether a plant is healthy or has some disease, first line should declare plant's status(If diseased state name of disease). For Diseased plants response should consist of sections: disease overview, symptoms, causes and possible solutions. For healthy plants response should consist of sections: plant overview, common diseases, preventive measures. Put '/?#' at the beginning of each section. Make sure that the information is accurate. Use text formatting to make the content more visually appealing. Respond in the language selected.",
            max_output_tokens=1000,
            temperature=0.05),
            contents=[info_prompt]
        )
        data[language][Plant_Class][Predicted_Class] = response.text

collection.insert_one(data)
print("Data inserted successfully")
#info_prompt = f"You have deduced that Apple has the disease Apple scab. Give Information about the disease. Selected Language is Hindi"
# info_prompt = f"You have deduced that Blueberry plant is healthy. Give some information about the plant in short. Selected Language is HIndi"
# response = ai_client.models.generate_content(
#             model="gemini-2.0-flash",
#             config=types.GenerateContentConfig(
#             system_instruction="You are deducing whether a plant is healthy or has some disease, first line should declare plant's status(If diseased state name of disease). For Diseased plants response should consist of sections: disease overview, symptoms, causes and possible solutions. For healthy plants response should consist of sections: plant overview, common diseases, preventive measures. Put '/?#' at the beginning of each section. Make sure that the information is accurate. Use text formatting to make the content more visually appealing. Respond in the language selected.",
#             max_output_tokens=1000,
#             temperature=0.05),
#             contents=[info_prompt]
#         )
