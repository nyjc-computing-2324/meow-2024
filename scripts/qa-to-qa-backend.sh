#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge qa into qa-backend
git switch qa
git pull
git switch qa-backend
git pull
git merge qa
echo "Merged qa into qa-backend"
git commit -m "Merged qa into qa-backend"
git push

# Update permissions to +x
chmod 700 ./scripts/qa-to-qa-backend.sh

# Only devops can run
