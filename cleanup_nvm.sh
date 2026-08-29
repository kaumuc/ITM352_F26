#!/bin/bash

# Cleanup and reinstall Node.js NVM (Node Version Manager)
# This script demonstrates safe destructive operations with verification

set -e  # Exit on error

# Configuration
NVM_DIR="${HOME}/.nvm"
BACKUP_DIR="${HOME}/.nvm_backup_$(date +%Y%m%d_%H%M%S)"
NODE_VERSION="v20.10.0"
SHELL_CONFIGS=("${HOME}/.bashrc" "${HOME}/.zshrc" "${HOME}/.bash_profile")

# Color for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== NVM Cleanup and Reinstall Script ===${NC}"
echo ""

# STEP 1: VERIFICATION - Show what will be deleted
echo -e "${YELLOW}STEP 1: Identifying files to remove...${NC}"

if [ -d "$NVM_DIR" ]; then
    echo -e "${RED}Directory to remove: $NVM_DIR${NC}"
    echo "Contents:"
    du -sh "$NVM_DIR"
    find "$NVM_DIR" -type f | head -20
    echo ""
else
    echo -e "${GREEN}✓ NVM directory not found (already clean)${NC}"
fi

echo -e "${YELLOW}Shell config files to modify:${NC}"
for config in "${SHELL_CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        echo "  - $config"
        # Show lines containing nvm
        if grep -q "nvm" "$config" 2>/dev/null; then
            echo "    Found nvm references:"
            grep "nvm" "$config" | head -3
        fi
    fi
done
echo ""

# STEP 2: USER CONFIRMATION - Critical safety check
echo -e "${RED}WARNING: This will DELETE:${NC}"
echo "  1. $NVM_DIR and all contents"
echo "  2. NVM references from shell config files"
echo ""
echo -e "${YELLOW}A backup will be created at: $BACKUP_DIR${NC}"
read -p "Do you want to proceed? (type 'YES' to confirm): " confirmation

if [ "$confirmation" != "YES" ]; then
    echo -e "${RED}Operation cancelled.${NC}"
    exit 1
fi

echo ""

# STEP 3: BACKUP - Never delete without backup
echo -e "${YELLOW}STEP 2: Creating backup...${NC}"
if [ -d "$NVM_DIR" ]; then
    cp -r "$NVM_DIR" "$BACKUP_DIR"
    echo -e "${GREEN}✓ Backup created at: $BACKUP_DIR${NC}"
fi
echo ""

# STEP 4: REMOVE - The destructive part
echo -e "${YELLOW}STEP 3: Removing NVM...${NC}"
if [ -d "$NVM_DIR" ]; then
    rm -rf "$NVM_DIR"
    echo -e "${GREEN}✓ Removed $NVM_DIR${NC}"
fi

# Remove from PATH
export PATH=$(echo $PATH | tr ':' '\n' | grep -v "\.nvm" | paste -sd ':' -)
echo -e "${GREEN}✓ Updated PATH${NC}"
echo ""

# STEP 5: CLEAN SHELL CONFIGS - Pattern-based modification
echo -e "${YELLOW}STEP 4: Removing NVM references from shell configs...${NC}"
for config in "${SHELL_CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        # Create backup before modifying
        cp "$config" "${config}.bak_before_nvm_cleanup"
        
        # Remove lines containing nvm export/source commands
        grep -v "nvm\|NVM" "$config" > "${config}.tmp" && mv "${config}.tmp" "$config"
        
        echo -e "${GREEN}✓ Cleaned: $config${NC}"
    fi
done
echo ""

# STEP 6: REINSTALL - Conditional reinstall based on cleanup success
echo -e "${YELLOW}STEP 5: Reinstalling NVM...${NC}"

if [ ! -d "$NVM_DIR" ]; then
    # Install NVM
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    
    # Source NVM
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    # Install specific Node version
    nvm install "$NODE_VERSION"
    nvm use "$NODE_VERSION"
    
    echo -e "${GREEN}✓ NVM reinstalled with Node $NODE_VERSION${NC}"
    echo "Node version: $(node --version)"
else
    echo -e "${RED}✗ NVM directory still exists. Something went wrong.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Cleanup and reinstall completed successfully! ===${NC}"
echo -e "${YELLOW}Backup location: $BACKUP_DIR${NC}"
echo "To restore from backup if needed:"
echo "  rm -rf $NVM_DIR && cp -r $BACKUP_DIR $NVM_DIR"
