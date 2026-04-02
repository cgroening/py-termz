"""
termz.util.string
=================

Provides utility functions for string manipulation and formatting.

This module contains helper methods for performing common string operations.

Included Features:
- `linewrap`: Splits long text into multiple lines, respecting a maximum line
   width and avoiding word breaks when possible.
- `charpos`: Returns all positions of a given character within a string.

These utilities are useful for simple text formatting tasks, especially when
preparing console output or working with fixed-width layouts.

"""


def linewrap(text: str, linewidth: int):
    """
    Splits a string into multiple lines with a specified maximum width.

    Parameters
    ----------
    text : str
        The input text to be split into lines.
    linewidth : int
        Maximum number of characters allowed per line.

    Returns
    -------
    str
        A string with lines separated by line breaks (\n).
    """
    lines = []
    while len(text) > 0:
        # Cut the maximum portion out of the given string
        maxcutpos = min(linewidth, len(text))

        # If the maximum portion doesn't end with a whitespace, cut off
        # at the last whitespace
        if len(text) > linewidth and text[maxcutpos-1] != ' ' \
           and text[maxcutpos] != ' ':
            # Position of the last whitespace
            cutpos = max(charpos(text[0:maxcutpos-1], ' '))
        else:
            cutpos = maxcutpos

        # Set snippet for this line and remove it from given text
        line = text[0:cutpos].strip()
        text = text[cutpos:len(text)]

        # Add line break if it's not the last line of the text
        if maxcutpos == linewidth and len(text[0:linewidth].strip()) > 0:
            line += '\n'

        lines.append(line)

    return ''.join(lines)


def charpos(text: str, char: str) -> list[int]:
    """
    Finds all positions of a specific character in a string.

    Parameters
    ----------
    text : str
        The input text to search in.
    char : str
        The character to search for.

    Returns
    -------
    list[int]
        A list of indices where the character occurs in the text.
    """
    return [pos for pos, c in enumerate(text) if c == char]
