<!--
Copyright 2026 Transpiler-Mate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# CWL 2 Markdown

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2markdown.svg)](https://pypi.org/project/cwl2markdown)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2markdown.svg)](https://pypi.org/project/cwl2markdown)

CWL to Markdown Transpiler-Mate plugin. It generates one Markdown page per CWL
workflow and renders document-level Schema.org `SoftwareApplication` metadata.

## Quick start

Install the plugin and runtime in the same Python environment:

```console
python -m pip install cwl2markdown transpiler-mate-runtime
```

Generate pages from a metadata-bearing CWL document:

```console
transpiler-mate cwl2markdown --output build/docs workflow.cwl
```

See the [first-steps tutorial](https://Transpiler-Mate.github.io/cwl2markdown/tutorials/first-steps/)
for a complete Schema.org metadata example.

## Project conventions

This project is templated a Hatch-based Python package with:

- Apache-2.0 license
- Keep a Changelog-compatible `CHANGELOG.md`
- Diátaxis documentation under `docs/`
- top-level `mkdocs.yaml`
- Taskfile integration with `Terradue/taskfile-utils`
- GitHub Actions CI

## Documentation

Project documentation is published at: https://Transpiler-Mate.github.io/cwl2markdown/

## Contribute

Submit a [Github issue](https://github.com/Transpiler-Mate/cwl2markdown/issues) if you have comments or suggestions.

### Local quality checks

Install [Hatch](https://hatch.pypa.io/) and [Taskfiles](https://taskfile.dev/docs/guide) then install the Git hook:

```console
task quality:pre-commit:install
```

Every commit runs Ruff (including the configured McCabe complexity limit),
Ruff formatting, strict mypy checks, and the pytest suite.

Run the complete hook explicitly with:

```console
task quality:pre-commit:run
```

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
