
from setuptools import setup

setup(name='s3_utils',
      version='0.1',
      description='Tools for saving matplotlib figures and files to S3',
      author='Bogdan Buduroiu',
      packages=['s3'],
      install_requires=[
            'boto3'
      ],
      zip_safe=False)
