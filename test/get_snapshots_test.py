import boto3, pytest, sys
sys.path.append("..") # doing this because yeah, Windows 🖕
from get_snapshots import get_presigned_url, upload_s3, extract_frames
from conftest import MyS3Client

#tempfile module creates temporary files and dirs, and are automatically cleaned up
from tempfile import NamedTemporaryFile

#testing
def test_list_objects(s3_client, s3_test) -> None:
    file_text = "test"
    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        with open(tmp.name, "w", encoding="UTF-8") as f:
            f.write(file_text)

        s3_client.upload_file(tmp.name, "my-test-bucket", "file12")
        s3_client.upload_file(tmp.name, "my-test-bucket", "file22")

    my_client = MyS3Client()
    objects = my_client.list_objects(bucket_name="my-test-bucket", prefix="file1")
    assert objects == ["file12"]


import requests
from requests import RequestException

def test_get_presigned_url_fakebucket(s3_client) -> None:
    created_url = get_presigned_url('fakebucket', 'fake/dir/test.mp4', 100, s3_client) != None
    try:
        print("Status Code:", requests.head(created_url).status_code)
        assert requests.head(created_url).status_code <400
    except RequestException as e:
        print("Exception Error, Invalid Address:", e)