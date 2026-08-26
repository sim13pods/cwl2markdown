# {{software_application.name}} v{{software_application.software_version}}

{{software_application.description}}

> This software is licensed under the terms of the [{{software_application.license.name}}]({{software_application.license.url}}) license - SPDX short identifier: [{{software_application.license.identifier}}](https://spdx.org/licenses/{{software_application.license.identifier}})
>
> {{software_application.date_created}} - {{timestamp}} Copyright [{{software_application.publisher.name}}](mailto:{{software_application.publisher.email}}) - {% if software_application.publisher.identifier %}> [{{software_application.publisher.identifier}}]({{software_application.publisher.identifier}}){% endif %}

## Project Team

### Authors

| Name | Email | Organization | Role | Identifier |
|------|-------|--------------|------|------------|
{% for role in software_application | normalize_author %}| {{role.author.family_name}}, {{role.author.given_name}} | [{{role.author.email}}](mailto:{{role.author.email}}) | [{{role.author.affiliation.name}}]({{role.author.affiliation.identifier}}) | [{{role.role_name}}]({{role.additional_type}}) | [{{role.author.identifier}}]({{role.author.identifier}}) |
{% endfor %}

### Contributors
{% if software_application.contributor %}
| Name | Email | Organization | Role | Identifier |
|------|-------|--------------|------|------------|
{% for role in software_application | normalize_contributor %}| {{role.contributor.family_name}}, {{role.contributor.given_name}} | [{{role.contributor.email}}](mailto:{{role.contributor.email}}) | [{{role.contributor.affiliation.name}}]({{role.contributor.affiliation.identifier}}) | [{{role.role_name}}]({{role.additional_type}}) | [{{role.contributor.identifier}}]({{role.contributor.identifier}}) |
{% endfor %}
{% else %}
The are no contributors for this project.
{% endif %}

{% if software_application.software_help %}## {{software_application.software_help.name}}

{{software_application.software_help.name}} can be found on [{{software_application.software_help.url}}]({{software_application.software_help.url}}).
{% endif %}

## Runtime environment

### Supported Operating Systems

{% for operating_system in software_application.operating_system %}- {{operating_system}}
{% endfor %}
### Requirements

{% for software_requirement in software_application.software_requirements %}- [{{software_requirement}}]({{software_requirement}})
{% endfor %}
