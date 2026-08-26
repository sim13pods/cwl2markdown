{% include "metadata.md" %}

---

{% import "workflow.md" as wf with context %}
{{wf.serialize_workflow(workflow)}}
