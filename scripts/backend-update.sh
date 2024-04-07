#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash


sh ./scripts/backend-routing-to-backend.sh 
sh ./scripts/backend-database-to-backend.sh 
sh ./scripts/dev-to-backend.sh
sh ./scripts/backend-to-backend-routing.sh 
sh ./scripts/backend-to-backend-database.sh 


echo "Both merges completed."