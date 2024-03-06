import streamlit as st
from eBay_scrapper import scrapper

def main():
    st.title("Amazon Scraper test")

    product_name = st.text_input("Enter a product name:", "")
    #headless_mode = st.checkbox("Run in headless mode", value=True)

    if st.button("Scrape Amazon"):
        with st.spinner("Scraping Amazon..."):
            scrapper("--headless", product_name, "FILE")
            st.success("eBay scraped successfully!")

            #st.write(f"Product {product_name} results in eBay")
            #st.dataframe()

if __name__ == "__main__":
    main()
