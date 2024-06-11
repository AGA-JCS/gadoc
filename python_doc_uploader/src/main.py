import os

import streamlit as st
from google.cloud import storage

from config import bucket_name, folder_name

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/appadmin/app/src/service-account.json"


# Funcion para subir los archivos al bucket
def upload_to_gcs(bucket_name, folder_name, file, concatenated_name):
    client = storage.Client()  # Dejar en blanco
    bucket = client.bucket(bucket_name)  # Definimos bucket
    blob = bucket.blob(f"{folder_name}/{concatenated_name}")  # Definimos path con nombre concatenado
    blob.upload_from_string(file.getvalue(), content_type=file.type)  # Subimos archivo
    return f"Archivo {concatenated_name} subido a {bucket_name}."


# Streamlit app
st.title("Streamlit Vanda")

# Elemento de streamlit para crear un menu de subida de archivos
uploaded_file = st.file_uploader("Choose a file")

# Campo de texto para que el usuario ingrese el número de despacho
numero_despacho = st.text_input("Numero Despacho")

# Elemento de streamlit para crear un caja de selección
options_dict = {"BL": "Bill of Lading", "FA": "Factura", "CO": "Certificado de Origen"}
# Invertir el diccionario para obtener los valores legibles
options_list = list(options_dict.values())
option = st.selectbox("Select an option", options_list)

if st.button("Submit"):
    if uploaded_file is not None:
        nombre_archivo = uploaded_file.name
        # Obtener la clave correspondiente al valor seleccionado
        option_key = next(key for key, value in options_dict.items() if value == option)
        concatenado = f"{numero_despacho}_{option_key}_{nombre_archivo}"
        # st.write("Nombre concatenado:", concatenado)

        # Subimos archivos a Cloud Storage
        result = upload_to_gcs(bucket_name, folder_name, uploaded_file, concatenado)
        st.success(result)

        # Llamamos la Gemini API con los parámetros:
        # bucket_name and folder_name ---> para poder referenciar el documento subido a Cloud Storage
        # option ---> variable que guarda el valor del select box
        # response = f"Función no implementada aún"
        # st.markdown(response)

    else:
        st.error("Please upload a file first.")


def main():
    print("Python doc uploader")


if __name__ == "__main__":
    main()
