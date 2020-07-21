import json
import logging

from flask import Blueprint, g, request

reporting = Blueprint("reporting", __name__)
logger = logging.getLogger("content_security_policy")


@reporting.route("/", methods=["POST"])
def report():
    g.trace_id = request.args.get("trace_id")
    data = json.loads(request.data.decode("utf-8"))
    csp_report = data["csp-report"]

    logger.error("CSP violation", extra={"content_security_policy_report": csp_report})

    return "", 204
