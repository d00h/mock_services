from datetime import datetime

from covador import opt, split
from covador.flask import args, form
from flask import Blueprint, jsonify 

from mock_services.api.decorators import mockable

mailgun = Blueprint("mailgun", __name__,
                    url_prefix='/service/mailgun')


@mailgun.route('messages', methods=['POST'])
@form(**{
    'from': str,
    'to': split(str),
    'subject': str,
    'text': str,
    'html': opt(str),
    'o:testmode': opt(str),
})
@mockable
def messages(**kwargs):
    now = datetime.now()
    return jsonify(
        id='<{0:%Y%m%d%H%M%S}.{1}@mailgun.org>'.format(now, now.timestamp()),
        text='Queued. Thank you.'
    )


@mailgun.route('stats/total', methods=['GET'])
@mockable
def stats(**kwargs):
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
