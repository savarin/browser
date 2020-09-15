import collections


class Stylesheet():
    def __init__(self, rules):
        self.rules = rules

class Rule():
    def __init__(self, selectors, declarations):
        self.selectors = selectors
        self.declarations = declarations

Selector = collections.namedtuple("Selector", ["Simple"])

class SimpleSelector():
    def __init__(self, tag_name, selector_id, selector_class):
        self.tag_name = tag_name
        self.selector_id = selector_id
        self.selector_class = selector_class

class Declaration():
    def __init__(self, name, value):
        self.name = name
        self.value = value

Value = collections.namedtuple("Value", ["Keyword", "Length", "ColorValue"])
Unit = collections.namedtuple("Unit", ["Px"])
Color = collections.namedtuple("Color", ["r", "g", "b", "a"])


class CSSParser():
    def __init__(self, pos, text):
        #
        """
        """
        self.pos = pos
        self.text = text

    def eof(self):
        #
        """
        """
        return self.pos >= len(self.text)

    def next_char(self):
        #
        """
        """
        return self.text[self.pos]

    def consume_char(self):
        #
        """
        """
        cur_char = self.text[self.pos]
        self.pos += 1

        return cur_char

    def consume_while(self, test):
        #
        """
        """
        result = ""

        while not self.eof() and test(self.next_char()):
            result += self.consume_char()

        return result

    def consume_whitespace(self):
        #
        """
        """
        return self.consume_while(lambda x: x.isspace())

    def valid_identifier_char(self, char):
        #
        """
        """
        return char.isalnum() or char in ['-', '_']

    def parse_identifier(self):
        #
        """
        """
        return self.consume_while(self.valid_identifier_char)

    def parse_simple_selector(self):
        #
        """
        """
        selector = SimpleSelector(tag_name=None, selector_id=None, selector_class=[])

        while not self.eof():
            char = self.next_char()

            if self.valid_identifier_char(char):
                selector.tag_name = self.parse_identifier()
            elif self.next_char() == "#":
                self.consume_char()
                selector.selector_id = self.parse_identifier()
            elif self.next_char() == ".":
                self.consume_char()
                selector.selector_class.append(self.parse_identifier())
            elif self.next_char() == "*":
                self.consume_char()
            else:
                break

        return selector

    def parse_selectors(self):
        #
        """
        """
        selectors = []

        while True:
            selectors.append(Selector(Simple=self.parse_simple_selector()))
            self.consume_whitespace()
            char = self.next_char()

            if char == ",":
                self.consume_char()
                self.consume_whitespace()
            elif char == "{":
                break
            else:
                raise ValueError

        return selectors


if __name__ == "__main__":
    text = """\
h1, h2, h3 { margin: auto; color: #cc0000; }
div.note { margin-bottom: 20px; padding: 10px; }
#answer { display: none; }
"""
    
    result = CSSParser(0, text)
    selector = result.parse_selectors()

    for i in range(len(selector)):
        print(selector[i].Simple.tag_name)







