import re
from flask import current_app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.common.string import validate_email as validate_email_common


class Contact(FlaskForm):
    class Meta:
        csrf = False

    contact_type = RadioField('種別', choices=[], validators=[DataRequired()])
    name = StringField('名前', validators=[DataRequired(), Length(max=248)])
    name_phonetic = StringField('フリガナ',
                validators=[DataRequired(), Length(max=248)])
    email = StringField('メールアドレス',
                validators=[DataRequired(), Email(), Length(max=128)])
    tel = StringField('電話番号',
                validators=[DataRequired(), Length(min=10, max=11)])
    content = TextAreaField('内容', [DataRequired(), Length(max=3000)])
    recaptcha = None


    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        if current_app.config['CONTACT_USE_RECAPTCHA']:
            self.recaptcha = RecaptchaField()

    def validate_email(self, field):
        if not current_app.config['CONTACT_EMAIL_IS_CHECK_DNS']:
            return

        if not validate_email_common(field.data, True):
            raise ValidationError('メールアドレスが正しくありません。')


    def validate_tel(self, field):
        pattern = r'^(0[5-9]0[0-9]{8}|0[1-9][1-9][0-9]{7})$'
        matches = re.match(pattern, field.data)
        if matches == None:
            raise ValidationError('電話番号が正しくありません。')


    def get_dict(self):
        return {
            'contact_type': self.contact_type.data,
            'name': self.name.data,
            'name_phonetic': self.name_phonetic.data,
            'email': self.email.data,
            'tel': self.tel.data,
            'content': self.content.data,
        }
