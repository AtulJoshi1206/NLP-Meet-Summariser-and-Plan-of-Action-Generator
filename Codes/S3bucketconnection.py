import boto3
import os

# Set AWS credentials as environment variables (for debugging purposes)
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# Retrieve credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Print the credentials to verify they are being set (for debugging)
print(f'AWS_ACCESS_KEY_ID: {aws_access_key_id}')
print(f'AWS_SECRET_ACCESS_KEY: {aws_secret_access_key}')

# Create a session using the environment variables
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='ap-south-1'
)

s3 = session.resource('s3')

bucket_name = ''
folder_name = 'Atul_Joshi/'

# Create the folder by uploading a zero-byte object with the folder name
bucket = s3.Bucket(bucket_name)

try:
    bucket.put_object(Key=folder_name)
    print(f'Folder {folder_name} created successfully in bucket {bucket_name}.')
except Exception as e:
    print(f'Error creating folder {folder_name} in bucket {bucket_name}: {e}')

s3_client = session.client('s3')

# File details
files = {
    'video.mp4': "D:\Study material\Python\Infosys_Internship\A one minute TEDx Talk for the digital age _ Woody Roseland _ TEDxMileHigh.mp4",

}

# Upload the files to the folder
for file_name, file_path in files.items():
    if os.path.exists(file_path):
        try:
            s3_client.upload_file(file_path, bucket_name, folder_name + file_name)
            print(f'File {file_name} uploaded successfully to {folder_name} in bucket {bucket_name}.')
        except Exception as e:
            print(f'Error uploading file {file_name} to {folder_name} in bucket {bucket_name}: {e}')
    else:
        print(f'File {file_path} does not exist. Skipping upload.')

# List objects in the Atul_Joshi folder
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    if 'Contents' in response:
        print(f'Objects in {folder_name} folder in bucket {bucket_name}:')
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print(f'No objects found in {folder_name} folder in bucket {bucket_name}.')
except Exception as e:
    print(f'Error listing objects in {folder_name} folder in bucket {bucket_name}: {e}')

