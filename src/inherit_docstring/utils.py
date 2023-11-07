import re
from typing import Any

params_sections = [
    "Attributes",
    "Parameters",
    "Returns",
    "Yiels",
    "Receives",
    "Raises",
    "Warns",
    "Warnings",
]

indent = '    '


def strip(doc: str, spaces: int = 0) -> str:
    lines = [x.strip() for x in doc.strip().split("\n")]
    return "\n".join([" " * spaces + x if x else "" for x in lines])


def parse_docstring(doc: str) -> dict[str, Any]:
    # Split by the major sections: Parameters, Returns, Notes, etc.
    sections = re.split(rf"{indent}([a-zA-Z0-9_]+)\n{indent}-+", doc)

    docstrings: dict[str, Any] = {}
    # First section is always the header
    if header := strip(sections[0]):
        docstrings["Header"] = header

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            section_name = sections[i].strip()
            section_content = sections[i + 1]
            docstrings[section_name] = {}

            if section_name in params_sections:
                params = re.split(rf"[\n^]{indent}(\S.*)\n",
                    section_content,
                )
                while params[0] == "":
                    params = params[1:]
                for j in range(0, len(params), 2):
                    if ':' in params[j]:
                        name, type_name = params[j].split(':')
                    else:
                        name = params[j]
                        type_name = ''

                    docstrings[section_name][name.strip()] = (
                        type_name.strip(),
                        strip(params[j + 1], len(indent)),
                    )
            else:
                docstrings[section_name] = strip(section_content)

    return docstrings


def merge_docstring(base_doc: str, doc: str) -> str:
    docstring = parse_docstring(base_doc)
    parse_doc = parse_docstring(doc)
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
            merged_doc += "-" * len(section_name) + "\n"
        if section_name in params_sections:
            for param in docstring[section_name]:
                merged_doc += param + ":"
                if docstring[section_name][param][0] != "":
                    merged_doc += " " + docstring[section_name][param][0]
                merged_doc += "\n"
                merged_doc += docstring[section_name][param][1] + "\n"
        else:
            merged_doc += docstring[section_name] + "\n"
        merged_doc += "\n"
    merged_doc = merged_doc.strip()
    return merged_doc


def docstring_add_space(doc: str, spaces: int = 4) -> str:
    docstring = "\n".join(
        [" " * spaces + x if x else "" for x in doc.split("\n")]
    ).strip()
    if len(docstring.split("\n")) > 0:
        docstring += "\n" + " " * spaces
    return docstring
