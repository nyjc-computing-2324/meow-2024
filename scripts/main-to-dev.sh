#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge main into dev
git switch main
git pull
git switch dev
git pull
git merge main
echo "Merged main into dev"
git commit -m "Merged main into dev"
git push

# Update permissions to +x
chmod 700 ./scripts/main-to-dev.sh

# Only devops can run
