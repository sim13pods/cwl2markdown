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

# Generate your first Markdown page

This tutorial generates Markdown documentation for a CWL workflow whose
document-level metadata describes a Schema.org `SoftwareApplication`.

## 1. Install the runtime and plugin

Create and activate a virtual environment, then install both packages:

```console
python -m venv .venv
source .venv/bin/activate
python -m pip install cwl2markdown transpiler-mate-runtime
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead.

Confirm that the runtime discovered the plugin:

```console
transpiler-mate cwl2markdown --help
```

## 2. Create a metadata-bearing CWL workflow

Save the following as `hello-workflow.cwl` (it is also available as a
[documentation example](../examples/hello-workflow.cwl)):

```yaml
cwlVersion: v1.2
class: Workflow
$namespaces:
  s: https://schema.org/
s:name: Hello workflow
s:description: Run a tool that prints a greeting.
s:dateCreated: "2026-08-26"
s:license:
  s:name: Apache License 2.0
  s:url: https://www.apache.org/licenses/LICENSE-2.0
  s:identifier: Apache-2.0
s:softwareVersion: 1.0.0
s:operatingSystem:
  - Linux
  - macOS
s:softwareRequirements:
  - https://www.commonwl.org/
  - https://www.python.org/
s:softwareHelp:
  s:name: Hello workflow documentation
  s:url: https://example.org/hello/help
s:publisher:
  s:name: Example organization
  s:email: info@example.org
s:author:
  s:givenName: Ada
  s:familyName: Lovelace
  s:email: ada@example.org
  s:identifier: https://orcid.org/0000-0000-0000-0000
  s:affiliation:
    s:name: Example organization
    s:identifier: https://example.org/
$graph:
  - id: hello-workflow
    class: Workflow
    label: Hello workflow
    doc: Pass a message to the hello command-line tool.
    inputs:
      message:
        type: string
        label: Message
        doc: Greeting text to print.
    outputs: []
    steps:
      hello:
        run: "#hello-tool"
        in:
          message: message
        out: []
  - id: hello-tool
    class: CommandLineTool
    baseCommand: echo
    inputs:
      message:
        type: string
        inputBinding:
          position: 1
    outputs: []
```

`$namespaces` defines the `s` prefix. The `s:*` properties are document-level
metadata around `$graph`; the runtime preserves and validates them as a
Schema.org `SoftwareApplication` before the plugin runs. The graph must contain
at least one `Workflow`, because standalone `CommandLineTool` processes are not
rendered as pages.

## 3. Generate the page

Run the plugin through Transpiler-Mate:

```console
transpiler-mate cwl2markdown --output build/docs hello-workflow.cwl
```

The plugin creates the output directory and writes one page for every workflow
in the document. For this example, the result is:

```text
build/docs/hello-workflow.md
```

The page combines the Schema.org project information with the workflow inputs,
steps, outputs, and referenced command-line tools.

To render only one workflow from a graph, append its process ID to the source:

```console
transpiler-mate cwl2markdown \
  --output build/docs \
  'hello-workflow.cwl#hello-workflow'
```

## Next steps

- Review all [command options](../how-to/use-cli.md).
- Read how the [plugin processes a document](../explanation/architecture.md).
