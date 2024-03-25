#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend-layout into frontend
git switch frontend-layout
git pull
git switch frontend
git pull
git merge frontend-layout
echo "Merged frontend-layout into frontend"
git commit -m "Merged frontend-layout into frontend"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-layout-to-frontend.sh

# Only devops can run
