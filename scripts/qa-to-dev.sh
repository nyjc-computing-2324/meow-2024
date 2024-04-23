#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge qa into dev
git switch qa
git pull
git switch dev
git pull
git merge qa
echo "Merged qa into dev"
git commit -m "Merged qa into dev"
git push

# Update permissions to +x
chmod 700 ./scripts/qa-to-dev.sh

# Only devops can run
