import io
import os

import boto3

def save_fig(fig, s3_file_key='untitled.png', s3_bucket=None):
    '''Saves a matplotlib.pyplot.figure as a PNG image 
    to a specified file in an S3 bucket.

    User must have their access and secret keys stored as environment 
    variables.

    # Arguments:
        fig: matplotlib figure to save
        s3_file_key: full path to save location on aws
        s3_bucket: name of the S3 bucket to receive the file

    # Examples:
        fig = plt.figure()
        save_fig(fig, s3_file_key='folder1/folder2/file.png', s3_bucket='bucket-name')
    '''
    if not s3_bucket:
        raise Exception('You must specify an S3 bucket to save to.')

    img_data = io.BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    s3.put_object(
        Body=img_data,
        Bucket=s3_bucket,
        ContentType='image/png',
        Key=s3_file_key
    )


def save_file(local_file_path, s3_file_key='results/anodcgan', s3_bucket=None):
    '''Saves a generic file to an S3 bucket.

    User must have their access and secret keys stored as environment 
    variables.

    # Arguments:
        local_file_path: local location of the file
        s3_file_key: full path to save location on S3
        s3_bucket: name of the S3 bucket to receive the file

    # Examples:
        save_file('/path/to/file/file.txt', s3_file_key='folder1/folder2/file.txt', s3_bucket='bucket-name')
    '''
    if not s3_bucket:
        raise Exception('You must specify an S3 bucket to save to.')

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    s3.put_object(
        Body=open(local_file_path, 'rb'),
        Bucket=s3_bucket,
        ContentType='image/png',
        Key=s3_file_key
    )


def get_all_files(s3_folder_key, destination='.', s3_bucket=None):
    '''Retrieves all files from an S3 bucket folder to a specified destination.

    User must have their access and secret keys stored as environment 
    variables.

    # Arguments:
        s3_folder_key: full path of the s3 folder
        destination: local destination of the files
        s3_bucket: name of the S3 bucket to receive the file

    # Examples:
        get_all_files('s3/path/to/folder', destination='local/destination', s3_bucket='bucket-name')
    '''
    if not s3_bucket:
        raise Exception('You must specify an S3 bucket to save to.')

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    list_s3_files = s3.list_objects(
        Bucket=s3_bucket,
        Prefix=s3_folder_key
    )

    for file in list_s3_files['Contents']:
        file_obj = s3.get_object(
            Bucket=s3_bucket,
            Key=file['Key']
        )
        file_body = file_obj['Body']
        with io.FileIO(os.path.join(destination, file['Key'].split('/')[-1]), 'w') as file:
            for b in file_body._raw_stream:
                file.write(b)


def get_file(s3_file_key, destination='file', s3_bucket=None):
    '''Retrieves all files from an S3 bucket folder to a specified destination.

    User must have their access and secret keys stored as environment 
    variables.

    # Arguments:
        s3_folder_key: full path of the s3 folder
        destination: local destination of the files
        s3_bucket: name of the S3 bucket to receive the file

    # Examples:
        get_file('s3/path/to/file.txt', destination='local/destination/file.txt', s3_bucket='bucket-name')
    '''
    if not s3_bucket:
        raise Exception('You must specify an S3 bucket to save to.')

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    file_obj = s3.get_object(
        Bucket=s3_bucket,
        Key=s3_file_key
    )

    file_body = file_obj['Body']
    with io.FileIO(destination, 'w') as file:
        for b in file_body._raw_stream:
            file.write(b)

    return os.path.abspath(destination)