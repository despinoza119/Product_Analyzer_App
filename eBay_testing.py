import streamlit as st
from eBay_scrapper import scrapper


def main():
    st.title("eBay Scraper") # Title

    col1, col2 = st.columns(2)
    product_1 = col1.text_input("Enter first product name:", "") # Input box
    product_2 = col2.text_input("Enter second product name:", "") # Input box
    # headless_mode = st.checkbox("Run in headless mode", value=True)

    if st.button("Scrape eBay"): # This is the button
        with st.spinner("Scraping eBay..."):
            df1 = scrapper("--headless", product_1, "FILE")
            df2 = scrapper("--headless", product_2, "FILE")
            st.success("eBay scraped successfully for both products!")
            st.columns(2)
            col1.dataframe(df1.head(3))
            col1.image(df1.loc[1, 'Image'])
            col2.dataframe(df2.head(3))
            col2.image(df2.loc[1, 'Image'])

            # st.write(f"Product {product_name} results in eBay")
            # st.dataframe()

if __name__ == "__main__":
    main()
