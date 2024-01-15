from marko import inline

class ParamBit(inline.InlineElement):

    pattern = r'\\$\\{[A-Za-z0-9_]+\\}'
    parse_children = True