from flask import Blueprint, render_template_string 

root = Blueprint('root', __name__)


@root.route('/')
def index():
    items = [
        dict(
            caption='ApiDocs', href='/apidocs'),
        # dict(
        #     caption='EasySMS: weak',
        #     href=url_for('easysms.send_sms', profile='easysms_weak', **easysms_args)),
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
