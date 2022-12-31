# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
