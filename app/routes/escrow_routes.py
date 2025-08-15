from flask import Blueprint, request, jsonify, g
from ..utils.auth_utils import require_api_key, require_role
from ..schemas.escrow_schema import EscrowTransactionSchema
from ..models.escrow_transaction import EscrowTransaction
from ..extensions import db

escrow_bp = Blueprint('escrow', __name__)

@escrow_bp.route('/create', methods=['POST'])
@require_api_key
def create_escrow():
    data = request.get_json()
    schema = EscrowTransactionSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # MOCK: Use a fake subaddress for development/testing
    subaddress = f"FAKE_MONERO_SUBADDRESS_{data['buyer_id']}_{data['seller_id']}"

    escrow = EscrowTransaction(
        buyer_id=data['buyer_id'],
        seller_id=data['seller_id'],
        subaddress=subaddress,
        amount=data['amount'],
        status='waiting_payment'
    )
    db.session.add(escrow)
    db.session.commit()

    return jsonify(schema.dump(escrow)), 201

@escrow_bp.route('/status/<uuid>', methods=['GET'])
@require_api_key
def escrow_status(uuid):
    escrow = EscrowTransaction.query.filter_by(id=uuid).first()
    if not escrow:
        return jsonify({'error': 'Escrow not found'}), 404
    schema = EscrowTransactionSchema()
    return jsonify(schema.dump(escrow)), 200

@escrow_bp.route('/release/<uuid>', methods=['POST'])
@require_api_key
@require_role('admin')
def release_escrow(uuid):
    escrow = EscrowTransaction.query.filter_by(id=uuid).first()
    if not escrow:
        return jsonify({'error': 'Escrow not found'}), 404
    if escrow.status != 'funded':
        return jsonify({'error': 'Escrow is not funded and cannot be released'}), 400
    escrow.status = 'completed'
    db.session.commit()
    schema = EscrowTransactionSchema()
    return jsonify(schema.dump(escrow)), 200

@escrow_bp.route('/refund/<uuid>', methods=['POST'])
@require_api_key
@require_role('admin')
def refund_escrow(uuid):
    escrow = EscrowTransaction.query.filter_by(id=uuid).first()
    if not escrow:
        return jsonify({'error': 'Escrow not found'}), 404
    if escrow.status != 'funded':
        return jsonify({'error': 'Escrow is not funded and cannot be refunded'}), 400
    escrow.status = 'refunded'
    db.session.commit()
    schema = EscrowTransactionSchema()
    return jsonify(schema.dump(escrow)), 200