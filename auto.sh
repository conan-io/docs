watchmedo shell-command \
    --patterns="*.rst" \
    --recursive \
    --command='echo Rebuilding && make html' \
    .
