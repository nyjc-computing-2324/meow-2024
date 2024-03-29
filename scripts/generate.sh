#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Function to generate merge script
generate_merge_script() {
    source_branch=$1
    target_branch=$2
    script_name="scripts/${source_branch}-to-${target_branch}.sh"

    cat << EOF > "$script_name"
#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Import git identity check
sh ./scripts/git-identity.sh

# Merge $source_branch into $target_branch
git switch $source_branch
git pull
git switch $target_branch
git pull
git merge $source_branch
echo "Merged $source_branch into $target_branch"
git commit -m "Merged $source_branch into $target_branch"
git push

# Update permissions to +x
chmod 700 ./$script_name

# Only devops can run
EOF

    chmod +x "$script_name"
}

# Generate merge scripts for different scenarios
generate_merge_script "main" "dev"
generate_merge_script "dev" "main"
generate_merge_script "dev" "frontend"
generate_merge_script "frontend" "dev"
generate_merge_script "frontend" "frontend-templates"
generate_merge_script "frontend-templates" "frontend"
generate_merge_script "frontend" "frontend-layout"
generate_merge_script "frontend-layout" "frontend"
generate_merge_script "dev" "backend"
generate_merge_script "backend" "dev"
generate_merge_script "backend" "backend-routing"
generate_merge_script "backend-routing" "backend"
generate_merge_script "backend" "backend-database"
generate_merge_script "backend-database" "backend"
generate_merge_script "dev" "qa"
generate_merge_script "qa" "dev"
generate_merge_script "qa" "qa-frontend"
generate_merge_script "qa-frontend" "qa"
generate_merge_script "qa" "qa-backend"
generate_merge_script "qa-backend" "qa"
generate_merge_script "main" "devops-security"
generate_merge_script "devops-security" "main"

# End of script

echo "Merge scripts generated successfully."
ls -l scripts/*.sh