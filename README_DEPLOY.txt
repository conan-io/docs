0. Checkout to the latest version (before release), e.j release/1.4.2 and merge master into it,
   to make sure we keep the version freeze with the latest changes, and push it.
1. Go  to master, edit conf.py and change the current version
2. Edit the deploy_gh_pages, down, the versions_dict and introduce all the history versions we want to maintain
3. Push master.