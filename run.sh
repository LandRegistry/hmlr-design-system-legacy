#!/bin/bash

cp /supporting-files/package-lock.json .
npm run build &
/usr/local/bin/gunicorn --pythonpath /src --access-logfile - manage:manager.app --reload --keyfile /supporting-files/ssl.key --certfile /supporting-files/ssl.cert
