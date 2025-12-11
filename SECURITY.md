# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Modal LLM Evaluator seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before we've had a chance to address it
- Exploit the vulnerability beyond what is necessary to demonstrate it

### Please Do

**Report security vulnerabilities to: hello@gtmvp.com**

Please include the following information in your report:

- Type of vulnerability (e.g., API key exposure, injection attack, etc.)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

### What to Expect

1. **Acknowledgment**: We'll acknowledge receipt of your vulnerability report within 48 hours
2. **Communication**: We'll keep you informed about our progress addressing the vulnerability
3. **Disclosure**: We'll work with you to understand the issue and determine an appropriate disclosure timeline
4. **Credit**: We'll credit you in our security advisory (unless you prefer to remain anonymous)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies by severity
  - Critical: 1-7 days
  - High: 7-30 days
  - Medium: 30-90 days
  - Low: Best effort

## Security Best Practices

When using Modal LLM Evaluator, follow these security guidelines:

### API Key Management

- **Never commit API keys** to version control
- Use Modal secrets for storing API keys: `python -m modal secret create`
- Rotate API keys regularly
- Use separate API keys for development and production
- Set appropriate permissions and usage limits on API keys

### Environment Variables

- Store sensitive configuration in `.env` files (included in `.gitignore`)
- Use Modal secrets for cloud deployment
- Never log or print API keys or other sensitive data

### Email Configuration

- Use app-specific passwords, not your main email password
- Enable 2FA on email accounts used for notifications
- Limit SMTP credentials to minimum required permissions
- Consider using dedicated email service (Brevo, SendGrid) instead of personal email

### Budget Limits

- Always set budget limits when running evaluations
- Monitor costs regularly
- Use test/sandbox API keys for development
- Start with small-scale tests before running large evaluations

### Data Privacy

- Be cautious about what test data you include in evaluations
- Don't include PII (Personally Identifiable Information) in test cases
- Review results before sharing to ensure no sensitive data is exposed
- Be aware that LLM providers may log your prompts and responses

### Code Security

- Keep dependencies up to date
- Review third-party packages before installation
- Use virtual environments to isolate dependencies
- Run security scans with tools like `bandit` and `safety`

## Known Security Considerations

### LLM API Keys

This project requires API keys from LLM providers (Anthropic, OpenAI, Google). These keys:

- Provide access to paid services
- Should be treated as highly sensitive credentials
- Can incur significant costs if compromised
- Should never be hardcoded in source code

### Email Credentials

SMTP credentials used for email notifications:

- Provide access to send emails from your account
- Should use app-specific passwords when possible
- Should be stored in Modal secrets or environment variables
- Should have appropriate rate limiting configured

### Result Files

Evaluation results may contain:

- Test prompts and responses
- Cost information
- Model performance data
- Potentially sensitive test cases

Ensure proper access controls on result files, especially when shared publicly.

## Dependency Security

We regularly update dependencies to address security vulnerabilities. To check for updates:

```bash
# Check for outdated packages
pip list --outdated

# Check for known vulnerabilities
pip install safety
safety check
```

## Secure Development

Contributors should follow secure coding practices:

- Input validation for all user-provided data
- Proper error handling without exposing sensitive information
- Secure file operations (path traversal prevention)
- SQL injection prevention (when database features are added)
- XSS prevention in UI components

## Security Updates

Security updates will be:

- Released as patch versions (e.g., 1.0.1, 1.1.3)
- Announced in release notes
- Published in GitHub Security Advisories
- Communicated via email to affected users when possible

## Vulnerability Disclosure Policy

Once a security vulnerability has been fixed:

1. We'll publish a security advisory on GitHub
2. We'll credit the researcher (unless they prefer anonymity)
3. We'll provide details about the vulnerability and the fix
4. We'll recommend upgrade paths for affected users

## Bug Bounty Program

We currently do not offer a bug bounty program. However, we greatly appreciate responsible disclosure and will:

- Publicly acknowledge your contribution
- Include you in our security hall of fame (if you wish)
- Provide a reference letter for your work (upon request)

## Contact

- **Security Issues**: hello@gtmvp.com
- **General Support**: hello@gtmvp.com
- **GitHub Issues**: https://github.com/GTMVP/modal-llm-evaluator/issues (for non-security bugs)

## Responsible Disclosure

We follow responsible disclosure principles and request that security researchers do the same. We commit to:

- Responding promptly to vulnerability reports
- Keeping reporters informed of our progress
- Crediting reporters appropriately
- Working collaboratively to address issues

Thank you for helping keep Modal LLM Evaluator and our users safe!
