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
            df1=pd.read_excel("output/product1_amazon.xlsx")
            st.image("https://ams3.digitaloceanspaces.com/graffica/2023/03/amazon_logo._CB633267048_.png")
            st.write("## Amazon:")
            st.image(df1.loc[1, 'Imagen'], width=300, caption='Imagen centrada', use_column_width=True)
            st.table(df1.head(5))

            scraping(make_headless,input2,"product2_amazon")
            df2=pd.read_excel("output/product2_amazon.xlsx")
            st.image(df2.loc[1, 'Imagen'])
            st.table(df2.head(5))

            scrapper("--headless", input1, "product1_ebay")
            st.image("https://ams3.digitaloceanspaces.com/graffica/2023/03/amazon_logo._CB633267048_.png")
            st.write("## Ebay:")
            st.image("https://ams3.digitaloceanspaces.com/graffica/2023/03/amazon_logo._CB633267048_.png")
            df3=pd.read_excel("output/product1_ebay.xlsx")
            st.image(df3.loc[1, 'Image'])
            st.table(df3.head(5))

            scrapper("--headless", input2, "product2_ebay")
            df4=pd.read_excel("output/product2_ebay.xlsx")
            st.image(df4.loc[1, 'Image'], width=300, caption='Imagen centrada', use_column_width=True)
            st.table(df4.head(5))

        else:
            st.write("Please enter two products to compare.")

if __name__ == "__main__":
    main()
