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

# Use the command line

Invoke the installed plugin through the Transpiler-Mate runtime:

```console
transpiler-mate cwl2markdown [OPTIONS] SOURCE
```

For example:

```console
transpiler-mate cwl2markdown --output build/docs workflow.cwl
```

`SOURCE` is a CWL location understood by the runtime. It may be a local path or
a supported URL. Append `#PROCESS_ID` to select one process from a CWL graph:

```console
transpiler-mate cwl2markdown \
  --output build/docs \
  'workflow.cwl#main'
```

The selected process must be a `Workflow`. Without a fragment, the plugin
creates one `<workflow-id>.md` file for every workflow and ignores other process
types. It creates `--output` when the directory does not exist.

## Plugin options

| Option | Required | Default | Description |
| --- | --- | --- | --- |
| `--output PATH` | No | `.` | Directory in which Markdown pages are created. |
| `--code-repository TEXT` | No | — | Repository URL accepted by the current options model. It does not currently change the rendered page. |

The runtime also exposes source-access options for OCI credentials and an
OAuth 2 bearer token. Run the installed command's help to see the complete
interface:

```console
transpiler-mate cwl2markdown --help
```

## Metadata requirements

The CWL document must contain Schema.org metadata at document level and define
its prefix in `$namespaces`:

```yaml
$namespaces:
  s: https://schema.org/
s:name: Example workflow
```

The runtime validates this metadata as a `SoftwareApplication`. The fields used
by the Markdown template are `name`, `description`, `dateCreated`, `license`,
`softwareVersion`, `softwareHelp`, `publisher`, `author`, `contributor`,
`operatingSystem`, and `softwareRequirements`. See the complete
[working example](../examples/hello-workflow.cwl).
