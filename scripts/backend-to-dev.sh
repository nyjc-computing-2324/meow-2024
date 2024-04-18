#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge backend into dev
git switch backend
git pull
git switch dev
git pull
git merge backend
echo "Merged backend into dev"
git commit -m "Merged backend into dev"
git push

# Update permissions to +x
chmod 700 ./scripts/backend-to-dev.sh

# Only devops can run
