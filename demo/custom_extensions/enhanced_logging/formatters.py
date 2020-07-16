import collections
import json
import logging
import traceback


class JsonFormatter(logging.Formatter):
    def format(self, record):
        if record.exc_info:
            exc = traceback.format_exception(*record.exc_info)
        else:
            exc = None

        # Timestamp must be first (webops request)
        log_entry = collections.OrderedDict(
            [
                ("timestamp", self.formatTime(record)),
                ("level", record.levelname),
                ("traceid", record.trace_id),
                ("message", record.msg % record.args),
                ("exception", exc),
            ]
        )

        return json.dumps(log_entry)


class ContentSecurityPolicyFormatter(logging.Formatter):
    def format(self, record):
        # Timestamp must be first (webops request)
        log_entry = collections.OrderedDict(
            [
                ("timestamp", self.formatTime(record)),
                ("level", record.levelname),
                ("traceid", record.trace_id),
                ("message", record.msg % record.args),
                ("content_security_policy_report", record.content_security_policy_report),
            ]
        )

        return json.dumps(log_entry)
