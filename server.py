#!/usr/bin/env python
import os, boto3
from flask import Flask, Response, send_file, jsonify, abort, request, render_template, send_from_directory, redirect, flash
from werkzeug.utils import secure_filename

import config


################################################################################
### Environment setup
################################################################################

app = Flask(__name__)
app.secret_key = config.SECRET
s3 = boto3.resource('s3')


################################################################################
### Path handlers
################################################################################

@app.route('/')
def home():
    """
    Home page
    """

    images = [x.key for x in s3.Bucket(config.OUT_BUCKET).objects.all()]

    return render_template('index.html', context=config.CONTEXT, images=images)


################################################################################
### Generic handlers and addons
################################################################################

@app.route('/static/<path:path>')
def static_serve(path):
    """
    Implements static file serving through application process.
    Not ideal for many performance reasons, but sometimes useful or necessary.
    """
    return send_from_directory('static', path)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['x-Badass'] = 'Yes I am.'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


################################################################################
### Command line handler
################################################################################

if __name__ == '__main__':
    app.run(processes=3, host='0.0.0.0', port=5000, debug=True)

