# Don't wait till any change is done
echo Building HTML files && make html
watchmedo shell-command \
    --patterns="*.rst" \
    --recursive \
    --command='echo Rebuilding && make html' \
    --drop
    .
