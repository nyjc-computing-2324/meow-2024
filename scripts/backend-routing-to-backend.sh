#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge backend-routing into backend
git switch backend-routing
git pull
git switch backend
git pull
git merge backend-routing
echo "Merged backend-routing into backend"
git commit -m "Merged backend-routing into backend"
git push

# Update permissions to +x
chmod 700 ./scripts/backend-routing-to-backend.sh

# Only devops can run
