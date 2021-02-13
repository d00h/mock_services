import uuid
from covador import opt
from covador.flask import args, query_string
from flask import Blueprint, jsonify, request, current_app

easysms = Blueprint("easysms", __name__)


@easysms.route('/', methods=['GET'], endpoint='send_sms')
@args(profile=str)
@query_string(login=opt(str), password=opt(str),
              ordinator=str, phone=str, text=str)
def send_sms(profile, login, password, ordinator, phone, text):
    return current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint,
        login=login, password=password,
        ordinator=ordinator, phone=phone, text=text) or \
        jsonify(sms_id=uuid.uuid4(), text='Sended')