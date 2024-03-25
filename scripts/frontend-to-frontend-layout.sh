#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend into frontend-layout
git switch frontend
git pull
git switch frontend-layout
git pull
git merge frontend
echo "Merged frontend into frontend-layout"
git commit -m "Merged frontend into frontend-layout"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-to-frontend-layout.sh

# Only devops can run
