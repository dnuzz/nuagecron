# !bin/bash
set -e -x
poetry export --without-hashes -f requirements.txt -o requirements.txt --with-credentials
yarn serverless deploy
rm -f requirements.txt