#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge dev into frontend
git switch dev
git pull
git switch frontend
git pull
git merge dev
echo "Merged dev into frontend"
git commit -m "Merged dev into frontend"
git push

# Update permissions to +x
chmod 700 ./scripts/dev-to-frontend.sh

# Only devops can run
