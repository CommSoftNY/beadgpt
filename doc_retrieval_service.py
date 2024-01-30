import os
import boto3
import streamlit as st
import json
from PyPDF2 import PdfReader
from io import BytesIO

# variables & aws credentials
aws_access_key = st.secrets["AWS_ACCESS_KEY"]
aws_secret_key = st.secrets["AWS_SECRET_KEY"]
aws_region = st.secrets["AWS_REGION"]
s3_bucket_name = st.secrets["S3_BUCKET_NAME"]
#document_key = ""
document_title = ""

#external database source
#retrieve document by document name from aws bucket
def retrieve_document(document_id):

    """
    Retrieve a document from amazon s3 bucket

    parameters:
    - document_id (string): The name of the document. Possibly int but we will most likely be searching for it by name

    returns:
    - str: The document details (title and context for the ai to read and reference)
    """
    #variables
    text = ""

    print("Connecting to the S3 Repository")
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    print(f"Attempting to retrieve the document: {document_id} ")

    try:
        #gets single object by name from s-3bucket
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=document_id)
        
        print(f'The single document retrieval response is: {response}')

        #checks if response is no empty and if the response object is found
        if response is None and response.Body is None:
            print(f"The document: {document_id} could not be found.")
            return None
        else:
            print(f"The document: {document_id} was retrieved")
            #reads the object
            fs = response['Body'].read()
            reader = PdfReader(BytesIO(fs))            
            
            #reads each page
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # checking if page_text is not None or empty string
                    print("reading pages")
                    text += page_text
                else:
                    print(f"Failed to extract text from a page in {reader}")
            print(f"This is the pdf text: {text}")
            return text
    except Exception as ex:
        print(f"Error rendering document: {ex}")
        return None

 
#Retrieve all document names from repo
def retrieve_all_document_titles():
    #get array of string: titles from repo
    """
    Retrieve all document titles from amazon s3 bucket

    returns:
    - str: The document details (title)
    """

    pdf_titles = []
    
    print("Connecting to the S3 Repository")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    print(f"Attempting to retrieve all document titles from repo")

    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        for bucket_object in response['Contents']:
            title = bucket_object['Key']
            pdf_titles.append(title)
        return pdf_titles
    except Exception as ex:
        print(f"Error retrieving document titles: {ex}")
        return None
