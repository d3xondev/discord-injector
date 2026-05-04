#!/usr/bin/env bash
# Instant static cross-compile using GitHub Actions
# No MinGW download needed - builds on GitHub's Windows runners

set -e

echo "═══════════════════════════════════════════════════════"
echo "Discord Token Injector - GitHub Actions Build"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "[-] Git not found. Install git first:"
    echo "    sudo pacman -S git"
    exit 1
fi

# Initialize git repo if needed
if [ ! -d .git ]; then
    echo "[*] Initializing git repository..."
    git init
    git add discord.py build_static.py .github/
    git commit -m "Initial commit" || true
fi

# Add GitHub secret for releases (optional)
echo "[*] To enable automatic releases, add GitHub token as secret:"
echo "    1. Go to https://github.com/[your-username]/[repo-name]/settings/secrets"
echo "    2. Create new secret 'GITHUB_TOKEN' with your GitHub token"
echo ""

echo "[+] GitHub Actions workflow created at: .github/workflows/build-windows.yml"
echo "[+] The Windows EXE will be built automatically on:"
echo "    - Every push to main branch"
echo "    - Or manually via GitHub Actions tab"
echo ""
echo " [*] SETUP STEPS:"
echo "    1. Create GitHub account (free): https://github.com"
echo "    2. Create new repository"
echo "    3. Push this code:"
echo "       git remote add origin https://github.com/[your-username]/[repo-name].git"
echo "       git branch -M main"
echo "       git push -u origin main"
echo "    4. Go to Actions tab and enable workflows"
echo "    5. Wait for build to complete (~2-3 minutes)"
echo "    6. Download DiscordInjector.exe from artifacts"
echo ""
echo "═══════════════════════════════════════════════════════"
