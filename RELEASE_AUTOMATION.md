# PyEPISuite Release Automation - Quick Start

## 🎉 You now have fully automated releases!

Your repository now includes automated GitHub Actions workflows that will:

✅ **Build and test** your package automatically  
✅ **Publish to PyPI** using secure trusted publishing  
✅ **Create GitHub releases** with distribution files  
✅ **Generate release notes** from your changelog  

## Next Steps to Complete Setup

### 1. Set Up PyPI Trusted Publishing (Required)

Before your first automated release, you need to configure PyPI:

1. **Go to [PyPI.org](https://pypi.org)** and log in
2. **Navigate to your project** (create it first if needed): https://pypi.org/project/pyepisuite/
3. **Go to Settings → Publishing**
4. **Click "Add a new pending publisher"**
5. **Fill in exactly**:
   - **PyPI project name**: `pyepisuite`
   - **Owner**: `USEtox`
   - **Repository name**: `PyEPISuite`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`

⚠️ **Important**: The values must match exactly or publishing will fail.

### 2. Test the Release Process

Once PyPI is configured, test with a patch release:

```bash
# Option 1: Use the release script (recommended)
python scripts/release.py 1.0.1

# Option 2: Manual process
# Update versions in src/pyepisuite/__init__.py and pyproject.toml
# git add . && git commit -m "Bump version to 1.0.1"
# git tag -a v1.0.1 -m "Release 1.0.1"
# git push origin main && git push origin v1.0.1
```

### 3. Monitor the Release

After pushing a tag, monitor:

1. **GitHub Actions** tab to see workflows running
2. **Releases** tab for the created release
3. **PyPI** to confirm successful publishing

## How It Works

### When you push a version tag (e.g., `v1.0.1`):

1. **Test workflow** runs (tests, linting)
2. **Build workflow** creates wheel and source distribution
3. **PyPI workflow** publishes to PyPI automatically
4. **Release workflow** creates GitHub release with files
5. **Done!** Your package is live on PyPI and GitHub

### Files Created:

- `.github/workflows/release.yml` - Main release automation
- `.github/workflows/create-release.yml` - GitHub release creation
- `.github/workflows/test.yml` - Updated to run on releases
- `scripts/release.py` - Version management helper
- `.github/RELEASE.md` - Complete documentation

### Security Features:

- ✅ **No secrets needed** - Uses PyPI trusted publishing
- ✅ **Minimal permissions** - Workflows only get what they need
- ✅ **Audit trail** - All releases traceable through Git
- ✅ **Automated testing** - Won't release if tests fail

## Troubleshooting

If something goes wrong:

1. **Check GitHub Actions logs** in the Actions tab
2. **Verify PyPI trusted publishing** is configured correctly
3. **Check tag format** - must be `v*.*.*` (e.g., `v1.0.1`)
4. **Read `.github/RELEASE.md`** for detailed troubleshooting

## Version Management Best Practices

- **Patch releases** (1.0.0 → 1.0.1): Bug fixes
- **Minor releases** (1.0.0 → 1.1.0): New features
- **Major releases** (1.0.0 → 2.0.0): Breaking changes

Keep your `CHANGELOG.md` updated for automatic release notes!

---

🚀 **You're all set for automated releases!** Just set up PyPI trusted publishing and you can release with a single command.
