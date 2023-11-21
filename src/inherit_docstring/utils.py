import re
from typing import Any

param_sections = [
    "Attributes",
    "Parameters",
    "Returns",
    "Yields",
    "Receives",
    "Raises",
    "Warns",
    "Warnings",
    "See Also",
]


def remove_indent(doc: str, indent: int = 4) -> str:
    return "\n".join(
        [
            x[indent:] if x.startswith(" " * indent) else x
            for x in doc.strip().split("\n")
        ]
    )


def add_indent(doc: str, indent: int = 4) -> str:
    docstring = "\n".join(
        [" " * indent + x if x else "" for x in doc.split("\n")]
    ).strip()
    if len(docstring.split("\n")) > 0:
        docstring += "\n" + " " * indent
    return docstring


def strip(doc: str, indent: int = 0) -> str:
    lines = [x.strip() for x in doc.strip().split("\n")]
    return "\n".join([" " * indent + x if x else "" for x in lines])


def parse_sections(doc: str) -> list[str]:
    sections = re.split(
        r"^([a-zA-Z0-9_]+\n-+|.. deprecated:: .*)\n", doc, flags=re.M
    )
    return sections


def parse_param_section(content: str) -> dict[str, tuple[str, str]]:
    params: dict[str, tuple[str, str]] = {}
    content_list = re.split(r"^(\S.*)\n", content, flags=re.M)
    name = None
    j = 0
    while j < len(content_list):
        if not content_list[j].strip():
            j += 1
            continue
        if name is None:
            if ":" in content_list[j]:
                colons = content_list[j].split(":")
                name = colons[0].strip()
                type_name = ":".join(colons[1:]).strip()
            else:
                name = content_list[j].strip()
                type_name = ""
            j += 1
        else:
            description = ""
            if content_list[j].startswith(" "):
                description = strip(content_list[j], indent=4)
                j += 1

            params[name] = (
                type_name.strip(),
                description,
            )
            name = None
    return params


def parse_docstring(doc: str, indent: int = 4) -> dict[str, Any]:
    doc = remove_indent(doc, indent=indent).strip()

    # Split by the major sections: Parameters, Returns, Notes, etc.
    sections = parse_sections(doc)

    docstrings: dict[str, Any] = {}
    # First section is always the header
    if header := strip(sections[0]):
        docstrings["Header"] = header

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            if not sections[i].startswith(".."):
                section_name = sections[i].split("\n")[0].strip()
            else:
                section_name = sections[i].strip()
            section_content = sections[i + 1].rstrip()
            docstrings[section_name] = {}

            if section_name in param_sections:
                docstrings[section_name] = parse_param_section(section_content)
            else:
                docstrings[section_name] = section_content.rstrip()

    return docstrings


def make_section_name(name: str) -> str:
    if not name.startswith(".."):
        name += "\n" + "-" * len(name)
    return name + "\n"


def make_param_doc(params: dict[str, tuple[str, str]]) -> str:
    doc = ""
    for param in params:
        doc += param
        if params[param][0] != "":
            doc += " : " + params[param][0]
        doc += "\n"
        if params[param][1]:
            doc += params[param][1] + "\n"
    return doc


def merge_docstring(base_doc: str, doc: str, indent: int = 4) -> str:
    docstring = parse_docstring(base_doc, indent=indent)
    parse_doc = parse_docstring(doc, indent=indent)
    for section_name in parse_doc:
        if section_name in param_sections:
            docstring[section_name] = docstring.get(section_name, {})
            for parm in parse_doc[section_name]:
                docstring[section_name][parm] = parse_doc[section_name][parm]
        else:
            docstring[section_name] = parse_doc[section_name]
    merged_doc = ""
    for section_name in docstring:
        if section_name != "Header":
            merged_doc += make_section_name(section_name)
        if section_name in param_sections:
            merged_doc += make_param_doc(docstring[section_name])
        else:
            merged_doc += docstring[section_name] + "\n"
        merged_doc += "\n"
    merged_doc = add_indent(merged_doc, indent=indent)
    return merged_doc
