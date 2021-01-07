from flask import Blueprint, render_template_string, url_for

root = Blueprint('root', __name__)


@root.route('/')
def samples():
    easysms_args = dict(
        login='some login',
        password='some_password',
        ordinator='+7-499-123-56-12',
        phone='+7-499-999-99-99',
        text='hello world'
    )
    items = [
        dict(
            caption='ApiDocs', href='/apidocs'),
        dict(
            caption='EasySMS: default',
            href=url_for('easysms.send_sms', profile='default', **easysms_args)),
        dict(
            caption='EasySMS: weak',
            href=url_for('easysms.send_sms', profile='easysms_weak', **easysms_args)),
        dict(
            caption='EasySMS: sequence',
            href=url_for('easysms.send_sms', profile='easysms_123', **easysms_args)),
        dict(
            caption='EasySMS: sms_limit',
            href=url_for('easysms.send_sms', profile='easysms_limit', **easysms_args)),
    ]
    return render_template_string("""
    <html>
    <body>
        {% for item in items %}
           <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
        {% endfor %}
    </body>
    </html>
    """, items=items)
