from __future__ import annotations


def strip_swift_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    in_string = False
    in_multiline_string = False
    while index < len(text):
        if not in_string and not in_multiline_string and text.startswith("//", index):
            while index < len(text) and text[index] != "\n":
                result.append(" ")
                index += 1
            continue
        if not in_string and not in_multiline_string and text.startswith("/*", index):
            index = mask_swift_block_comment(text, index, result)
            continue
        if text.startswith('"""', index):
            in_multiline_string = not in_multiline_string
            result.extend('"""')
            index += 3
            continue
        if not in_multiline_string and text[index] == '"' and not is_escaped(text, index):
            in_string = not in_string

        result.append(text[index])
        index += 1
    return "".join(result)


def mask_swift_block_comment(text: str, index: int, result: list[str]) -> int:
    depth = 1
    result.extend("  ")
    index += 2
    while index < len(text) and depth > 0:
        if text.startswith("/*", index):
            depth += 1
            result.extend("  ")
            index += 2
            continue
        if text.startswith("*/", index):
            depth -= 1
            result.extend("  ")
            index += 2
            continue
        result.append("\n" if text[index] == "\n" else " ")
        index += 1
    return index


def is_escaped(text: str, index: int) -> bool:
    slash_count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slash_count += 1
        cursor -= 1
    return slash_count % 2 == 1
