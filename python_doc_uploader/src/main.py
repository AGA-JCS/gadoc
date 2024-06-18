import os

import requests
import streamlit as st
from google.cloud import storage

from config import bucket_name

# streamlit run src/main.py

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/appadmin/app/src/service-account.json"


# Funcion para subir los archivos al bucket
def upload_to_gcs(bucket_name, folder_name, file, concatenated_name):
    client = storage.Client()  # Dejar en blanco
    bucket = client.bucket(bucket_name)  # Definimos bucket
    # Verificar si la carpeta existe y crearla si no existe
    if not bucket.blob(f"{folder_name}/").exists():
        bucket.blob(f"{folder_name}/").upload_from_string("")  # Crear el directorio

    blob = bucket.blob(f"{folder_name}/{concatenated_name}")  # Definimos path con nombre concatenado
    blob.upload_from_string(file.getvalue(), content_type=file.type)  # Subimos archivo
    # return f"Archivo {concatenated_name} subido a {bucket_name}."
    return f"Archivo {concatenated_name} subido a {bucket_name}/{folder_name}.", blob


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
        # Crear el folder_name basado en el numero_despacho
        folder_name = numero_despacho

        # Subimos archivos a Cloud Storage
        result, blob = upload_to_gcs(bucket_name, folder_name, uploaded_file, concatenado)
        st.success(result)

        # Datos a enviar a la API
        data = {
            "numero_despacho": numero_despacho,
            "option_key": option_key,
            "concatenado": concatenado,
            "full_path": f"gs://{bucket_name}/{blob.name}",
        }
        print(f"Data= {data}")

        # URL de la API
        api_url = "http://localhost:8000/endpoint"
        # Realiza la solicitud POST a la API
        response = requests.post(api_url, json=data)
        # Verifica la respuesta de la API
        if response.status_code == 200:
            st.success("Datos enviados correctamente a la API.")
        else:
            st.error(f"Error al enviar datos a la API: {response.status_code}")

    else:
        st.error("Please upload a file first.")


def main():
    print("Python doc uploader")


if __name__ == "__main__":
    main()
