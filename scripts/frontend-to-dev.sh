#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend into dev
git switch frontend
git pull
git switch dev
git pull
git merge frontend
echo "Merged frontend into dev"
git commit -m "Merged frontend into dev"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-to-dev.sh

# Only devops can run
