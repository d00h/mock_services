import uuid

from covador import opt
from covador.flask import query_string
from flask import Blueprint, current_app, jsonify, request

easysms = Blueprint("easysms", __name__, url_prefix='/service/easysms')


@easysms.route('/', methods=['get'], endpoint='send_sms')
@query_string(login=opt(str), password=opt(str),
              ordinator=str, phone=str, text=str)
def send_sms(login, password, ordinator, phone, text):
    response = current_app.get_fake_response(
        endpoint=request.endpoint,
        login=login, password=password,
        ordinator=ordinator, phone=phone, text=text)
    if response is not None:
        return response
    return jsonify(sms_id=uuid.uuid4(), text='Sended')
