# Contributing to Guitar Tuner Web App

Thank you for your interest in contributing! 🎸

## How to Contribute

### Reporting Bugs
1. Check if the bug already exists in [Issues](https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB/issues)
2. Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
3. Provide:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (browser, OS, device)

### Suggesting Features
1. Check if the feature is already discussed in [Issues](https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB/issues)
2. Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
3. Describe:
   - What problem it solves
   - Why it's important
   - How it should work

### Submitting Code Changes

#### Setup Development Environment
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/PDS-Guitar-Tuner-WEB.git
cd PDS-Guitar-Tuner-WEB

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install flake8 pytest

# Create feature branch
git checkout -b feature/your-feature-name
```

#### Code Style
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep lines under 100 characters
- Comment complex logic

#### Testing
```bash
# Run linter
flake8 .

# Check syntax
python -m py_compile app.py src/core/*.py src/audio/*.py
```

#### Commit & Push
```bash
# Make your changes
git add .
git commit -m "feat: Add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

#### Submit Pull Request
1. Go to the repository
2. Click "Compare & pull request"
3. Provide:
   - Clear description of changes
   - Reference any related issues (#issue-number)
   - Screenshots if UI changes
4. Wait for review

## Commit Message Format

Use conventional commits:
```
feat:   New feature
fix:    Bug fix
docs:   Documentation changes
style:  Code style changes (formatting, etc)
refactor: Code refactoring
test:   Test changes
chore:  Build, dependencies, etc
```

Example:
```
feat: Add offline mode support

- Implement caching for frequency calculations
- Add offline indicator in UI
- Update documentation

Closes #123
```

## Pull Request Guidelines

- One feature per pull request
- Include tests if applicable
- Update documentation
- Link related issues
- Keep commits clean and organized
- Respond to review comments promptly

## Code Review Process

1. At least one maintainer review required
2. All checks must pass (linting, syntax)
3. Changes should not break existing features
4. Performance impact should be minimal

## Areas for Contribution

### High Priority
- [ ] Add unit tests
- [ ] Improve audio detection accuracy
- [ ] Add support for alternate tunings (Drop D, Baritone, 7-string)
- [ ] Mobile UI optimization
- [ ] Dark mode toggle

### Medium Priority
- [ ] Add tuning history/logs
- [ ] Implement preset profiles
- [ ] Add chord recognition
- [ ] Performance optimizations
- [ ] Documentation improvements

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional language support
- [ ] Social sharing features
- [ ] Gamification elements

## Questions?

- 💬 Open a [Discussion](https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB/discussions)
- 📧 Contact maintainers
- 📖 Check [DEPLOYMENT.md](DEPLOYMENT.md) for setup help

## Recognition

Contributors will be:
- Listed in README.md
- Credited in commit messages
- Featured in release notes

Thank you for helping improve Guitar Tuner! 🎵
