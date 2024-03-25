#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge frontend-templates into frontend
git switch frontend-templates
git pull
git switch frontend
git pull
git merge frontend-templates
echo "Merged frontend-templates into frontend"
git commit -m "Merged frontend-templates into frontend"
git push

# Update permissions to +x
chmod 700 ./scripts/frontend-templates-to-frontend.sh

# Only devops can run
