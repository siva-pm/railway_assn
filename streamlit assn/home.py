import streamlit as st
import pandas as pd

def app():
    
    with st.container():
        st.title("Manage Your Expense")    
        def load_data():
            data=pd.read_csv("/home/siva-pt7760/Downloads/myexpenses.csv")
            data['Date'] = pd.to_datetime(data['Date'], format='mixed')
            return data
        data = load_data()
        st.write("---")
        date= st.text_input("search expense by date ")  

        mod_data=data[data['Date']==date]

        if mod_data.empty:
            st.write("no data found!!! ")
        else :  
            st.dataframe(mod_data)

    with st.container():
        st.write("---")
        st.write("make an entry")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            input1 = st.date_input("date: ")

        with col2:
            input2 = st.text_input("item: ")

        with col3:
            input3 = st.text_input("amount: ")

        with col4:
            input4 = st.text_input("category: ")

        with col5:
            input5 = st.text_input("time: ")

        with col6:
            input6 = st.text_input("day: ")
        if st.button("make entry"):
            data.loc[len(data)]=[input1,input2,input3,input4,input5,input6]
            data.to_csv("/home/siva-pt7760/Downloads/myexpenses.csv",index=False)
            st.write("entry made!!!")

    with st.container():
        st.write("---")
        st.write("Suggested for you: ")
        imgc,txtc=st.columns((1,2))
        with imgc:
            st.image("/home/siva-pt7760/Pictures/Screenshots/money.png")
        with txtc:
            st.subheader("How To Manage Your Money (50/30/20 Rule)")
            st.write("In this video I present a high level overview on how to manage your money using the 50/30/20 Rule. Money management is 90% discipline and 10% knowledge. The 50/30/20 rule will force you to create a budget and understand where every single one of your after-tax dollars is going.")
            st.markdown("[watch video...](https://www.youtube.com/watch?v=HQzoZfc3GwQ)")
