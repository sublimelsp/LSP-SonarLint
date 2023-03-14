# LSP-SonarLint

```
NOTE: Not an official SonarSource extension.
```

This package contains the SonarLint language server.

To use this package, you must have:
- The [LSP](https://packagecontrol.io/packages/LSP) package.
- Java in your $PATH

## Installation (from source)

1. Run `make` to download and combine the files to a single zip.
2. Copy the files manually to your Sublime Text `Packages` directory, on mac this would be in `~/Library/Application Support/Sublime Text/Packages`
3. Restart Sublime Text.

## Applicable Selectors

SonarLint can lint various file types. The following [language IDs](https://github.com/sublimelsp/LSP/blob/st4000-exploration/language-ids.sublime-settings) are supported:

- java
- javascript
- javascriptreact
- php
- python
- typescript
- typescriptreact
- vue
- html
- jsp
- apex
- plsql
- oraclesql

## Configuration

Configure SonarLint by running `Preferences: LSP-SonarLint` from the command palette.

## Capabilities

SonarLint can only do linting. It doesn't provide completions, formatting, goto-def or code navigation.
