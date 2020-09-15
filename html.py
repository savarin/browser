import dom


class HTMLParser():
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

    def starts_with(self, s):
        #
        """
        """
        return self.text[self.pos:].startswith(s)

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

    def parse_tag_name(self):
        #
        """
        """
        return self.consume_while(lambda x: x.isalnum())

    def parse_node(self):
        #
        """
        """
        if self.next_char() == "<":
            return self.parse_element()

        return self.parse_text()

    def parse_text(self):
        #
        """
        """
        dom.text(self.consume_while(lambda x: x != "<"))

    def parse_element(self):
        #
        """
        """
        assert self.consume_char() == "<"
        tag_name = self.parse_tag_name()
        attrs = self.parse_attributes()
        assert self.consume_char() == ">"

        children = self.parse_nodes()

        assert self.consume_char() == "<"
        assert self.consume_char() == "/"
        assert self.parse_tag_name() == tag_name
        assert self.consume_char() == ">"

        return dom.elem(tag_name, attrs, children)

    def parse_attr(self):
        #
        """
        """
        name = self.parse_tag_name()

        assert self.consume_char() == "="
        value = self.parse_attr_value()

        return name, value

    def parse_attr_value(self):
        #
        """
        """
        open_quote = self.consume_char()
        assert open_quote in ['"', "'"]
        value = self.consume_while(lambda c: c!= open_quote)
        assert self.consume_char() == open_quote

        return value

    def parse_attributes(self):
        #
        """
        """
        attributes = {}

        while True:
            self.consume_whitespace()

            if self.next_char() == ">":
                break

            name, value = self.parse_attr()
            attributes[name] = value

        return attributes

    def parse_nodes(self):
        #
        """
        """
        nodes = []

        while True:
            self.consume_whitespace()

            if self.eof() or self.starts_with("</"):
                break

            nodes.append(self.parse_node())

        return nodes

def parse(source):
    #
    """Parse an HTML document and return the root element."""
    nodes = Parser(pos=0, text=source).parse_nodes()

    if len(nodes) == 1:
        return nodes[0]
    
    return dom.elem("html", {}, nodes)


if __name__ == "__main__":
    text = """\
<html>
    <body>
        <h1>Title</h1>
        <div id="main" class="test">
            <p>Hello <em>world</em>!</p>
        </div>
    </body>
</html>
"""

    result = parse(text)
    print(result)
    print(result.children)
    print(result.node_type)
    print(result.children[0])
    print(result.children[0].children)
    print(result.children[0].node_type)
    print(result.children[0].children[0].node_type)
    print(result.children[0].children[1].node_type)
    
