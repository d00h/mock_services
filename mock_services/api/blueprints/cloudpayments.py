from flask import Blueprint, current_app, jsonify

cloudpayments = Blueprint("cloudpayments", __name__)


@cloudpayments.route('payments/cards/auth',
                     endpoint='payments_cards_auth',
                     methods=['post'])
def payments_cards_auth(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})


@cloudpayments.route('payments/void',
                     endpoint='payments_void',
                     methods=['post'])
def payments_void(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})


@cloudpayments.route('payments/tokens/charge',
                     endpoint='payments_tokens_charge',
                     methods=['post'])
def payments_tokens_charge(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})


@cloudpayments.route('payments/cards/post3ds',
                     endpoint='payment_cards_post3ds',
                     methods=['post'])
def payment_cards_post3ds(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})


@cloudpayments.route('payments/find',
                     endpoint='payments_find',
                     methods=['post'])
def payments_find(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})
