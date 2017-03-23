#!/usr/bin/env python
import os, boto3, StringIO
from PIL import Image, ImageDraw, ImageFont
import config

s3 = boto3.client('s3')


################################################################################
### AWS Event handlers
################################################################################

def watermark(event, context):
    """
    Receives an S3 event record for a newly created object, downloads the object 
    to the lambda's filesystem, adds a watermark to it, and uploads it to another bucket.
    """

    bucket, key = unwrap_bucket_key_from(event)
    extension = key.split('.')[-1].lower()  # File extension of object

    if extension not in config.ALLOWED_EXTENSIONS:  # Abort early due to unsupported file extension
        print('extension {} not allowed'.format(extension))
        return False

    local_file = cache_original(bucket, key)

    watermarked_io = watermark_image(local_file, 'Welcome to WAPRO')
    upload_io(watermarked_io, config.OUT_BUCKET, key)

    return True


################################################################################
### Utility functions
################################################################################


def watermark_image(original, watermark_text):
    main_image = Image.open(original)
    draw = ImageDraw.Draw(main_image)

    # Scale text to width of image
    img_fraction = 0.80

    font_path = os.path.join(config.PARENT_DIRECTORY, 'static', 'Arial.ttf')
    font_size = 1  # starting font size
    font = ImageFont.truetype(font_path, font_size)

    while font.getsize(watermark_text)[0] < img_fraction * main_image.size[0]:
        # iterate until the text size is just larger than the criteria
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)

    font_size -= 1
    font = ImageFont.truetype(font_path, font_size)

    draw.text((10, 10), watermark_text, font=font) # put the text on the image

    io = StringIO.StringIO()
    main_image.save(io, 'JPEG')  # Save Image instance to StringIO, to avoid writing to disk
    io.seek(0)  # Seek back to 0th byte for good measure
    return io


def unwrap_bucket_key_from(event):
    bucket = event['Records'][0]['s3']['bucket']['name']  # Bucket where object was created
    key = event['Records'][0]['s3']['object']['key']  # Key (relpath) of object in bucket
    return bucket, key


def cache_original(bucket, key):
    path = os.path.join('/tmp/', key)
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    s3.download_file(bucket, key, path)
    return path


def upload_io(iostream, bucket, key):
    s3.upload_fileobj(iostream, bucket, key)
    return True
