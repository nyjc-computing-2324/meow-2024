#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Run frontend-templates-to-frontend.sh and frontend-layout-to-frontend.sh in the background
sh ./scripts/qa-backend-to-qa.sh
sh ./scripts/qa-frontend-to-qa.sh
sh ./scripts/dev-to-qa.sh
sh ./scripts/qa-to-qa-backend.sh
sh ./scripts/qa-to-qa-frontend.sh


echo "Both merges completed."