# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows semantic-style versioning where practical.

## [0.1.8] - 2026-05-07

### Added

- Added a refined project README with clearer architecture, lineage, and usage documentation.
- Added repository health files: `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md`.
- Added a simple SVG project logo for repository and package branding.

### Changed

- Renamed the project runtime, package, and CLI surface to `Essentials`.
- Reduced the repository to a smaller local-first agent core focused on terminal workflows.
- Simplified swarm execution to a subprocess-based worker path.
- Consolidated provider access around Anthropic and a single OpenAI-compatible client path.
- Improved documentation for configuration, project scope, and repository layout.

### Removed

- Removed product-specific surfaces outside the core agent runtime, including broader frontend and integration layers.
- Removed legacy compatibility paths and unused execution backends that were not part of the retained runtime.
- Removed the `image_to_text` fallback chain and its dedicated vision-model configuration path.

### Notes

- This release reflects a substantial repository reduction and cleanup intended
  to make Essentials easier to understand, maintain, and extend as a focused
  open-source agent runtime.
