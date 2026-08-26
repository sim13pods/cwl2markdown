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

CWL 2 Markdown is a Transpiler-Mate plugin that creates Markdown pages for CWL
workflows and includes project information from document-level Schema.org
metadata.

Use these docs by intent:

- [Tutorials](tutorials/index.md): learn by completing a guided path.
- [How-to guides](how-to/index.md): solve specific tasks.
- [Reference](reference/index.md): look up commands, APIs, and configuration.
- [Explanation](explanation/index.md): understand design decisions and concepts.

## Quick start

```console
python -m pip install cwl2markdown transpiler-mate-runtime
transpiler-mate cwl2markdown --output build/docs workflow.cwl
```

Start with the [guided tutorial](tutorials/first-steps.md) for a complete,
working CWL example.
