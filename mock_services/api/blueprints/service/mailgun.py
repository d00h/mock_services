"""
name: service/mailgun
description: |
   https://documentation.mailgun.com/
   Integrate email into your application with ease
"""
import uuid

from covador import opt
from covador.flask import query_string
from flask import Blueprint, jsonify

mailgun = Blueprint("mailgun", __name__)
mailgun.swagger_tag = __doc__

@mailgun.route('/messages', methods=['POST'])
def messages():
    '''
    summary: Отправка почты
    tags: [ service/mailgun ]
    description: https://documentation.mailgun.com/en/latest/api-sending.html#sending
    responses:
        200:
            description: OK
            schema:
                type: object
                properties:
                    id:
                        type: string
                    message:
                        type: string
   '''
    return jsonify(
        id='<20111114174239.25659.5817@samples.mailgun.org>',
        text='Queued. Thank you.'
    )
    

@mailgun.route('/stats', methods=['GET'])
def stats():
    '''
    summary: Получение статистики рассылки
    tags: [ service/mailgun ]
    description: https://documentation.mailgun.com/en/latest/api-stats.html#stats
    responses:
        200:
            description: OK
            schema:
                type: object
                properties:
                    id:
                        type: string
                    message:
                        type: string
   '''
    return jsonify(
        id='<20111114174239.25659.5817@samples.mailgun.org>',
        text='Queued. Thank you.'
    )
