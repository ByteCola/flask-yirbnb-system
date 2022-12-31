# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

import os

from datetime import datetime

from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user

from apps import db
from apps.profile import blueprint
from apps.profile.forms import ProfileForm, BillingForm, LandlordForm
from apps.profile.models import Profiles, Billing, Landlord
from apps.profile.util import allowed_image_file

from apps.config import Config


# 用户个人信息（设置）路由方法定义与实现

@blueprint.route('/settings/photo/<filename>', methods=['GET', 'POST'])
def profile_photo(filename):
    """
    个人照片访问
    :param filename:
    :return:
    """
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@blueprint.route('/settings.html', methods=['GET', 'POST'])
@login_required
def settings():
    """
    个人信息的查询与保存
    :return:
    """
    profile_exists = Profiles.query.filter_by(users_id=current_user.id).first()

    if not profile_exists:

        profile_form = ProfileForm()
        user_profile = Profiles()

        if 'profile' in request.form:

            # check if file added and upload
            file = request.files['photo']
            if file and allowed_image_file(file.filename):
                # create a secure filename and save file in Uploads folder
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = str(current_user.id) + "." + ext
                file.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))

            profile_form.populate_obj(user_profile)

            user_profile.users_id = current_user.id
            # convert date str into python datetime object
            user_profile.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d')

            # add saved filename into user profile column
            if file and allowed_image_file(file.filename):
                user_profile.photo = filename
            else:
                user_profile.photo = ""

            db.session.add(user_profile)
            db.session.commit()

            return render_template('profile/settings.html',
                                   form=profile_form,
                                   msg='Profile details added successfully',
                                   segment='profile')

        return render_template('profile/settings.html', form=profile_form, segment='profile')

    if profile_exists:

        profile_form = ProfileForm(obj=profile_exists)

        if 'profile' in request.form:

            old_photo = profile_exists.photo
            # check if file added and upload
            file = request.files['photo']
            if file and allowed_image_file(file.filename):
                # create a secure filename and save file in Uploads folder
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = str(current_user.id) + "." + ext
                file.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))

            profile_form.populate_obj(profile_exists)

            # convert date str into python datetime object
            profile_exists.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d')

            # add saved filename into user profile column
            if file and allowed_image_file(file.filename):
                profile_exists.photo = filename
            else:
                profile_exists.photo = old_photo

            db.session.add(profile_exists)
            db.session.commit()

            return render_template('profile/settings.html',
                                   form=profile_form,
                                   msg='Profile details updated successfully',
                                   segment='profile')

        return render_template('profile/settings.html', form=profile_form, segment='profile')

    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/billing.html', methods=['GET', 'POST'])
@login_required
def billing():
    """
    收款账号设置
    :return:
    """
    billing_exists = Billing.query.filter_by(users_id=current_user.id).first()
    if not billing_exists:
        billing_form = BillingForm()
        user_billing = Billing()
        if 'billing' in request.form:
            billing_form.populate_obj(user_billing)
            user_billing.users_id = current_user.id
            user_billing.account = request.form['account']
            db.session.add(user_billing)
            db.session.commit()

            return render_template('profile/billing.html',
                                   form=billing_form,
                                   msg='更新账户信息成功',
                                   segment='billing')

        return render_template('profile/billing.html', form=billing_form, segment='billing')

    if billing_exists:

        billing_form = BillingForm(obj=billing_exists)

        if 'billing' in request.form:
            billing_form.populate_obj(billing_exists)
            billing_exists.account = request.form['account']
            db.session.add(billing_exists)
            db.session.commit()

            return render_template('profile/billing.html',
                                   form=billing_form,
                                   msg='更新账户信息成功',
                                   segment='billing')
        return render_template('profile/billing.html', form=billing_form, segment='billing')
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/landlord.html', methods=['GET', 'POST'])
@login_required
def landlord():
    """
    房东实名认证
    :return:
    """
    landlord_exists = Landlord.query.filter_by(users_id=current_user.id).first()
    if not landlord_exists:
        landlord_form = LandlordForm()
        user_landlord = Landlord()
        if 'landlord' in request.form:
            landlord_form.populate_obj(user_landlord)
            user_landlord.users_id = current_user.id
            user_landlord.id_name = request.form['id_name']
            user_landlord.id_no = request.form['id_no']
            user_landlord.id_pic_1 = request.form['id_pic_1']
            user_landlord.id_pic_2 = request.form['id_pic_2']
            db.session.add(user_landlord)
            db.session.commit()

            return render_template('profile/landlord.html',
                                   form=landlord_form,
                                   landlord=user_landlord,
                                   msg='提交成功',
                                   segment='landlord')

        return render_template('profile/landlord.html', form=landlord_form,landlord=user_landlord, segment='landlord')

    if landlord_exists:

        landlord_form = LandlordForm(obj=landlord_exists)

        if 'landlord' in request.form:
            landlord_form.populate_obj(landlord_exists)
            landlord_exists.id_name = request.form['id_name']
            landlord_exists.id_no = request.form['id_no']
            landlord_exists.id_pic_1 = request.form['id_pic_1']
            landlord_exists.id_pic_2 = request.form['id_pic_2']
            db.session.add(landlord_exists)
            db.session.commit()

            return render_template('profile/landlord.html',
                                   form=landlord_form,
                                   msg='提交成功',
                                   landlord=landlord_exists,
                                   segment='landlord')
        return render_template('profile/landlord.html', form=landlord_form,landlord=landlord_exists, segment='landlord')
    return redirect(url_for('home_blueprint.index'))
