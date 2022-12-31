# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""
import os
import uuid

from flask import request
from apps.config import Config
from apps.profile.util import allowed_image_file

from apps.rs import blueprint

# 文件图片上传路由方法定义与实现

@blueprint.route('/rs-upload', methods=['GET', 'POST'])
def upload():
    """
    图片上传与保存
    :return:
    """
    file = request.files['file']
    if file and allowed_image_file(file.filename):
        # create a secure filename and save file in Uploads folder
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = str(uuid.uuid4()) + "." + ext
        file.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))

    return filename
