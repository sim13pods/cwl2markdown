{% macro serialize_clt(clt) -%}## {{clt.id}}

### CWL Class

[{{clt.class_}}](https://www.commonwl.org/{{clt.cwlVersion}}/{% if "ExpressionTool" == clt.class_ %}Workflow{% else %}{{clt.class_}}{% endif %}.html#{{clt.class_}})

### Inputs

| Id | Option | Type |
|----|------|-------|
{% for input in clt.inputs %}| `{{input.id}}` | `{% if input.inputBinding.prefix %}{{input.inputBinding.prefix}}{% else %}--{{input.id}}{% endif %}` | {{ type_to_string(input.type_, clt) }} |
{% endfor %}
{% if "CommandLineTool" == clt.class_ %}### Execution usage example:

```
{{clt | get_exection_command}} \
{% for input in clt.inputs %}{% if input.type_ is nullable %}({% endif %}{% if input.inputBinding.prefix %}{{input.inputBinding.prefix}}{% else %}--{{input.id}}{% endif %} <{{input.id.upper()}}>{% if input.type_ is nullable %}){% endif %}{% if not loop.last %} \{% endif %}
{% endfor %}```{% endif %}
{%- endmacro %}

{% macro serialize_workflow(workflow) -%}## {{workflow.id}}

### CWL Class

[{{workflow.class_}}](https://www.commonwl.org/{{workflow.cwlVersion}}/{{workflow.class_}}.html#{{workflow.class_}})

{% if workflow.requirements %}### Requirements
{% for requirement in workflow.requirements %}
* [{{requirement.class_}}](https://www.commonwl.org/{{workflow.cwlVersion}}/{{workflow.class_}}.html#{{requirement.class_}}){% endfor %}{% endif %}

### Inputs

| Id | Type | Label | Doc |
|----|------|-------|-----|
{% for input in workflow.inputs %}| `{{input.id}}` | {{ type_to_string(input.type_, workflow) }} | {{input.label}} | {{input.doc}} |
{% endfor %}

### Steps

| Id | Runs | Label | Doc |
|----|------|-------|-----|
{% for step in workflow.steps %}| [{{step.id}}](#{{step.run[1:]}}) | `{{step.run}}` | {{step.label}} | {{step.doc}} |
{% endfor %}

### Outputs

| Id | Type | Label | Doc |
|----|------|-------|-----|
{% for output in workflow.outputs %}| `{{output.id}}` | {{ type_to_string(output.type_, clt) }} | {{output.label}} | {{output.doc}} |
{% endfor %}

### OGC API - Processes

When `{{ workflow.id }}` [{{workflow.class_}}](https://www.commonwl.org/{{workflow.cwlVersion}}/{{workflow.class_}}.html#{{workflow.class_}}) is exposed through [OGC API - Processes - Part 1: Core](https://docs.ogc.org/is/18-062r2/18-062r2.html), `inputs` and `outputs` fields below represent the interface of the [getProcessDescription](https://developer.ogc.org/api/processes/index.html#tag/ProcessDescription/operation/getProcessDescription) API. 

{% set ogc_processes_kinds=['Inputs', 'Outputs'] %}
{% for ogc_processes_kind in ogc_processes_kinds %}
#### {{ogc_processes_kind}}

![{{workflow.id}} OGC API Processes JSON {{ogc_processes_kind}} schema](./{{workflow.id}}/ogc_processes_{{ogc_processes_kind | lower}}.svg "{{workflow.id}} {{diagram}} diagram")
{% endfor %}

### UML Diagrams
{% set diagrams=['Activity', 'Component', 'Class', 'Sequence', 'State'] %}
{% for diagram in diagrams %}
#### {{diagram}} diagram

Learn more about the [{{diagram}} diagram](https://en.wikipedia.org/wiki/{{diagram}}_diagram) below.

![{{workflow.id}} flow diagram](./{{workflow.id}}/{{diagram | lower}}.svg "{{workflow.id}} {{diagram}} diagram")
{% endfor %}

{% for step in workflow.steps %}### Run in step

`{{step.id}}`

{% set resolved_step = index.get(step.run[1:]) %}
{% if "Workflow" == resolved_step.class_ %}
{{serialize_workflow(resolved_step)}}
{% else %}
{{serialize_clt(resolved_step)}}
{% endif %}
{% endfor %}

{%- endmacro %}
