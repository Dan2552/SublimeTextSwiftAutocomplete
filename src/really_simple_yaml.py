def generate_line(key, value, quote_string_values=None):
    if type(value) is list:
        return generate_line(key, _list_as_value(value, quote_string_values))
    if quote_string_values == True:
        value = _quote_string(value)

    return "\n" + str(key) + ": " + str(value)

def _list_as_value(values, quote_string_values=None):
    return "".join(map(lambda item: _decorate_list_item(item, quote_string_values) , values))

def _decorate_list_item(value, quote_string_values):
    if quote_string_values == True:
        value = _quote_string(value)
    return "\n- " + str(value)

def _quote_string(value):
    if type(value) is str:
        return "\"" + value + "\""
    return value
