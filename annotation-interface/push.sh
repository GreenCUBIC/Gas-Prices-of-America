aws s3 rm s3://gaspricesigns2 --recursive
aws s3 sync --acl public-read build s3://gaspricesigns2 --cache-control max-age=1
