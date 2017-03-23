import os


################################################################################
### Project
################################################################################

PROJECT_NAME = 'lambda-watermark'


################################################################################
### Environment
################################################################################

ENV = dict(os.environ)
if ENV.get('STAGE'):
    URL_PREFIX = '/{}'.format(ENV.get('STAGE'))
else:
    URL_PREFIX = ''

SECRET = 'xz98hw98hxixn09'

################################################################################
### Assets and storage
################################################################################

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

IN_BUCKET = 'zwatermark-in'
OUT_BUCKET = 'zwatermark-out'

WATERMARK_FILE = os.path.join(PARENT_DIRECTORY, 'watermark.png')

ALLOWED_EXTENSIONS = ['jpg', 'png', ]


################################################################################
### Sanitized dict for passing to templates
################################################################################

CONTEXT = {'PROJECT_NAME': PROJECT_NAME, 'URL_PREFIX': URL_PREFIX, 'OUT_BUCKET': OUT_BUCKET}