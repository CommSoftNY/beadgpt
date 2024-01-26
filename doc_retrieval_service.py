import os
import boto3
import streamlit as st
import json

# variables & aws credentials
aws_access_key = st.secrets["AWS_ACCESS_KEY"]
aws_secret_key = st.secrets["AWS_SECRET_KEY"]
aws_region = st.secrets["AWS_REGION"]
s3_bucket_name = st.secrets["S3_BUCKET_NAME"]
document_key = ""

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
    
    print("Connecting to the S3 Repository")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    print(f"Attempting to retrieve the document: {document_id} ")

    try:
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=document_key)

        if response is response.IfNoneMatch:
            print(f"The document: {document_id} could not be found.")
            return None
        else:
            print(f"The document: {document_id} was retrieved")
            document_content = response["Body"].read().decode("utf-8")
        return document_content
    except Exception as ex:
        print(f"Error retrieving document: {ex}")
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
            print(f"The response object title is : ", title)
            pdf_titles.append(title)
        return pdf_titles
    except Exception as ex:
        print(f"Error retrieving document titles: {ex}")
        return None