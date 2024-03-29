#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge qa-backend into qa
git switch qa-backend
git pull
git switch qa
git pull
git merge qa-backend
echo "Merged qa-backend into qa"
git commit -m "Merged qa-backend into qa"
git push

# Update permissions to +x
chmod 700 ./scripts/qa-backend-to-qa.sh

# Only devops can run
