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
            st.header(f"{product_1} vs {product_2}")
            st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
            c1, c2 = st.columns(2)
        # PROD 1
            c1.subheader(f"{product_1}")
            c1.image(df1.loc[1, 'Image'])
            # first price
            c1.subheader(df1.loc[1, 'Price'])
            c1.subheader(df1.loc[1, 'Condition'])
            c1.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", use_column_width=True)
            c1.dataframe(df1.head(3))
        # PROD 2
            c2.subheader(f"{product_2}")
            c2.image(df2.loc[1, 'Image'])
            # first price
            c2.subheader(df2.loc[1, 'Price'])
            c2.subheader(df2.loc[1, 'Condition'])
            c2.image("https://upload.wikimedia.org/wikipedia/commons/1/1b/EBay_logo.svg", use_column_width=True)
            c2.dataframe(df2.head(3))


            # st.write(f"Product {product_name} results in eBay")
            # st.dataframe()

if __name__ == "__main__":
    main()
