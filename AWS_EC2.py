import boto3
import sys

def amazon_upload() :
    ACCESS_KEY  = "AKIASIBKFBZCIDVBYVOH" 
    ACCESS_TYPE = "t2.micro"
    SECRET_ACCESS_KEY = "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"
    ec2_client = boto3.client('ec2', region_name = 'ap-northeast-2', aws_access_key_id =ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY)
    response = ec2_client.describe_instances()
    instances = response['Reservations']
    instance_ids = []

    for instance in instances:
        instance_ids.append(instance['Instances'][0]['InstanceId'])

    tage_creation = ec2_client.create_tags(

            Resources =
                instance_ids,
            Tags = [
                {
                    'Key' : 'Changman',
                    'Value' : 'hi',
                    'Key' : 'Operation',
                    'Value' : 'Start',
                    'Key' : 'Name',
                    'Value' : 'CHANG',
                }
                ]
            )

    print(instances)