#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge main into devops-security
git switch main
git pull
git switch devops-security
git pull
git merge main
echo "Merged main into devops-security"
git commit -m "Merged main into devops-security"
git push

# Update permissions to +x
chmod 700 ./scripts/main-to-devops-security.sh

# Only devops can run
