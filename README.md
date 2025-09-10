# LinkCheckMD - Markdown Link Checker

[![ci](https://github.com/scivision/linkchecker-markdown/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/linkchecker-markdown/actions/workflows/ci.yml)
[![PyPI Download stats](http://pepy.tech/badge/linkcheckmd)](http://pepy.tech/project/linkcheckmd)

> **Note**: This is a fork of [scivision/linkchecker-markdown](https://github.com/scivision/linkchecker-markdown) with additional domain exclusion functionality. All credit for the original implementation goes to the original maintainers.

A blazing-fast Python tool for checking links in Markdown files. Capable of processing 10,000+ Markdown files per second using high-performance asyncio and the [aiohttp](https://docs.aiohttp.org/) library.

**LinkCheckMD** is specifically designed for Markdown-based static site generators like Jekyll, Hugo, and MkDocs, providing fast and reliable link validation for documentation projects and static websites.

## Features

- ⚡ **Ultra-fast**: Asynchronous processing with configurable concurrency
- 🔗 **Comprehensive**: Checks both local and remote links
- 🎯 **Selective**: Filter by domain or exclude specific domains *(NEW in this fork)*
- 🛡️ **Robust**: Handles SSL verification, custom headers, and retry logic
- 📊 **Detailed**: Verbose output with timing information
- 🚀 **CI-ready**: Perfect for continuous integration pipelines
- 🔧 **Flexible**: Both Python API and command-line interface

## Installation

### Latest Release (PyPI)
```bash
pip install linkcheckmd
```

### Development Version
```bash
git clone https://github.com/scivision/linkchecker-markdown
pip install -e ./linkchecker-markdown
```

## Quick Start

### Command Line Usage
```bash
# Check all markdown files in current directory
python -m linkcheckmd .

# Check specific directory recursively
python -m linkcheckmd -r ./docs

# Exclude problematic domains
python -m linkcheckmd -r ./docs -e example.com -e slow-site.org

# Check only local files (skip remote URLs)
python -m linkcheckmd -local ./docs
```

### Python API
```python
import linkcheckmd as lc

# Basic usage
bad_links = lc.check_links("./docs")

# With domain exclusion
bad_links = lc.check_links("./docs", exclude_domains=["example.com", "test.org"])

# Local files only
local_issues = lc.check_local("./docs", ext=".md")
```

## Command Line Arguments

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `path` | Path to Markdown files | `./docs`, `~/website/content` |

### Optional Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `domain` | Check only links to specific domain | None | `github.com` |
| `-ext` | File extension to scan | `.md` | `-ext .markdown` |
| `-m, --method` | HTTP method (get/head) | `get` | `--method head` |
| `--headers` | Custom HTTP headers (JSON) | None | `--headers '{"User-Agent": "MyBot"}'` |
| `-v, --verbose` | Enable verbose output | False | `-v` |
| `--sync` | Use synchronous requests | False | `--sync` |
| `-local` | Check only local files | False | `-local` |
| `-r, --recurse` | Recurse subdirectories | False | `-r` |
| `-noverify` | Skip SSL certificate verification | False | `-noverify` |
| `-e, --exclude` | Exclude domains from checking | [] | `-e hashicorp.com -e terraform.io` |

## Detailed Usage Examples

### Basic Link Checking

```bash
# Check current directory
python -m linkcheckmd .

# Check specific directory
python -m linkcheckmd ./documentation

# Check with verbose output
python -m linkcheckmd -v ./docs
```

### Static Site Generators

```bash
# Jekyll
python -m linkcheckmd ~/website/_posts

# Hugo
python -m linkcheckmd ~/website/content

# MkDocs
python -m linkcheckmd ~/docs

# GitBook
python -m linkcheckmd ~/gitbook
```

### Domain Filtering

```bash
# Check only GitHub links
python -m linkcheckmd ./docs github.com

# Exclude multiple domains
python -m linkcheckmd -r ./docs -e hashicorp.com -e terraform.io -e slow-external-site.com

# Exclude domains with subdomains
python -m linkcheckmd ./docs -e reddit.com  # Excludes www.reddit.com, old.reddit.com, etc.
```

### Advanced Options

```bash
# Use HEAD requests for faster checking (may have false positives)
python -m linkcheckmd --method head ./docs

# Custom headers for sites requiring authentication
python -m linkcheckmd --headers '{"Authorization": "Bearer token123"}' ./docs

# Skip SSL verification for internal sites
python -m linkcheckmd -noverify ./internal-docs

# Use synchronous checking (slower but more predictable)
python -m linkcheckmd --sync ./docs
```

### Local File Checking Only

```bash
# Check only internal links (skip all HTTP/HTTPS)
python -m linkcheckmd -local ./docs

# Useful for offline development or testing internal structure
python -m linkcheckmd -local -r ./entire-project
```

## Domain Exclusion Feature

The `-e, --exclude` option allows you to skip link checking for specific domains. This is particularly useful for:

- **Known problematic sites**: Domains with anti-bot protection or rate limiting
- **Internal services**: Private or development domains not accessible during CI
- **Third-party dependencies**: External services outside your control
- **Performance optimization**: Skip slow or unreliable domains

### How It Works

Domain exclusion performs case-insensitive substring matching:

```bash
# This command
python -m linkcheckmd -e example.com ./docs

# Will skip these URLs:
# https://example.com/page
# https://www.example.com/api
# https://api.example.com/v1/data
# http://blog.example.com/post/123
```

### CI/CD Integration Examples

#### GitLab CI
```yaml
check-links:
  stage: test
  script:
    - pip install linkcheckmd
    - python -m linkcheckmd -r ./docs -e hashicorp.com -e terraform.io
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

#### GitHub Actions
```yaml
- name: Check Links
  run: |
    pip install linkcheckmd
    python -m linkcheckmd -r ./docs -e internal.company.com -e staging.example.org
```

#### Jenkins
```groovy
stage('Link Check') {
    steps {
        sh 'pip install linkcheckmd'
        sh 'python -m linkcheckmd -r ./docs -e dev.example.com'
    }
}
```

## Python API Reference

### Core Functions

#### `check_links(path, domain=None, **kwargs)`
Main function that checks both local and remote links.

**Parameters:**
- `path` (Path): Directory containing Markdown files
- `domain` (str, optional): Check only links to this domain
- `ext` (str): File extension to scan (default: ".md")
- `hdr` (dict, optional): Custom HTTP headers
- `method` (str): HTTP method - "get" or "head" (default: "get")
- `use_async` (bool): Use async processing (default: True)
- `local` (bool): Check only local files (default: False)
- `recurse` (bool): Recurse subdirectories (default: False)
- `ssl_verify` (bool): Verify SSL certificates (default: True)
- `exclude_domains` (list, optional): Domains to exclude from checking

**Returns:** List of bad links as tuples (file_path, url, error)

#### `check_local(path, ext=".md")`
Check only local/internal links within Markdown files.

**Parameters:**
- `path` (Path): Directory to scan
- `ext` (str): File extension to check

**Returns:** Generator of tuples (file_path, problematic_url)

#### `check_remotes(path, domain=None, **kwargs)`
Check only remote HTTP/HTTPS links.

**Parameters:** Same as `check_links()` but focuses on remote URLs only.

**Returns:** List of bad remote links

### Example Usage

```python
import linkcheckmd as lc
from pathlib import Path

# Basic check
docs_path = Path("./documentation")
issues = lc.check_links(docs_path)

# Advanced configuration
issues = lc.check_links(
    docs_path,
    exclude_domains=["internal.company.com", "dev.example.org"],
    method="head",  # Faster but less reliable
    ssl_verify=False,  # For internal sites
    recurse=True,  # Check subdirectories
    hdr={"User-Agent": "LinkChecker/1.0"}  # Custom headers
)

# Handle results
for file_path, url, error in issues:
    print(f"❌ {file_path}: {url} - {error}")

# Check only local links
local_issues = list(lc.check_local(docs_path))
for file_path, url in local_issues:
    print(f"🔗 Local link issue in {file_path}: {url}")
```

## Exit Codes

LinkCheckMD follows standard Unix conventions:

- **0**: Success - all links are valid
- **22**: Error - one or more links are broken (follows cURL convention)

This makes it perfect for CI/CD pipelines where you want builds to fail on broken links.

## Performance and Behavior

### Asynchronous Processing
- Uses `aiohttp` for concurrent HTTP requests
- Configurable timeout (10 seconds default)
- Automatic retry logic for transient failures
- Memory-efficient streaming for large sites

### Error Handling
- Distinguishes between network errors and HTTP errors
- Handles redirects automatically
- Graceful handling of SSL certificate issues
- Comprehensive logging with `-v` flag

### Output Format
- **stdout**: Broken links (for easy parsing)
- **stderr**: Debug information and warnings
- **Timing**: Execution time printed at completion

## Common Use Cases

### Documentation Teams
```bash
# Daily documentation health check
python -m linkcheckmd -r ./docs -e internal.company.com > broken-links.txt
```

### DevOps Integration
```bash
# Pre-deployment link validation
python -m linkcheckmd -r ./site-content -e staging.example.com -e dev.example.com
```

### Content Migration
```bash
# Check content after migration, excluding old domains
python -m linkcheckmd ./migrated-content -e old-site.com -e legacy.example.org
```

### Development Workflow
```bash
# Quick local check during development
python -m linkcheckmd -local ./docs  # Skip external links
```

## Troubleshooting

### Common Issues

**False Positives with HEAD Requests:**
```bash
# Solution: Use GET method (slower but more reliable)
python -m linkcheckmd --method get ./docs
```

**SSL Certificate Errors:**
```bash
# Solution: Disable SSL verification
python -m linkcheckmd -noverify ./docs
```

**Rate Limiting:**
```bash
# Solution: Exclude problematic domains
python -m linkcheckmd -e rate-limited-site.com ./docs
```

**Slow External Sites:**
```bash
# Solution: Use domain exclusion
python -m linkcheckmd -e slow-site.org -e another-slow-site.com ./docs
```

### Debugging

Enable verbose output to see what's happening:
```bash
python -m linkcheckmd -v ./docs
```

This shows:
- URLs being checked in real-time
- Success confirmations
- Detailed error messages
- Performance timing

## Alternatives

While LinkCheckMD is optimized for Markdown files, consider these alternatives for different use cases:

- **[htmltest](https://github.com/wjdp/htmltest)**: Go-based, works with HTML files
- **[GitHub Action](https://github.com/marketplace/actions/markdown-link-check)**: For GitHub-hosted projects
- **[Netlify Plugin](https://github.com/munter/netlify-plugin-checklinks)**: For Netlify deployments
- **Browser-based tools**: For JavaScript-heavy sites requiring full rendering

## Contributing

This fork adds domain exclusion functionality to the original [scivision/linkchecker-markdown](https://github.com/scivision/linkchecker-markdown) project. 

For contributions to the core functionality, please consider contributing to the upstream project. For issues or improvements specific to the domain exclusion feature, contributions are welcome!

Areas for improvement:

- Additional output formats (JSON, XML)
- Better regex patterns for edge cases
- Performance optimizations
- Additional authentication methods
- Support for more file formats

## Credits

- **Original Project**: [scivision/linkchecker-markdown](https://github.com/scivision/linkchecker-markdown)
- **Domain Exclusion Feature**: Added in this fork for CI/CD workflows that need to skip specific domains

## License

See [LICENSE.txt](LICENSE.txt) for details.