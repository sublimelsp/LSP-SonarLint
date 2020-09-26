# LSP-SonarLint

```
NOTE: Doesn't yet work on st4000-exploration
```

```
NOTE: Not an official SonarSource extension.
```

This package contains the SonarLint language server.

To use this package, you must have:
- The [LSP](https://packagecontrol.io/packages/LSP) package.
- Java in your $PATH

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
