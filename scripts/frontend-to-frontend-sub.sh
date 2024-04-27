#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend into frontend-sub
git switch frontend
git pull
git switch frontend-sub
git pull
git merge frontend
echo "Merged frontend into frontend-sub"
git commit -m "Merged frontend into frontend-sub"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-to-frontend-sub.sh

# Only devops can run