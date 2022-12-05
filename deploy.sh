# !bin/bash
set -e -x
yarn build
poetry export --without-hashes -f requirements.txt -o requirements.txt --with-credentials
yarn serverless deploy
rm -f requirements.txt