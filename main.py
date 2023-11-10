import logging
import boto3
from datetime import datetime, timedelta
from src import app
import os

TABLE_NAME= os.environ["TABLE_NAME_1"]
BUCKET_NAME= os.environ["BUCKET_NAME"]
REGION = os.environ['REGION']

logger=logging.getLogger()
logger.setLevel(logging.INFO)

current_datetime = datetime.now()
tomorrow_datetime = current_datetime + timedelta(days=1)
# Set the time component to 9:00 AM
tomorrow_datetime = tomorrow_datetime.replace(hour=9, minute=0, second=0, microsecond=0)

tomorrow_time_str = tomorrow_datetime.strftime("%Y-%m-%dT%H:%M:%S+08:00")
sms_blast_date = tomorrow_datetime.strftime("%d-%m-%Y")

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3", region_name=REGION)

object_key = f'Hana SMS Blast/SMS_Blast_{sms_blast_date}.xlsx'

def main(event, context):

    logger.info("Event : {}".format(event))
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    input_file = app.get_file_from_s3(s3_client, BUCKET_NAME, object_key)
    
    num_of_sheets = 9
    initialTimestamp = tomorrow_time_str

    split_batches = app.split_numbers(input_file, num_of_sheets)
    app.hourUpload(table, initialTimestamp,split_batches)