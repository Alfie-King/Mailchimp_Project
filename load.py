import os
import boto3
import sys
from dotenv import load_dotenv

def load():

    load_dotenv()
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket = os.getenv('bucket')
    s3_client = boto3.client(
        's3'
        , aws_access_key_id=aws_access_key
        , aws_secret_access_key=aws_secret_key
    )

    try:
        dir = 'data'
        files = [f for f in os.listdir(dir) if f.endswith('.json')]
        if files:
            for f in files:
                filename = f"{dir}/{f}"
                s3filename = f
                if "campaigns" in filename:
                    try:
                        s3_client.upload_file(filename, bucket, f"campaigns/{s3filename}")
                        os.remove(filename)
                        print(f"{filename} deleted")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                elif "list" in filename:
                    try:
                        s3_client.upload_file(filename, bucket, f"list/{s3filename}")
                        os.remove(filename)
                        print(f"{filename} deleted")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
        else:
            print("No files to upload")
    except Exception as e:
        print(e)
        raise e