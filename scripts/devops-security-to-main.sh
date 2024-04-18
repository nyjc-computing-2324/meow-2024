#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge devops-security into main
git switch devops-security
git pull
git switch main
git pull
git merge devops-security
echo "Merged devops-security into main"
git commit -m "Merged devops-security into main"
git push

# Update permissions to +x
chmod 700 ./scripts/devops-security-to-main.sh

# Only devops can run
