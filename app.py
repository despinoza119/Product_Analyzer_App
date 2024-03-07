import streamlit as st
import pandas as pd
import time as time
from youtube import obtain_transcript
from resume import compare_products
from youtube import return_summary
from amazon_scrapper import scraping
from eBay_scrapper import scrapper

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
            st.write(result)

            tiempoInicio = time.time()
            make_headless = True
            scraping(make_headless,input1,"product1_amazon")
            scraping(make_headless,input2,"product2_amazon")
            df1=pd.read_excel("output/product1_amazon.xlsx")
            df1.reset_index(drop=True, inplace=True)

            df2=pd.read_excel("output/product2_amazon.xlsx")
            df2.reset_index(drop=True, inplace=True)

            col1, col2 = st.columns(2)
            col1.subheader(f"{input1}")
            col1.image(df1.loc[1, 'Imagen'])
            col1.subheader(df1.loc[1, 'Precio'])
            col1.subheader(df1.loc[1, 'Calificacion'])
            col1.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=150)
            col1.dataframe(df1.head(5))

            col2.subheader(f"{input1}")
            col2.image(df2.loc[1, 'Imagen'])
            col2.subheader(df1.loc[1, 'Precio'])
            col2.subheader(df1.loc[1, 'Calificacion'])
            col2.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=150)
            col2.dataframe(df2.head(5))

            scrapper("--headless", input1, "product1_ebay")
            scrapper("--headless", input2, "product2_ebay")
            df3=pd.read_excel("output/product1_ebay.xlsx")
            df3.reset_index(drop=True, inplace=True)

            df4=pd.read_excel("output/product2_ebay.xlsx")
            df4.reset_index(drop=True, inplace=True)

            col1.subheader(f"{input1}")
            col1.image(df3.loc[1, 'Image'])
            col1.subheader(df3.loc[1, 'Price'])
            col1.subheader(df3.loc[1, 'Condition'])
            col1.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=150)
            col1.dataframe(df3.head(5))

            col2.subheader(f"{input2}")
            col2.image(df4.loc[1, 'Image'])
            col2.subheader(df4.loc[1, 'Price'])
            col2.subheader(df4.loc[1, 'Condition'])
            col2.dataframe(df4.head(5))

        else:
            st.write("Please enter two products to compare.")

if __name__ == "__main__":
    #show_ebay_section = st.sidebar.checkbox("Show eBay Section")
    main()
