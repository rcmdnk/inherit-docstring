import re
import sys
from typing import Any

param_sections = [
    'Attributes',
    'Parameters',
    'Returns',
    'Yields',
    'Receives',
    'Raises',
    'Warns',
    'Warnings',
    'See Also',
]


def remove_indent(doc: str, indent: int = 4) -> str:
    return '\n'.join(
        [
            x[indent:] if x.startswith(' ' * indent) else x
            for x in doc.strip().split('\n')
        ]
    )


def add_indent(doc: str, indent: int = 4) -> str:
    return '\n'.join([' ' * indent + x if x else '' for x in doc.split('\n')])


def multiline_strip(doc: str, indent: int = 0) -> str:
    lines = [x.strip() for x in doc.strip().split('\n')]
    return '\n'.join([' ' * indent + x if x else '' for x in lines])


def parse_sections(doc: str) -> list[str]:
    return re.split(
        r'^([a-zA-Z0-9_]+\n-+|.. deprecated:: .*)\n', doc, flags=re.MULTILINE
    )


def parse_param_section(content: str) -> dict[str, tuple[str, str]]:
    params: dict[str, tuple[str, str]] = {}
    content_list = re.split(r'^(\S.*)\n', content, flags=re.MULTILINE)
    name = None
    j = 0
    while j < len(content_list):
        if not content_list[j].strip():
            j += 1
            continue
        if name is None:
            if ':' in content_list[j]:
                colons = content_list[j].split(':')
                name = colons[0].strip()
                type_name = ':'.join(colons[1:]).strip()
            else:
                name = content_list[j].strip()
                type_name = ''
            j += 1
        else:
            description = ''
            if content_list[j].startswith(' '):
                description = multiline_strip(content_list[j], indent=4)
                j += 1

            params[name] = (
                type_name.strip(),
                description,
            )
            name = None
    return params


def parse_docstring(doc: str, indent: int = 4) -> dict[str, Any]:
    if len(lines := doc.split('\n')) > 1:
        last_blank_line = lines[-2].strip() == ''
    else:
        last_blank_line = False

    if sys.version_info < (3, 13):
        doc = remove_indent(doc, indent=indent).strip()

    # Split by the major sections: Parameters, Returns, Notes, etc.
    sections = parse_sections(doc)

    parsed: dict[str, Any] = {}
    # First section is always the header
    if header := multiline_strip(sections[0]):
        parsed['Header'] = header

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            if not sections[i].startswith('..'):
                section_name = sections[i].split('\n')[0].strip()
            else:
                section_name = sections[i].strip()
            section_content = sections[i + 1].rstrip()
            parsed[section_name] = {}

            if section_name in param_sections:
                parsed[section_name] = parse_param_section(section_content)
            else:
                parsed[section_name] = section_content.rstrip()

    parsed['last_blank_line'] = last_blank_line

    return parsed


def make_section_name(name: str) -> str:
    if not name.startswith('..'):
        name += '\n' + '-' * len(name)
    return name + '\n'


def make_param_doc(params: dict[str, tuple[str, str]]) -> str:
    doc = ''
    for param in params:
        doc += param
        if params[param][0] != '':
            doc += ' : ' + params[param][0]
        doc += '\n'
        if params[param][1]:
            doc += params[param][1] + '\n'
    return doc


def is_header_only(parsed: dict[str, Any]) -> bool:
    return list(parsed.keys()) == ['Header'] and '\n' not in parsed['Header']


def make_docstring(parsed: dict[str, Any]) -> str:
    doc = ''
    for section, content in parsed.items():
        if section != 'Header':
            doc += make_section_name(section)
        if section in param_sections:
            doc += make_param_doc(content)
        else:
            doc += content + '\n'
        doc += '\n'
    return doc


def complete_docstring(
    doc: str, indent: int = 4, last_blank_line: bool = False
) -> str:
    if sys.version_info < (3, 13):
        doc = add_indent(doc, indent=indent)

    doc = doc.strip()
    if last_blank_line:
        doc += '\n\n' + ' ' * indent
    elif len(doc.split('\n')) > 1:
        doc += '\n' + ' ' * indent
    return doc


def merge_docstring(base_doc: str, doc: str, indent: int = 4) -> str:
    base_parsed = parse_docstring(base_doc, indent=indent)
    parsed = parse_docstring(doc, indent=indent)
    last_blank_line = (
        base_parsed['last_blank_line'] or parsed['last_blank_line']
    )
    del base_parsed['last_blank_line']
    del parsed['last_blank_line']
    for section_name in parsed:
        if section_name in param_sections:
            base_parsed[section_name] = base_parsed.get(section_name, {})
            for parm in parsed[section_name]:
                base_parsed[section_name][parm] = parsed[section_name][parm]
        else:
            base_parsed[section_name] = parsed[section_name]
    if is_header_only(base_parsed):
        merged_doc = base_parsed['Header']
    else:
        merged_doc = make_docstring(base_parsed)

    return complete_docstring(
        merged_doc, indent=indent, last_blank_line=last_blank_line
    )
