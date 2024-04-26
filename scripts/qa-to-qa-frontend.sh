#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge qa into qa-frontend
git switch qa
git pull
git switch qa-frontend
git pull
git merge qa
echo "Merged qa into qa-frontend"
git commit -m "Merged qa into qa-frontend"
git push

# Update permissions to +x
chmod 700 ./scripts/qa-to-qa-frontend.sh

# Only devops can run
