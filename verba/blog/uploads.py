from flask import flash, request, redirect
import boto3
import random
import string


s3 = boto3.client('s3')
chars = string.digits + string.ascii_letters

class Upload:
    def __init__(self) -> None:
        pass

    def allowed_files(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'webp']
    
    def random_filename():
        filename = ''.join(random.choice(chars) for i in range(8))
        return filename

    def upload_file(self):
        if 'file' not in request.files:
            error = 'No file part'
            return error
        file = request.files['file']

        if file.filename == "":
            return
        elif file and self.allowed_files(file.filename):
            filename = self.random_filename()
            s3.put_object(Bucket='verba-post-images', Key=filename, Body=file.stream, ContentType=file.content_type)
            location = s3.get_bucket_location(Bucket='verba-post-images')['LocationConstraint']
            region = '' if location is None else f'{location}'
            image_url = f"https://verba-post-images.s3.{region}.amazonaws.com/{filename}"
        return image_url
    
    def delete_file(image_url):
        image_url = image_url.split("://")[1].split("/")[1]
        s3.delete_object(Bucket='verba-post-images', Key=image_url)