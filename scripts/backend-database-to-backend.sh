#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge backend-database into backend
git switch backend-database
git pull
git switch backend
git pull
git merge backend-database
echo "Merged backend-database into backend"
git commit -m "Merged backend-database into backend"
git push

# Update permissions to +x
chmod 700 ./scripts/backend-database-to-backend.sh

# Only devops can run
