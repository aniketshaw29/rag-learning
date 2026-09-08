# TechNova — Product: NovaCode

## Overview

NovaCode is TechNova's flagship product — an AI-powered code assistant
that helps developers write, review, and understand code faster.

## Key Features

### 1. Real-Time Code Completion
- Suggests entire lines or blocks of code as you type
- Understands project context (imports, types, variable names)
- Supports 28 languages including Python, JavaScript, TypeScript, Go, Rust,
  Java, C++, and more
- Average suggestion latency: **45ms**

### 2. AI Code Review
- Automatically reviews pull requests for bugs, security issues, and style problems
- Categorizes findings by severity: Critical, Warning, Suggestion
- Integrates with GitHub, GitLab, and Bitbucket
- Can auto-fix many issues with one click

### 3. Natural Language to SQL
- Ask questions in plain English, get SQL queries
- Example: "Show me all users who signed up in the last 30 days and have
  an active subscription" → generates optimized PostgreSQL query
- Supports PostgreSQL, MySQL, SQLite, and Snowflake

### 4. Code Explanation
- Highlight any code block and ask "Explain this"
- Returns a step-by-step breakdown of what the code does
- Useful for understanding unfamiliar codebases

### 5. Refactoring Suggestions
- Detects code smells and suggests improvements
- Can refactor code to follow best practices
- Supports extract method, rename, inline, and move operations

## Pricing

| Plan       | Price    | Features                                    |
|------------|----------|---------------------------------------------|
| Free       | $0/mo    | Basic completions, 50 suggestions/day       |
| Pro        | $19/mo   | Unlimited completions, code review, NL2SQL  |
| Team       | $39/mo   | Everything in Pro + admin dashboard, SSO    |
| Enterprise | Custom   | On-premise deployment, custom models, SLA   |

## Usage Statistics (as of August 2025)

- **Monthly Active Users:** 123,400
- **Daily Active Users:** 41,200
- **Average suggestions per user per day:** 87
- **Most popular language:** Python (32%), followed by TypeScript (24%)
- **Customer satisfaction score:** 4.6 / 5.0
- **Net Promoter Score (NPS):** 62

## Known Limitations

1. **Context window:** NovaCode can only see the current file and open tabs.
   It does not understand the full project structure yet (planned for v3.0).
2. **Generated code accuracy:** ~92% for common patterns, drops to ~78% for
   complex business logic. Always review AI suggestions.
3. **Language support depth:** Python and TypeScript have the best support.
   Less popular languages (Haskell, Elixir) have basic completions only.
4. **Offline mode:** Not available. NovaCode requires an internet connection
   for inference.

## Recent Updates

### v2.8 (July 2025)
- Added support for Rust and Kotlin
- Improved suggestion accuracy by 12% with updated model
- Added "Accept All" button for multi-line suggestions

### v2.7 (May 2025)
- Launched Natural Language to SQL feature
- Added GitLab integration for code review
- Fixed memory leak in VS Code extension

### v2.6 (March 2025)
- Introduced team dashboard with usage analytics
- Added SSO support (SAML, OIDC)
- Reduced average suggestion latency from 68ms to 45ms
