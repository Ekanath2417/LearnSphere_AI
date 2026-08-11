from flask import jsonify


def response(data=None, message="Success", status=200):
    return jsonify({"success": True, "message": message, "data": data}), status


def error(message, status=400, code="VALIDATION_ERROR"):
    return jsonify({"success": False, "message": message, "error": code}), status


def public_user_id():
    """Academic library content is intentionally available without login."""
    return 0


def parse_id(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None
