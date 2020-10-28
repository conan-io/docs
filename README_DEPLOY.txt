#### How to Deploy

0. Checkout to the latest version (before release), e.g., release/1.4.2 and merge master into it,
   to make sure we keep the version freeze with the latest changes, and push it.
1. Go  to master, edit conf.py and change the current version
2. Edit the deploy_gh_pages.py, down, the versions_dict and introduce all the history versions we want to maintain
3. Push master.


#### Testing Locally

Testing gh-pages locally is possible, but requires some steps before generating all artifacts.
We recommend doing it on 'master' branch, because the script is harcoded, but you can use any other branch name too.

1. Install all requirements
  - pip install -r requirements.txt
  - apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra latexmk enchant
  If you don't want to install all these packages, you can use a Docker image e.g conanio/gcc9

2. If you are using a different branch name (e.g. hotfix/foobar), you have to update deploy_gh_pages.py:
  - On versions_dict, replace "master" by your current branch name

3. As this test is local only, you don't need to deploy, thus you should update the main method:
  - Comment deploy() under the main method
  - The condition 'if should_deploy():' should be replaced by 'if True:'

4. If you want to generate the folder 'en/latest' and your current branch name is not master, you have to update
   'if branch == "master":' under build_and_copy() method. Replace "master" by your current branch name.

5. On versions_dict, you can discard all versions which you don't want to generate. Otherwise, it will take longer to finish.

6. Commit all temporary changes.

7. Run 'python deploy_gh_pages.py'

8. As result, you should be now on 'gh-pages' branch and looking only the generated html files.
   Now you can navigate with web browser as usual.
