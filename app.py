import streamlit as st
from youtube import obtain_transcript
from resume import compare_products
from youtube import return_summary

def main():
    st.title("Product Comparison")

    input1 = st.text_input("Enter the first product:", "")
    input2 = st.text_input("Enter the second product:", "")

    if input1 and input2:
        obtain_transcript(input1,input2)
        result =compare_products()
        #result = return_summary(input1,input2)
        st.write(f"{result}")
    else:
        st.write("Please enter two products to compare.")

if __name__ == "__main__":
    main()
