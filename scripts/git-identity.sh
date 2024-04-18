#!/nix/store/3x9jq3l68vxy0ap48xy500g6czvzavhm-bash/bin/bash

# Function to configure Git identity
configure_git_identity() {
    echo "Git committer identity is not configured."
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email

    # Configure Git identity
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
}

# Check if committer identity is configured
git_name=$(git config user.name)
git_email=$(git config user.email)

if [ -z "$git_name" ] || [ -z "$git_email" ]; then
    configure_git_identity
fi

# update permission to x+
chmod 700 ./scripts/git-identity.sh