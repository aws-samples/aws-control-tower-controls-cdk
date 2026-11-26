# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Security
- Scope the sample IAM policy write and delete actions to specific enabled control, organization policy, root, and OU ARNs
- Add an `aws:PrincipalOrgID` condition to the sample trust policy and remove the empty `Condition` block
- Replace hardcoded account IDs in the README examples with placeholders
- Upgrade Python dependencies and the AWS CDK CLI to fix known vulnerabilities
- Remove the `urllib3<2` constraint and pin `cdk-nag<3` to keep the `Aspects` API
- Replace `safety` with `pip-audit` for dependency vulnerability checks

## [2.0.0] - 2024-12-19
### Breaking Changes
- Migration from regional to global API identifiers

## [1.0.0] - 2023-06-22
### Added
- Initial public release
