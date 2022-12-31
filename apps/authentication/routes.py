# -*- encoding: utf-8 -*-
"""
登录、注册等认证路由相关
Copyright (c) 2022 - present ByteCola
"""

from uuid import uuid4
from itsdangerous import URLSafeSerializer

from flask import current_app

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import (LoginForm, CreateAccountForm,
                                       ForgotPasswordForm, ResetPasswordForm)
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, hash_pass

from apps.config import Config
from apps.authentication.email import send_email


# 登录与注册等认证路由方法定义

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        if user and not user.account_status:
            # Email not confirmed
            return render_template('accounts/login.html',
                                   msg='Inactive account - 请登录邮箱激活您的账号',
                                   form=login_form)

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.login'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='用户名或密码错误',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)

    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        msg = None   

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='用户名已存在',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='邮箱已注册',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)

        # check if confirmation email to be sent or not for activating account
        if Config.EMAIL_CONFIRMATION_REQUIRED:

            user.account_status = False 

            if confirm_user_mail(username, email):
                msg='User created, 请登录邮箱确认'
            else:
                msg='User created, 激活邮件发送失败.'

            db.session.add(user)
            db.session.commit()

            return render_template('accounts/register.html',
                                   msg=msg,
                                   success=True,
                                   form=create_account_form)

        else:
            user.account_status = True
            db.session.add(user)
            db.session.commit()

            return render_template('accounts/register.html',
                                   msg='账号创建成功 <a href="/login">请登录</a>',
                                   success=True,
                                   form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


def confirm_user_mail(username, email):

    # create a confirm_account link to send in email
    s = URLSafeSerializer('serliaizer_code')
    key = s.dumps([username, email])
    url = url_for('authentication_blueprint.confirm_account', secretstring=key, _external=True)

    subject = '账户确认'
    body_content = "请激活您的账号. <a href='" + url + "'>点击激活</a>"

    return send_email(subject, body_content, email)


@blueprint.route('/confirm_account/<secretstring>', methods=['GET', 'POST'])
def confirm_account(secretstring):
    s = URLSafeSerializer('serliaizer_code')
    username, email = s.loads(secretstring)

    user = Users.query.filter_by(username=username).first()
    user.account_status = True
    db.session.add(user)
    db.session.commit()

    #return redirect(url_for("authentication_blueprint.login", msg="Your account was confirmed succsessfully"))
    return render_template('accounts/login.html',
                        msg='Account confirmed successfully.',
                        form=LoginForm())

@blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    forgot_password_form = ForgotPasswordForm(request.form)
    if 'forgot-password' in request.form:

        # read form data
        email = request.form['email']

        # Locate user
        user = Users.query.filter_by(email=email).first()

        # Check user exists
        if user:

            user.email_token_key = str(uuid4())
            db.session.add(user)
            db.session.commit()

            # create a set_password link to send in email
            url = url_for('authentication_blueprint.reset_password',
                          email=user.email,
                          email_token_key=user.email_token_key,
                          _external=True)

            subject = '重置密码'
            body_content = "请重置您的账号密码. <a href='" + url + "'>点击重置</a>"

            send_email(subject, body_content, email)

            return render_template('registration/forgot_password.html',
                                   msg='重置链接已经发送至您的邮箱，请登录邮箱查看',
                                   success=True,
                                   form=forgot_password_form)

        return render_template('registration/forgot_password.html',
                               msg='不存在输入的邮箱账户',
                               success=False,
                               form=forgot_password_form)

    return render_template('registration/forgot_password.html', form=forgot_password_form)

def update_password(email, email_token_key, password):

    user = Users.query.filter_by(email_token_key=email_token_key, email=email).first()

    if user:
        user.password = hash_pass(password)
        user.email_token_key = None
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False    

@blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    email_token_key=request.values["email_token_key"]
    email=request.values["email"]

    current_app.logger.info('RESET_PASS -> EMAIL: ' + email )
    current_app.logger.info('RESET_PASS -> TOKEN: ' + email_token_key )

    user = Users.query.filter_by(email_token_key=email_token_key, email=email).first()
    if user:
        reset_password_form = ResetPasswordForm(email_token_key=email_token_key,
                                                email=email)

        msg=None     
        if 'reset-password' in request.form:
            
            if update_password(reset_password_form.email.data,
                               reset_password_form.email_token_key.data,
                               reset_password_form.password.data):

                msg='密码重置成功.'
            else:
                msg='密码重置失败.'

            #return redirect(url_for("authentication_blueprint.login", msg="Your password has been changed, log in again"))
            return render_template('accounts/login.html',
                        msg=msg,
                        form=LoginForm())

    return render_template("registration/reset_password.html", form=ResetPasswordForm(email_token_key=email_token_key, email=email))



@blueprint.route('/edit_password', methods=['GET', 'POST'])
def edit_password():

    if 'edit_password' in request.form:

        source_password = request.form['source_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if confirm_password != new_password:
            return render_template('accounts/security.html',
                                   msg='新密码输入不一致',
                                   success=False)

        user = Users.query.filter_by(username=current_user.username).first()

        # 验证密码
        if not verify_pass(source_password, user.password) :
            return render_template('accounts/security.html',
                                   msg='原密码输入错误',
                                   success=False)
        user.password = hash_pass(new_password)
        user.email_token_key = None
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/security.html',
                           msg='密码修改成功',
                           success=True)
    else:
        return render_template('accounts/security.html')




@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
   #return render_template('home/page-403.html'), 403
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
