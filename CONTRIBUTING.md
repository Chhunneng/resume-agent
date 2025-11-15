# Contributing to Resume Agent

Thank you for your interest in contributing to Resume Agent! This document provides guidelines for contributing to the project.

## Commit Message Convention

We follow the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification to maintain a consistent and meaningful commit history. This convention enhances readability and facilitates automated tooling.

### Commit Message Structure

Each commit message should follow this structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

The `<type>` field describes the nature of the change:

- **`feat`**: Introduces a new feature (corresponds to a MINOR version increment in Semantic Versioning)
- **`fix`**: Patches a bug (corresponds to a PATCH version increment)
- **`docs`**: Documentation changes only
- **`style`**: Code style changes (formatting, missing semicolons, etc.) that do not affect functionality
- **`refactor`**: Code changes that neither fix a bug nor add a feature
- **`perf`**: Performance improvements
- **`test`**: Adding or correcting tests
- **`build`**: Changes to build system or external dependencies
- **`ci`**: Changes to CI configuration files and scripts
- **`chore`**: Maintenance tasks (e.g., build process updates, dependency management)
- **`revert`**: Reverts a previous commit

### Scope

The `[optional scope]` provides context about the part of the codebase affected. Common scopes include:

- **Backend**: `backend`, `api`, `auth`, `database`, `migration`
- **Frontend**: `frontend`, `ui`, `components`, `hooks`
- **Infrastructure**: `docker`, `ci`, `deps`

### Description

The `<description>` should be:
- Written in imperative mood ("add feature" not "added feature" or "adds feature")
- Lowercase (except for proper nouns)
- No period at the end
- Concise but descriptive

### Body

The `[optional body]` provides additional context:
- Explains the "what" and "why" of the change
- Can include multiple paragraphs
- Each line should be wrapped at 72 characters

### Footer

The `[optional footer(s)]` can include:
- Breaking changes (see below)
- Issue references (e.g., `Closes #123`, `Fixes #456`)

### Breaking Changes

If a commit introduces a breaking change, include a `BREAKING CHANGE:` section in the body or footer:

```
BREAKING CHANGE: description of the breaking change
```

This indicates that the change is not backward-compatible and may require users to take action.

## Examples

### Adding a New Feature

```
feat(auth): add OAuth2 authentication support

Introduce OAuth2 authentication to enhance security and support
multiple authentication providers including Google and GitHub.

Closes #42
```

### Fixing a Bug

```
fix(api): resolve null pointer exception in user service

Addressed a null pointer exception that occurred when retrieving
user profiles without an email address. Added proper null checks
and default value handling.

Fixes #78
```

### Documentation Update

```
docs(readme): update installation instructions

Clarified the installation steps to include dependency requirements
and setup configurations for both Docker and manual setup.
```

### Code Refactoring

```
refactor(backend): improve error handling in resume service

Extracted error handling logic into separate utility functions to
improve code reusability and maintainability.
```

### Style Changes

```
style(frontend): format components with Prettier

Applied Prettier formatting to all React components to ensure
consistent code style across the frontend codebase.
```

### Performance Improvement

```
perf(api): optimize database query for job applications

Reduced query time by 60% by adding proper database indexes and
optimizing the join operations in the job application endpoint.
```

### Adding Tests

```
test(backend): add unit tests for skill analysis service

Added comprehensive unit tests covering edge cases and error
scenarios for the skill analysis functionality.
```

### Breaking Change

```
refactor(api): update response format structure

Standardized the API response format to improve consistency
across all endpoints.

BREAKING CHANGE: The 'data' field is now nested under 'result'
in all API responses. Update your API clients accordingly.
```

### Chore/Maintenance

```
chore(deps): update FastAPI to version 0.121.0

Updated FastAPI dependency to the latest version to include
security patches and performance improvements.
```

### Reverting a Commit

```
revert: revert "feat(auth): add OAuth2 support"

This reverts commit abc123def456 due to compatibility issues
with the current authentication system.

Refs #123
```

## Best Practices

1. **Keep commits focused**: Each commit should represent a single logical change
2. **Write clear descriptions**: The description should clearly explain what the commit does
3. **Use scopes appropriately**: Include scope when it adds meaningful context
4. **Reference issues**: Link commits to related issues when applicable
5. **Review before committing**: Ensure your commit message follows the convention

## Additional Resources

- [Conventional Commits 1.0.0 Specification](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning](https://semver.org/)

## Getting Started

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes following the code style guidelines
4. Write tests for new features
5. Ensure all tests pass
6. Commit your changes using the Conventional Commits format
7. Push to your fork and create a pull request

Thank you for contributing to Resume Agent!

