from flask import Blueprint, render_template_string 

root = Blueprint('root', __name__)


@root.route('/')
def index():
    items = [
        dict(caption='ApiDocs', href='/apidocs'),
        dict(caption='Profile', href='/mock_profile'),
        dict(caption='Logs', href='/mock_logger'),
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
