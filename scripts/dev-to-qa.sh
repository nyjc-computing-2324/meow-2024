#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge dev into qa
git switch dev
git pull
git switch qa
git pull
git merge dev
echo "Merged dev into qa"
git commit -m "Merged dev into qa"
git push

# Update permissions to +x
chmod 700 ./scripts/dev-to-qa.sh

# Only devops can run
