# harbormaster
Light weight API based AI Model Security tool

Project Structure
LLMGuardian follows a modular and secure architecture designed to provide comprehensive protection for LLM applications. Below is the detailed project structure with explanations for each component:

Directory Structure
```
LLMGuardian/
├── .github/                      # GitHub specific configurations
│   ├── workflows/                # GitHub Actions workflows
│   ├── CODEOWNERS               # Repository ownership rules
│   ├── ISSUE_TEMPLATE/          # Issue reporting templates
│   └── PULL_REQUEST_TEMPLATE.md # PR guidelines
├── .circleci/                   # config files for using CircleCI https://circleci.com/ 
│
├── src/                         # Source code
│   └── llmguardian/            # Main package directory
│       ├── cli/                # Command-line interface
│       ├── dashboard/          # Streamlit dashboard
│       ├── core/               # Core functionality
│       ├── scanners/           # Security scanning modules
│       ├── defenders/          # Defense mechanisms
│       ├── monitors/           # Monitoring components
│       ├── api/                # API integration
|       ├── vectors/            # Embeddings protection / supply chain vulnerabilities
|       ├── data/               # Sensive data exposure / data poisoning
|       ├── agency/             # Excessive agency protection
│       └── utils/              # Utility functions
│
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── security/              # Security-specific tests
│
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── requirements/              # Dependencies
├── docker/                    # Docker configurations
└── config/                    # Various config files
Component Details
Security Components
Scanners (src/llmguardian/scanners/)

Prompt injection detection
Data leakage scanning
Model security validation
Output validation checks
Defenders (src/llmguardian/defenders/)

Input sanitization
Output filtering
Rate limiting
Token validation
Monitors (src/llmguardian/monitors/)

Real-time usage tracking
Threat detection
Anomaly monitoring
Vectors (src/llmguardian/vectors/)

Embedding weaknesses
Supply chain vulnerabilities
Montior vector stores
Data (src/llmguardian/data/)

Sensitive information disclosure
Protection from data poisoning
Data sanitizing
Agency (src/llmguardian/agency/)

Permission management
Scope limitation
Safe execution
Core Components
CLI (src/llmguardian/cli/)

Command-line interface
Interactive tools
Configuration management
API (src/llmguardian/api/)

RESTful endpoints
Middleware
Integration interfaces
Core (src/llmguardian/core/)

Configuration management
Logging setup
Core functionality
Testing & Quality Assurance
Tests (tests/)
Unit tests for individual components
Integration tests for system functionality
Security-specific test cases
Vulnerability testing
Documentation & Support
Documentation (docs/)
API documentation
Implementation guides
Security best practices
Usage examples
Docker (docker/)
Containerization support
Development environment
Production deployment
Development Tools
Scripts (scripts/)
Setup utilities
Development tools
Security checking scripts
Dashboard
Dashboard(src/llmguardian/dashboard/)
Streamlit app
Visualization
Monitoring and control
Key Files
pyproject.toml: Project metadata and dependencies
setup.py: Package setup configuration
requirements/*.txt: Environment-specific dependencies
.pre-commit-config.yaml: Code quality hooks
CONTRIBUTING.md: Contribution guidelines
LICENSE: MIT license terms
Design Principles
The structure follows these key principles:

Modularity: Each component is self-contained and independently maintainable
Security-First: Security considerations are built into the architecture
Scalability: Easy to extend and add new security features
Testability: Comprehensive test coverage and security validation
Usability: Clear organization and documentation

```
@misc{lightweightapibasedaimodelsecuritytool,
      title={Harbormaster}, 
      author={Safe-Harbor-Cybersecurity, DeWitt Gibson},
      year={2025},
      eprint={null},
      archivePrefix={null},
      primaryClass={null},
      url={[https://github.com/Safe-Harbor-Cybersecurity/harbormaster](https://github.com/Safe-Harbor-Cybersecurity/harbormaster)}, 
}
```
