import logging

from flask import ctx, g


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """Provide some extra variables to be placed into the log message"""

        # If we have an app context (because we're servicing an http request) then get the trace id we have
        # set in g (see app.py)
        if ctx.has_request_context():
            log_record.trace_id = g.trace_id
        else:
            log_record.trace_id = "N/A"
        return True
