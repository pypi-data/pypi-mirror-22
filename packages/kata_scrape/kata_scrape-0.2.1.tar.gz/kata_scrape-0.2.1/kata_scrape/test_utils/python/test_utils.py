class AssertException(Exception):
    pass

def format_message(message):
    return message.replace("\n", "<:LF:>")


def expect(passed=None, message=None, allow_raise=False):
    if passed:
        print("<PASSED::>Test Passed")
    else:
        message = message or "Value is not what was expected"
        print("<FAILED::>{0}".format(message))
        if allow_raise:
            raise AssertException(message)


def assert_equals(actual, expected, message=None, allow_raise=True):
    equals_msg = "{0} should equal {1}".format(repr(actual), repr(expected))
    if message is None:
        message = equals_msg
    else:
        message += ": " + equals_msg

    expect(actual == expected, message, allow_raise)


def assert_not_equals(actual, expected, message=None, allow_raise=True):
    equals_msg = \
        "{0} should not equal {1}".format(repr(actual), repr(expected))
    if message is None:
        message = equals_msg
    else:
        message += ": " + equals_msg

    expect(actual != expected, message, allow_raise)


def expect_error(message, function):
    passed = False
    try:
        function()
    except:
        passed = True
    expect(passed, message)


def describe(message):
    print("<DESCRIBE::>{0}".format(format_message(message)))


def it(message):
    print("<IT::>{0}".format(format_message(message)))
