# Copyright 2026 Transpiler-Mate
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""transpiler-mate plugin for CWL 2 Markdown."""

from __future__ import annotations

import time
import types
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Union, get_args, get_origin

from cwl_utils.parser import Process, Workflow, cwl_v1_0, cwl_v1_1, cwl_v1_2
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from transpiler_mate.api import (
    AuthorRole,
    ContributorRole,
    PluginExecutionError,
    SoftwareApplication,
    transpiler_plugin,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from transpiler_mate.api import TranspilerContext

# START custom built-in functions to simplify the CWL rendering

# CWLtype to string methods

NA_ROLE = "N/A"

InputRecordSchema = (
    cwl_v1_0.InputRecordSchema | cwl_v1_1.InputRecordSchema | cwl_v1_2.InputRecordSchema
)

SchemaDefRequirement = (
    cwl_v1_0.SchemaDefRequirement
    | cwl_v1_1.SchemaDefRequirement
    | cwl_v1_2.SchemaDefRequirement
)


def normalize_author(
    software_application: SoftwareApplication,
) -> list[AuthorRole]:
    """Return application authors as role models for template rendering."""
    authors = software_application.author
    author_list = authors if isinstance(authors, list) else [authors]
    return [
        author
        if isinstance(author, AuthorRole)
        else AuthorRole(role_name=NA_ROLE, author=author)
        for author in author_list
    ]


def normalize_contributor(
    software_application: SoftwareApplication,
) -> list[ContributorRole]:
    """Return application contributors as role models for template rendering."""
    contributors = software_application.contributor
    if contributors is None:
        return []

    contributor_list = (
        contributors if isinstance(contributors, list) else [contributors]
    )
    return [
        contributor
        if isinstance(contributor, ContributorRole)
        else ContributorRole(role_name=NA_ROLE, contributor=contributor)
        for contributor in contributor_list
    ]


def type_to_string(typ: Any, parent: Process) -> str:  # noqa: C901
    """
    Serializes a CWL type to a human-readable string.

    Args:
        `typ` (`Any`): Any CWL type

    Returns:
        `str`: The human-readable string representing the input CWL type.
    """
    if get_origin(typ) in (Union, types.UnionType):
        return f"One of:<ul>{''.join(f'<li>{type_to_string(inner_type, parent)}</li>' for inner_type in get_args(typ))}</ul>"

    if isinstance(typ, list):
        return f"One of:<ul>{''.join(f'<li>{type_to_string(t, parent)}</li>' for t in typ)}</ul>"

    if hasattr(typ, "items"):
        return f"`array` of {type_to_string(typ.items, parent)}"

    if isinstance(typ, InputRecordSchema):
        fields = (
            "".join(
                f"<li>`{field.name.split('/')[-1]}`: {type_to_string(field.type_, parent)}</li>"
                for field in typ.fields
            )
            if typ.fields
            else ""
        )

        return f"[{typ.name.split('#')[-1]}]({typ.name}):<ul>{fields}</ul>"

    if isinstance(typ, str):
        type_str = typ
    elif hasattr(typ, "__name__"):
        type_str = typ.__name__
    elif hasattr(typ, "type_"):
        type_str = typ.type_
    else:
        # last hope to follow back
        type_str = str(typ)

    if "#" in type_str:  # we can assume it is an URL
        if parent and parent.requirements:
            for requirement in parent.requirements:
                if isinstance(requirement, SchemaDefRequirement):
                    for inner_type in requirement.types:
                        if type_str == inner_type.name:
                            return type_to_string(inner_type, parent)

        # follow up on plain link if not found
        return f"[{type_str.split('#')[-1]}]({type_str})"

    for special_type in ["Any", "Directory", "File"]:
        if special_type == type_str:
            return (
                f"[{type_str}](https://www.commonwl.org/v1.2/Workflow.html#{type_str})"
            )

    if type_str == "enum":
        symbols = "".join(
            f"<li>`{symbol.split('/')[-1]}`</li>"
            for symbol in typ.symbols  # type: ignore
        )
        return f"[{type_str}](https://www.commonwl.org/v1.2/Workflow.html#{type(typ).__name__}):<ul>{symbols}</ul>"

    return f"[{type_str}](https://www.commonwl.org/v1.2/Workflow.html#CWLType)"


def _get_version() -> str:
    try:
        return version("cwl2markdown")
    except PackageNotFoundError:
        return "N/A"


def _to_mapping(functions: list[Any]) -> dict[str, Any]:
    mapping: dict[str, Any] = {}

    for function in functions:
        mapping[function.__name__] = function

    return mapping


def nullable(type_: Any) -> bool:
    return (
        isinstance(type_, list)
        and "null" in type_
        or hasattr(type_, "items")
        and nullable(type_.items)  # type: ignore
    )


def get_exection_command(clt: Any) -> str:
    result: list[str] = []

    def _append_arg(arg: Any):
        if isinstance(arg, list):
            for arg_i in arg:
                _append_arg(arg_i)
        elif isinstance(arg, str):
            result.append(arg)
        else:
            result.append("<ARGUMENT_DYNAMICALLY_SET>")

    def _check_then_append(arg_name: str):
        if hasattr(clt, arg_name) and getattr(clt, arg_name):
            _append_arg(getattr(clt, arg_name))

    _check_then_append("baseCommand")
    _check_then_append("arguments")

    return " ".join(result)


# END


class CWL2MarkdownOptions(BaseModel):
    """Options accepted by the CWL 2 Markdown plugin."""

    model_config = ConfigDict(extra="forbid")

    output: Annotated[
        Path, Field(default=Path("./"), description="The output directory path")
    ]

    code_repository: Annotated[
        str | None,
        Field(
            default=None,
            description="The (SVN, GitHub, CodePlex, ...) code repository URL",
        ),
    ]


@transpiler_plugin(
    name="cwl2markdown",
    description="CWL to Markdown Transpiler-Mate Plugin.",
    options_model=CWL2MarkdownOptions,
)
def cwl2markdown(context: TranspilerContext, options: CWL2MarkdownOptions) -> None:
    """CWL to Markdown Transpiler-Mate Plugin."""
    _jinja_environment = Environment(
        loader=PackageLoader(package_name="cwl2markdown"),
        autoescape=select_autoescape(),
    )
    _jinja_environment.globals["type_to_string"] = type_to_string
    _jinja_environment.filters.update(
        _to_mapping(
            [
                get_exection_command,
                normalize_author,
                normalize_contributor,
            ]
        )
    )
    _jinja_environment.tests.update(_to_mapping([nullable]))

    template = _jinja_environment.get_template("index.md")

    try:
        options.output.mkdir(parents=True, exist_ok=True)

        wf_ids: Iterable[str] = (
            [context.process_id] if context.process_id else context.document.keys()
        )

        workflows: list[str] = []

        for wf_id in wf_ids:
            process: Process | None = context.document.get(wf_id)

            logger.debug(f"* Checking '{wf_id}'...")

            if not process:
                logger.warning(
                    f"  '{wf_id}' does not exist in {context.source} CWL document, discarding."
                )
                continue

            if not isinstance(process, Workflow):
                logger.warning(
                    f"  '{process.id}' is not a Workflow instance, discarding"
                )
                continue

            logger.debug(f"  Processing '{process.id}'")
            workflows.append(process.id)

        if not workflows:
            raise PluginExecutionError(
                f"No Workflow(s) found in input {context.source} CWL document"
            )

        for workflow in workflows:
            target: Path = Path(options.output, f"{workflow}.md")
            logger.info(f"Rendering Markdown documentation to {target.absolute()}...")

            with target.open("w") as output_stream:
                output_stream.write(
                    template.render(
                        version=_get_version(),
                        timestamp=datetime.fromtimestamp(time.time()).isoformat(
                            timespec="milliseconds"
                        ),
                        software_application=context.metadata,
                        workflow=workflow,
                        index=context.document,
                    )
                )
            logger.success(
                f"Markdown documentation successfully serialized to {target.absolute()}"
            )
    except Exception as e:
        raise PluginExecutionError(
            f"An error occurred when serializing to {options.output.absolute()}, see nested exception"
        ) from e
