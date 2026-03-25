# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-03-25

### Added
- Initial release of PentOps
- CLI with 16+ modules for pentesting automation
- Workflow engine with YAML-based automation
- Integration with external APIs (Shodan, VirusTotal, ExploitDB, HaveIBeenPwned)
- Auto-detection module for intelligent vulnerability scanning
- Credential harvesting guides
- WiFi pentesting module
- Active Directory pentesting module
- Advanced reporting (HTML/Markdown)
- Multiple workflow templates (hybrid, quick, advanced)

### Infrastructure
- GitHub Actions CI/CD pipeline
- Pre-commit hooks (ruff, mypy, pre-commit-hooks)
- Type hints for core modules (config.py, utils.py)
- Logging infrastructure (Python logging module)

## [1.0.1] - Unreleased

### Added
- Extended type hints coverage
- Better error handling and logging

### Fixed
- Typo in config.py (extra space in tool name)
- Bare except clause in utils.py
- Added .gitignore
