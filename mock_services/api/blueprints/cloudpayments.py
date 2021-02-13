# Generated from specs/cloudpayments.yaml
from covador.flask import args
from flask import Blueprint, current_app, jsonify, request

cloudpayments = Blueprint("cloudpayments", __name__)


@cloudpayments.route('{profile}/payments/cards/auth',
                     endpoint='payments_cards_auth', methods=['post'])
@args(profile=str)
def payments_cards_auth(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    result = {}
    return jsonify(result)


@cloudpayments.route('{profile}/payments/void',
                     endpoint='payments_void', methods=['post'])
@args(profile=str)
def payments_void(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    result = {}
    return jsonify(result)


@cloudpayments.route('{profile}/payments/tokens/charge',
                     endpoint='payments_tokens_charge', methods=['post'])
@args(profile=str)
def payments_tokens_charge(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    result = {}
    return jsonify(result)


@cloudpayments.route('{profile}/payments/cards/post3ds',
                     endpoint='payment_cards_post3ds', methods=['post'])
@args(profile=str)
def payment_cards_post3ds(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    result = {}
    return jsonify(result)


@cloudpayments.route('{profile}/payments/find',
                     endpoint='payments_find', methods=['post'])
@args(profile=str)
def payments_find(profile, **kwargs):
    response = current_app.get_fake_response(
        profile=profile, endpoint=request.endpoint, **kwargs)
    if response is not None:
        return response
    result = {}
    return jsonify(result)
