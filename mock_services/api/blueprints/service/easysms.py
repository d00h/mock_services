import uuid

from covador import opt
from covador.flask import query_string
from flask import Blueprint, jsonify 
from mock_services.api.decorators import mockable

easysms = Blueprint("easysms", __name__, url_prefix='/service/easysms')


@easysms.route('/', methods=['get'], endpoint='send_sms')
@query_string(login=opt(str), password=opt(str),
              ordinator=str, phone=str, text=str)
@mockable
def send_sms(login, password, ordinator, phone, text):
    return jsonify(sms_id=uuid.uuid4(), text='Sended')
