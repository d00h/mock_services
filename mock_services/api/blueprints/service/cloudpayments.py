# Generated from specs/cloudpayments.yaml
from flask import Blueprint, jsonify

from mock_services.api.decorators import mockable

cloudpayments = Blueprint("cloudpayments", __name__,
                          url_prefix='/service/cloudpayments')


@cloudpayments.route('payments/cards/auth',
                     endpoint='payments_cards_auth', methods=['post'])
@mockable
def payments_cards_auth(**kwargs):
    result = {}
    return jsonify(result)


@cloudpayments.route('payments/void',
                     endpoint='payments_void', methods=['post'])
@mockable
def payments_void(**kwargs):
    result = {}
    return jsonify(result)


@cloudpayments.route('payments/tokens/charge',
                     endpoint='payments_tokens_charge', methods=['post'])
@mockable
def payments_tokens_charge(**kwargs):
    result = {}
    return jsonify(result)


@cloudpayments.route('payments/cards/post3ds',
                     endpoint='payment_cards_post3ds', methods=['post'])
@mockable
def payment_cards_post3ds(**kwargs):
    result = {}
    return jsonify(result)


@cloudpayments.route('payments/find',
                     endpoint='payments_find', methods=['post'])
@mockable
def payments_find(**kwargs):
    result = {}
    return jsonify(result)
