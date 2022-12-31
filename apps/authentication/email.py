# -*- encoding: utf-8 -*-
"""
邮件发送
Copyright (c) 2022 - present ByteCola
"""

from flask_mailman import EmailMessage
from apps.config import Config

from flask import current_app

def send_email(subject, body, send_to):
    """
    向目标邮箱发送邮件
    :param subject: 邮件主题
    :param body: 邮件内容
    :param send_to: 发送邮箱
    :return: Ture or False
    """
    try:

        msg = EmailMessage(
            subject,
            body,
            Config.MAIL_USERNAME,
            [send_to]
        )
        msg.content_subtype = "html"
        msg.send()

        return True
    
    except:
        current_app.logger.info('ERR - Cannot send email, please check MAIL settings')
        current_app.logger.info('    -> MAIL Subject: ' + subject )
        current_app.logger.info('    -> MAIL Body: ' + body )
        return False