import streamlit as st
import tensorflow as tf
import numpy as np
import json as js

models = {"MobileNetV2FT": "PPD_MobileNetV2_FT.keras", "MobileNetV2":"Plant_Disease_Model_MobileNetV2_Default.keras", "NPDDCustom":"NPDDCustom_model.keras","ResNet50":"PPD_ResNet50.keras","MNV_Plant_Village":"Plant_Disease_Model_PlantVillageAugmented.keras"}
#Input for model
def model_predictions(test_image, model1 = 'NPDDCustom'):
    model = tf.keras.models.load_model(models[model1])
    input_image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    if model1 in ["MobileNetV2FT", "ResNet50"]:
        #Resizing image to 256x256
        input_image = tf.image.resize(input_image, (256,256))
    elif model1 == "MobileNetV2":
        #Resizing image to 224x224
        input_image = tf.image.resize(input_image, (224,224))
    input_arr = np.array([tf.keras.preprocessing.image.img_to_array(input_image)])
    predictions = model.predict(input_arr)
    return_index =  np.argmax(predictions)
    return return_index

#Changing layout of the page
st.set_page_config(page_title="Plant Disease Detection", page_icon="🌿", layout="wide")
st.markdown(
    """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    """,
    unsafe_allow_html=True
)
#Make an about page that is clickable
class_names_NPDD = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
class_names_PV =["Apple___Apple_scab","Apple___Black_rot", "Apple___Cedar_apple_rust","Apple___healthy","Blueberry___healthy","Cherry_(including_sour)___Powdery_mildew","Cherry_(including_sour)___healthy",    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot","Corn_(maize)___Common_rust_",  "Corn_(maize)___Northern_Leaf_Blight","Corn_(maize)___healthy",   "Grape___Black_rot","Grape___Esca_(Black_Measles)","Grape___Leaf_blight_(Isariopsis_Leaf_Spot)","Grape___healthy ","Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot","Peach___healthy",    "Pepper,_bell___Bacterial_spot","Pepper,_bell___healthy","Potato___Early_blight",'Potato___Late_blight',  "Potato___healthy","Raspberry___healthy",   "Soybean___healthy","Squash___Powdery_mildew","Strawberry___Leaf_scorch","Strawberry___healthy",  "Tomato___Bacterial_spot","Tomato___Early_blight", "Tomato___Late_blight","Tomato___Leaf_Mold",  "Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot" ,"Tomato___Tomato_Yellow_Leaf_Curl_Virus","Tomato___Tomato_mosaic_virus","Tomato___healthy"] 

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Resources"])

if page == "Home":
    st.title("Plant Disease Detection")
    st.write("Welcome to the Home Page!")
    
    model = st.sidebar.selectbox("Model", ["MobileNetV2FT", "NPDDCustom","MNV_Plant_Village"])
    language = st.sidebar.selectbox("Language", ["English", "Hindi", "Marathi"])
    image_file = st.file_uploader("Upload a leaf image", type=["jpg", "png"])
    if image_file is not None:
        returned = model_predictions(image_file, model)
        col_1, col_2, col_3 = st.columns([1, 1,1])
        with col_2:
            st.image(image_file, caption="Uploaded Image", use_container_width=True)
        
            Plant_Class = class_names_PV[returned].split("_")[0].strip()
            Predicted_Class = (' ').join(class_names_PV[returned].split("_")[1:]).strip()
            st.write(f"{Plant_Class}: {Predicted_Class}")

        if "healthy" in Predicted_Class:
            info_prompt = f"""Give Information about the plant {Plant_Class}"""
        else:
            info_prompt = f"""Give Information about disease {Predicted_Class} and how it affects the plant {Plant_Class}"""
        
        #Loading json file
        with open("Disease_Info_Database.Diseases.json", "r", encoding="utf-8") as f:
            disease_info = js.load(f)
        
        response = disease_info[0][language][Plant_Class][Predicted_Class]
        responses = response.split("/?#")
        if "healthy" in Predicted_Class:
            st.subheader(f"The {Plant_Class} Plant is Healthy")
            st.write(responses[1])
            st.expander("Common Diseases", expanded=False).write(responses[2])
            st.expander("Preventive Measures", expanded=False).write(responses[3])
        else:
            st.subheader(f"The {Plant_Class} Plant is suffering from {Predicted_Class} Diseas")
            st.write(responses[1])
            st.expander("Symptons", expanded=False).write(responses[2])
            st.expander("Causes", expanded=False).write(responses[3])
            st.expander("Solutions", expanded=False).write(responses[4])
    else:
        st.write("Upload an image to get started!")
elif page == "About":
    st.title("About Us", )
    st.write("We are PBL group 4 from F13. ")

elif page == "Resources":
    st.title("Resources")
    st.markdown("Resources for Plant Disease Detection")
    st.markdown(f"""<h6>PlantVillage Dataset {class_names_PV}</h6>""")
