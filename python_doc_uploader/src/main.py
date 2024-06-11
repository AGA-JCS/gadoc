import streamlit as st

# Streamlit app
st.title("Streamlit Vanda")

# Elemento de streamlit para crear un menu de subida de archivos
uploaded_file = st.file_uploader("Choose a file")

# Elemento de streamlit para crear un caja de selección
option = st.selectbox("Select an option", ("BL", "Factura", "Certificado de Origen"))

if st.button("Submit"):
    if uploaded_file is not None:
        # Subimos archivos a Cloud Storage
        result = f"Función no implementada aún"
        st.success(result)

        # Llamamos la Gemini API con los parámetros:
        # bucket_name and folder_name ---> para poder referenciar el documento subido a Cloud Storage
        # option ---> variable que guarda el valor del select box
        response = f"Función no implementada aún"
        st.markdown(response)

    else:
        st.error("Please upload a file first.")


def main():
    print("Python doc uploader")


if __name__ == "__main__":
    main()
