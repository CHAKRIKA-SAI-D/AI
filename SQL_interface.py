import google.generativeai as genai
import streamlit as st
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import pymysql


st.title('AI-Powered Data Query Interface')
st.write('Enter your SQL query about client data:')
api_key="" # Replace with your gemini api
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')
persona = """ you are data-dynamo bot. Your job is this
give me only sql commands where i will ask you in natural language is it okay?
give me without any `` i just need query that's enough
give me correct sql syntax
if any unnecesary things asked  or unrelated questions are asked by user simply say this : 1
"""

persona2=""" 
this is the question 
you just give me explnation of output below provided with respect to question in 2 sentences maximum
"""
question=st.text_input("Ask me Anything  !!")
if st.button("Ask",use_container_width=400):
    if question and question!="":
        ##prompting the gpt
        prompt=persona + "So here is the user want : "+question
        responce=model.generate_content(prompt)

        # st.write(responce.text)
        if(responce.text.strip() == '1' or responce.text.strip() == 1):
            st.write("Please describe your requirement in more precise way :)")
        else:
            endpoint =''  # Replace with your Azure Text Analytics endpoint
            api_key = ''  # Replace with your Azure Text Analytics API key

            # Initialize the Text Analytics client
            text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

            # Function to query the MySQL database
            def query_database(query):
                connection = pymysql.connect(
                    host='',  # Adjust with your MySQL server details
                    user='',
                    password='',
                    database=''
                )
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                connection.close()
                return result

            # Function to analyze text using Azure Text Analytics
            def analyze_text(text):
                response = text_analytics_client.extract_key_phrases(documents=[text])
                return response[0].key_phrases

            # Streamlit UI

            # user_query = st.text_input('Query')
            user_query=responce.text
            if user_query:
                try:
                    # Query the database
                    db_response = query_database(user_query)

                    # Format the database response for analysis
                    response_text = f"Data: {db_response} Query: {user_query}"
                    key_phrases = analyze_text(response_text)

                    st.write('Database Response:')
                    st.write(db_response)

                    st.header(" Short Explanation: ")
                    prompt2=question+persona2+ str(db_response)
                    responce2=model.generate_content(prompt2)
                    st.write(responce2.text)

                except Exception as e:
                    st.write(f"Error: {e}")

                else:
                    pass
