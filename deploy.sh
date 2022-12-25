# !bin/bash
set -e -x

if [ -f .env ]
then
  export $(cat .env | xargs)
fi

yarn build
poetry export --without-hashes -f requirements.txt -o requirements.txt --with-credentials
yarn serverless deploy
rm -f requirements.txt
aws s3 cp frontend/build "s3://${WEBSITE_BUCKET}/" --recursive --acl 'public-read'