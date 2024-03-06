import streamlit as st
import pandas as pd
import time
from youtube import obtain_transcript
from resume import compare_products
from youtube import return_summary
from amazon_scrapper import scraping

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

            # Display result as a paragraph in one page
            st.write("## Comparison of products:")
            st.write(result)
            tiempoInicio = time.time()

            make_headless = True

            scraping(make_headless, input1, "product1")
            scraping(make_headless, input2, "product2")

            # Display tables in another page
            st.write("## Amazon Prices:")
            st.write(f"### {input1}:")
            st.table(pd.read_excel("output/product1.xlsx"))
            st.write(f"### {input2}:")
            st.table(pd.read_excel("output/product2.xlsx"))

        else:
            st.write("Please enter two products to compare.")

if __name__ == "__main__":
    main()
