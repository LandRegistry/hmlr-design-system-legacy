import os

# RULES OF CONFIG:
# 1. No region specific code. Regions are defined by setting the OS environment variables appropriately to build up the
# desired behaviour.
# 2. No use of defaults when getting OS environment variables. They must all be set to the required values prior to the
# app starting.
# 3. This is the only file in the app where os.environ should be used.


# For logging
FLASK_LOG_LEVEL = os.environ["LOG_LEVEL"]

# For health route
COMMIT = os.environ["COMMIT"]

# This APP_NAME variable is to allow changing the app name when the app is running in a cluster. So that
# each app in the cluster will have a unique name.
APP_NAME = os.environ["APP_NAME"]

MAX_HEALTH_CASCADE = os.environ["MAX_HEALTH_CASCADE"]
# Following is an example of building the dependency structure used by the cascade route
# SELF can be used to demonstrate how it works (i.e. it will call it's own cascade
# route until MAX_HEALTH_CASCADE is hit)
# SELF = "http://localhost:8080"
# DEPENDENCIES = {"SELF": SELF}

# Secret key for CSRF
SECRET_KEY = os.environ["SECRET_KEY"]

# Content security policy mode
# Can be either 'full' or 'report-only'
# 'full' will action the CSP and block violations
# 'report-only' will log but not block violations
# It is recommended to run in report-only mode for a while and monitor the logs
# to ensure that all violations are cleaned up to prevent your app from breaking
# when you switch it on fully
CONTENT_SECURITY_POLICY_MODE = os.environ["CONTENT_SECURITY_POLICY_MODE"]

# Static assets mode
# Can be either 'development' or 'production'
# 'development' will:
#   - Not gzip static assets
#   - Set far *past* expiry headers on static asset requests to prevent your browser from caching them
#   - Not add cachebusters to static asset query strings
# 'production' will:
#   - gzip static assets
#   - Set far *future* expiry headers on static asset requests to force browsers to cache for a long time
#   - Add cachebusters to static asset query strings to invalidate browsers' caches when necessary
STATIC_ASSETS_MODE = os.environ["STATIC_ASSETS_MODE"]

# Using SQLAlchemy/Postgres?
# The required variables (and required usage) can be found here:
# http://192.168.249.38/gadgets/gadget-api/blob/master/gadget_api/config.py
