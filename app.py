import streamlit as st
import pandas as pd
import time as time
from youtube import obtain_transcript
from resume import compare_products
from youtube import return_summary
from tools import scraping

def main():
    st.title("Product Comparison")

    # Configurar el diseño en dos columnas
    col1, col2 = st.columns(2)

    # Input para el primer producto en la primera columna
    input1 = col1.text_input("Enter the first product:", "")

    # Input para el segundo producto en la segunda columna
    input2 = col2.text_input("Enter the second product:", "")

    # Botón para comparar productos debajo de los inputs
    if st.button("Compare Products"):
        if input1 and input2:
            obtain_transcript(input1, input2)
            result = compare_products()

            tiempoInicio = time.time()

            make_headless = True
        
            scraping(make_headless,input1,"product1")
            scraping(make_headless,input2,"product2")

            df1=pd.read_excel("output/product1.xlsx")
            df2=pd.read_excel("output/product2.xlsx")
            st.table(df1)
            st.table(df2)

            # Dividir el resultado en dos partes en el primer *
            result_parts = result.split('-----')
            if len(result_parts) > 1:
                col1.write(f"{result_parts[0]}")
                col2.write(f"{result_parts[1]}")
            else:
                st.write("Error in processing the result.")
        else:
            st.write("Please enter two products to compare.")

if __name__ == "__main__":
    main()
