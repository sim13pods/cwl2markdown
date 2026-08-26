from transpiler_mate.api import (
    AuthorRole,
    ContributorRole,
    Organization,
    Person,
    SoftwareApplication,
)

from cwl2markdown.plugin import normalize_author, normalize_contributor


def _person(given_name: str) -> Person:
    return Person(
        given_name=given_name,
        family_name="Example",
        email=f"{given_name.lower()}@example.com",
        affiliation=Organization(name="Example Organization"),
    )


def test_normalize_author_uses_software_application_models() -> None:
    person = _person("Alice")
    role = AuthorRole(role_name="Developer", author=_person("Bob"))
    metadata = SoftwareApplication.model_construct(author=[person, role])

    normalized = normalize_author(metadata)

    assert normalized == [AuthorRole(role_name="N/A", author=person), role]
    assert all(isinstance(author, AuthorRole) for author in normalized)


def test_normalize_contributor_uses_software_application_models() -> None:
    person = _person("Carol")
    role = ContributorRole(role_name="Reviewer", contributor=_person("Dan"))
    metadata = SoftwareApplication.model_construct(contributor=[person, role])

    normalized = normalize_contributor(metadata)

    assert normalized == [ContributorRole(role_name="N/A", contributor=person), role]
    assert all(isinstance(contributor, ContributorRole) for contributor in normalized)


def test_normalize_contributor_handles_missing_contributors() -> None:
    metadata = SoftwareApplication.model_construct(contributor=None)

    assert normalize_contributor(metadata) == []
