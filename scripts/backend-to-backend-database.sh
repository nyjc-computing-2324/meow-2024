#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge backend into backend-database
git switch backend
git pull
git switch backend-database
git pull
git merge backend
echo "Merged backend into backend-database"
git commit -m "Merged backend into backend-database"
git push

# Update permissions to +x
chmod 700 ./scripts/backend-to-backend-database.sh

# Only devops can run
