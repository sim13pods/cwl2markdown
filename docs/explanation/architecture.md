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

# Architecture

`cwl2markdown` is an installed Transpiler-Mate plugin, not a standalone CLI.
Its package entry point registers the `cwl2markdown` command with the runtime.

When a command runs, the runtime loads the CWL source, resolves its graph, and
converts preserved document-level Schema.org JSON-LD into a validated
`SoftwareApplication`. The plugin then:

1. selects the requested process, or all processes when no fragment is given;
2. retains only CWL `Workflow` processes;
3. renders the packaged Jinja templates for each workflow; and
4. writes `<workflow-id>.md` in the configured output directory.

The main template combines two sections. `metadata.md` renders the
`SoftwareApplication` fields, including the team, license, help, and runtime
requirements. `workflow.md` renders the CWL workflow interface and recursively
describes processes referenced by its steps.

Type links in the generated page point to the CWL v1.2 specification. The page
also contains placeholders for OGC API - Processes schemas and UML diagrams;
the plugin links to those SVG assets but does not generate them.
