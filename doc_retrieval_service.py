import os
import boto3
import streamlit as st

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

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    try:
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=document_key)
        document_content = response["Body"].read().decode("utf-8")
        return document_content
    except Exception as ex:
        print(f"Error retrieving document: {ex}")
        return None

 
