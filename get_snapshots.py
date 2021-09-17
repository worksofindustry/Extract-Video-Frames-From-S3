import boto3, cv2, os
from typing import List

def get_presigned_url(bucket, key, expr, s3_client):
    """generates presigned url to make GET request from S3"""
    url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': key}, ExpiresIn = expr)
    return url

def upload_s3(boto_connection, bucket, key, data):
    boto_connection.put_object(Body=data, Bucket=bucket, 
                Key=key, ContentType='image/jpeg', ACL='public-read',
                StorageClass='REDUCED_REDUNDANCY')

def extract_frames(frames_to_keep: List[int], url, boto_connection, bucket, s3_folder='') -> None:
    """frames_to_keep: list, url: video file location on s3, boto_connection: client conn, s3_folder: dir on s3, bucket: dest bucket"""
    count: int = 0
    filebase_name,_=os.path.basename(url).split('?')
    cap = cv2.VideoCapture(url)
    success,frame = cap.read()
    while success:
        if count in frames_to_keep:
            generated_key = s3_folder + filebase_name + "_" "%d.jpg" % count
            image_string = cv2.imencode('.jpeg', frame)[1].tobytes()
            upload_s3(boto_connection=boto_connection, bucket=bucket, key=generated_key, data=image_string)
            print("Uploading:", generated_key)
        success,_ = cap.read()
        count += 1




if __name__ == "__main__":
    test = [150,2264] #list of frames to extract from the video
    s3_client = boto3.client('s3')
    key = 'videos/2021/8B49-0782-DF75-A32B0924C3CB_4.mp4'
    item_url = get_presigned_url('my-video-bucket', key, 600, s3_client)
    print(item_url)
    extract_frames(frames_to_keep=test, url=item_url, bucket='my-image-bucket', boto_connection=s3_client, s3_folder='optional')
   