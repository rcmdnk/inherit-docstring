import re
from typing import Any

params_sections = [
    "Attributes",
    "Parameters",
    "Returns",
    "Yields",
    "Receives",
    "Raises",
    "Warns",
    "Warnings",
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


def parse_docstring(doc: str, indent: int = 4) -> dict[str, Any]:
    doc = remove_indent(doc, indent=indent).strip()

    # Split by the major sections: Parameters, Returns, Notes, etc.
    sections = re.split(r"^([a-zA-Z0-9_]+\n-+|.. deprecated:: .*)\n", doc, flags=re.M)

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

            if section_name in params_sections:
                params = re.split(r"^(\S.*)\n", section_content, flags=re.M)
                name = None
                j = 0
                while j < len(params):
                    if not params[j].strip():
                        j += 1
                        continue
                    if name is None:
                        if ":" in params[j]:
                            colons = params[j].split(":")
                            name = colons[0].strip()
                            type_name = ":".join(colons[1:]).strip()
                        else:
                            name = params[j].strip()
                            type_name = ""
                        j += 1
                    else:
                        description = ""
                        if params[j].startswith(" "):
                            description = strip(params[j], indent=4)
                            j += 1

                        docstrings[section_name][name] = (
                            type_name.strip(),
                            description,
                        )
                        name = None
            else:
                docstrings[section_name] = strip(section_content, indent=4)

    return docstrings


def merge_docstring(base_doc: str, doc: str, indent: int = 4) -> str:
    docstring = parse_docstring(base_doc, indent=indent)
    parse_doc = parse_docstring(doc, indent=indent)
    for section_name in parse_doc:
        if section_name in params_sections:
            docstring[section_name] = docstring.get(section_name, {})
            for parm in parse_doc[section_name]:
                docstring[section_name][parm] = parse_doc[section_name][parm]
        else:
            docstring[section_name] = parse_doc[section_name]
    merged_doc = ""
    for section_name in docstring:
        if section_name != "Header":
            merged_doc += section_name + "\n"
            if not section_name.startswith(".."):
                merged_doc += "-" * len(section_name) + "\n"
        if section_name in params_sections:
            for param in docstring[section_name]:
                merged_doc += param
                if docstring[section_name][param][0] != "":
                    merged_doc += " : " + docstring[section_name][param][0]
                merged_doc += "\n"
                if docstring[section_name][param][1]:
                    merged_doc += docstring[section_name][param][1] + "\n"
        else:
            merged_doc += docstring[section_name] + "\n"
        merged_doc += "\n"
    merged_doc = add_indent(merged_doc, indent=indent)
    return merged_doc
