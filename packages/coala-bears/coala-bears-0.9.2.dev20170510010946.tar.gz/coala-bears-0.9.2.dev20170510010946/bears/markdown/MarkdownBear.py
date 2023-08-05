import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='remark',
        use_stdin=True,
        output_format='corrected',
        result_message='The text does not comply to the set style.')
class MarkdownBear:
    """
    Check and correct Markdown style violations automatically.

    See <https://github.com/wooorm/remark-lint> for details about the tool
    below.
    """

    LANGUAGES = {'Markdown'}
    REQUIREMENTS = {NpmRequirement('remark-cli', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         markdown_bullets: str='-',
                         markdown_closed_headings: bool=False,
                         markdown_setext_headings: bool=False,
                         markdown_emphasis: str='*',
                         markdown_strong: str='*',
                         markdown_encode_entities: bool=False,
                         markdown_codefence: str='`',
                         markdown_fences: bool=True,
                         markdown_list_indent: str='1',
                         markdown_loose_tables: bool=False,
                         markdown_spaced_tables: bool=True,
                         markdown_list_increment: bool=True,
                         markdown_horizontal_rule: str='*',
                         markdown_horizontal_rule_spaces: bool=False,
                         markdown_horizontal_rule_repeat: int=3):
        """
        :param markdown_bullets:
            Character to use for bullets in lists. Can be "-", "*" or "+".
        :param markdown_closed_headings:
            Whether to close Atx headings or not. if true, extra # marks will
            be required after the heading. eg: `## Heading ##`.
        :param markdown_setext_headings:
            Whether to use setext headings. A setext heading uses underlines
            instead of # marks.
        :param markdown_emphasis:
            Character to wrap strong emphasis by. Can be "_" or "*".
        :param markdown_strong:
            Character to wrap slight emphasis by. Can be "_" or "*".
        :param markdown_encode_entities:
            Whether to encode symbols that are not ASCII into special HTML
            characters.
        :param markdown_codefence:
            Used to find which characters to use for code fences. Can be "`" or
            "~".
        :param markdown_fences:
            Use fences for code blocks.
        :param markdown_list_indent:
            Used to find spacing after bullet in lists. Can be "1", "tab" or
            "mixed".

            - "1" - 1 space after bullet.
            - "tab" - Use tab stops to begin a sentence after the bullet.
            - "mixed" - Use "1" when the list item is only 1 line, "tab" if it
              spans multiple.
        :param markdown_loose_tables:
            Whether to use pipes for the outermost borders in a table.
        :param markdown_spaced_tables:
            Whether to add space between pipes in a table.
        :param markdown_list_increment:
            Whether an ordered lists numbers should be incremented.
        :param markdown_horizontal_rule:
            The horizontal rule character. Can be '*', '_' or '-'.
        :param markdown_horizontal_rule_spaces:
            Whether spaces should be added between horizontal rule characters.
        :param markdown_horizontal_rule_repeat:
            The number of times the horizontal rule character will be repeated.
        """
        remark_configs = {
            'bullet': markdown_bullets,                         # - or *
            'closeAtx': markdown_closed_headings,               # Bool
            'setext': markdown_setext_headings,                 # Bool
            'emphasis': markdown_emphasis,                      # char (_ or *)
            'strong': markdown_strong,                          # char (_ or *)
            'entities': markdown_encode_entities,               # Bool
            'fence': markdown_codefence,                        # char (~ or `)
            'fences': markdown_fences,                          # Bool
            'listItemIndent': markdown_list_indent,             # int or "tab"
                                                                # or "mixed"
            'looseTable': markdown_loose_tables,                # Bool
            'spacedTable': markdown_spaced_tables,              # Bool
            'incrementListMarker': markdown_list_increment,     # Bool
            'rule': markdown_horizontal_rule,                   # - or * or _
            'ruleSpaces': markdown_horizontal_rule_spaces,      # Bool
            'ruleRepetition': markdown_horizontal_rule_repeat,  # int
        }

        config_json = json.dumps(remark_configs)
        # Remove { and } as remark adds them on its own
        settings = config_json[1:-1]
        return '--no-color', '--quiet', '--setting', settings
