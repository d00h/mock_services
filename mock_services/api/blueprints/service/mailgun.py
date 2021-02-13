from datetime import datetime

from covador import opt, split
from covador.flask import form, args
from flask import Blueprint, current_app, jsonify, request

mailgun = Blueprint("mailgun", __name__)


@mailgun.route('/{profile}/messages', methods=['POST'])
@args(profile=str)
@form(**{
    'from': str,
    'to': split(str),
    'subject': str,
    'text': str,
    'html': opt(str),
    'o:testmode': opt(str),
})
def messages(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    now = datetime.now()
    return jsonify(
        id='<{0:%Y%m%d%H%M%S}.{1}@mailgun.org>'.format(now, now.timestamp()),
        text='Queued. Thank you.'
    )


@mailgun.route('/{profile}/stats/total', methods=['GET'])
@args(profile=str)
def stats(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response

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
