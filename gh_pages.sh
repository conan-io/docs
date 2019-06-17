make html && rm -rf /tmp/docs && cp -r ./_build/html/* /tmp/docs && git checkout gh-pages && git rm -r * && cp -r /tmp/docs . && git add . && git commit -m "gh pages"
