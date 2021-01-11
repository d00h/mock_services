"""
name: service/mailgun
description: |
   https://documentation.mailgun.com/
   Integrate email into your application with ease
"""
from datetime import datetime

from covador import opt, split
from covador.flask import form
from flask import Blueprint, jsonify

mailgun = Blueprint("mailgun", __name__)
mailgun.swagger_tag = __doc__


@mailgun.route('/messages', methods=['POST'])
@form(**{
    'from': str,
    'to': split(str),
    'subject': str,
    'text': str,
    'html': opt(str),
    'o:testmode': opt(str),
})
def messages(profile, **kwargs):
    '''
    summary: Отправка почты
    tags: [ service/mailgun ]
    description:  |
        https://documentation.mailgun.com/en/latest/api-sending.html#sending
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: profile
        type: string
        required: true
        default: default
      - in: formData
        name: from
        type: string
        format: email
        default: sender@gmail.com
        required: true
      - in: formData
        name: to
        type: array
        collectionFormat: csv
        items:
           type: string
           format: email
        required: true
      - in: formData
        name: subject
        type: string
        required: true
        default: SomeTitle
      - in: formData
        name: text
        type: string
        required: true
        default: Hello user
      - in: formData
        name: html
        type: string
        required: false
      - in: formData
        name: "o:test"
        type: string
        required: false
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
    now = datetime.now()
    return jsonify(
        id='<{0:%Y%m%d%H%M%S}.{1}@mailgun.org>'.format(now, now.timestamp()),
        text='Queued. Thank you.'
    )


@mailgun.route('/stats/total', methods=['GET'])
def stats(profile, **kwargs):
    '''
    summary: Получение статистики рассылки
    tags: [ service/mailgun ]
    description: |
       https://documentation.mailgun.com/en/latest/api-stats.html#stats

       BUG: попробывать не работает из-за ограничений передачи параметров swagger-ui в GET

       сгенеренный curl работает нормально
    parameters:
      - in: path
        name: profile
        type: string
        required: true
        default: default
      - in: formData
        name: event
        type: string
        required: true
        enum:
        - accepted
        - delivered
        - failed
        - opened
        - clicked
        - unsubscribed
        - complained
        - stored
      - in: formData
        name: duration
        type: string
        required: true
        example: [ 12h, 1d ]
        default: 1d
    responses:
        200:
            description: OK
            schema:
                type: object
   '''
    return jsonify(
        {
            "end": "Fri, 01 Apr 2012 00:00:00 UTC",
            "resolution": "month",
            "start": "Tue, 14 Feb 2012 00:00:00 UTC",
            "stats": [
                {
                    "time": "Tue, 14 Feb 2012 00:00:00 UTC",
                    "accepted": {
                        "outgoing": 10,  # authenticated
                        "incoming": 5,   # unauthenticated
                        "total": 15
                    },
                    "delivered": {
                        "smtp": 15,  # delivered over SMTP
                        "http": 5,   # delivered over HTTP
                        "total": 20
                    },
                    "failed": {
                        "permanent": {
                            "bounce": 4,
                            "delayed-bounce": 1,
                            "suppress-bounce": 1,       # recipients previously bounced
                            "suppress-unsubscribe": 2,  # recipients previously unsubscribed
                            "suppress-complaint": 3,    # recipients previously complained
                            "total": 10                 # failed permanently and dropped
                        },
                        "temporary": {
                            "espblock": 1   # failed temporary due to ESP block, will be retried
                        }
                    },
                }
            ]
        }
    )
