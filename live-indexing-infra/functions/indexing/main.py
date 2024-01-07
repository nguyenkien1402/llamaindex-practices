## main function of AWS Lambda function
import llama_index
from llama_index import download_loader
import boto3
import json
import urllib.parse
from llama_index import SimpleDirectoryReader


def main(event, context):
    # extracting s3 bucket and key information from SQS message
    print(event)
    s3_info = json.loads(event['Records'][0]['body'])
    bucket_name = s3_info['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(s3_info['Records'][0]['s3']['object']['key'], encoding='utf-8')

    
    try:
        # the first approach to rea =d the content of uploaded file. 
        S3Reader = download_loader("S3Reader", custom_path='/tmp/llamahub_modules')
        loader = S3Reader(bucket=bucket_name, key=object_key)
        documents = loader.load_data()

        # the second approach to read the content of uploaded file
        # Creating an S3 client
        # s3_client = boto3.client('s3')
        # response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        # file_content  = response['Body'].read().decode('utf-8')
        # save the file content to /tmp folder
        # tmp_file_path = f"/tmp/{object_key.split('/')[-1]}"
        # with open(tmp_file_path, "w") as f:
        #     tmp_file_path.write(file_content)
        # reader = SimpleDirectoryReader(input_files=tmp_file_path)
        # doc = reader.load_data()
        # print(f"Loaded {len(doc)} doc")

        ## TODO
        # ReIndex or Create New Index from document
        # Update or Insert into VectoDatabase
        # (Optional) Update or Insert into DocStorage DB
        # Update or Insert index to MongoDB
        # Can have Ingestion Pipeline with Redis Cache
        
        return {
            'statusCode': 200
        }
        
    #     # creating an index 
    except Exception as e:
        print(f"Error reading the file {object_key}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error reading the file')
        }