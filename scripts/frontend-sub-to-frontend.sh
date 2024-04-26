#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend-sub into frontend
git switch frontend-sub
git pull
git switch frontend
git pull
git merge frontend-sub
echo "Merged frontend-sub into frontend"
git commit -m "Merged frontend-sub into frontend"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-sub-to-frontend.sh

# Only devops can run
