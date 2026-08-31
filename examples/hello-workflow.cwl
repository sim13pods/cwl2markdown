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
