"""
name: service/easysms
description: |
    https://easy-sms.ru/
    SMS рассылки в один клик!
    Рекламные, информационные и сервисные сообщения
"""
import uuid

from covador import opt
from covador.flask import args, query_string
from flask import Blueprint, current_app, jsonify, request

easysms = Blueprint("easysms", __name__)
easysms.swagger_tag = __doc__


@easysms.route('/', methods=['GET'])
@args(profile=str)
@query_string(login=opt(str), password=opt(str),
              ordinator=str, phone=str, text=str)
def send_sms(profile, login, password, ordinator, phone, text):
    '''
      tags: [ service/easysms ]
      summary: Oтправка смс
      description: https://easy-sms.ru/podcluchenia/#api_sms
      parameters:
      - in: path
        name: profile
        type: string
        required: true
        default: default
      - in: query
        name: login
        type: string
        required: true
      - in: query
        name: password
        type: string
        required: true
      - in: query
        name: ordinator
        type: string
        required: true
        description: Отправитель
      - in: query
        name: phone
        type: string
        required: true
      - in: query
        name: text
        type: string
        required: true
      responses:
        200:
          description: OK
          schema:
            type: object
            properties:
              sms_id:
                type: string
                format: uuid
              text:
                type: string
    '''
    return current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint,
        login=login, password=password,
        ordinator=ordinator, phone=phone, text=text) or \
        jsonify(sms_id=uuid.uuid4(), text='Sended')
