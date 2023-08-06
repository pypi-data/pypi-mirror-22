""" some tools """

import logging
import re
import sys

from rancon import settings

tag_matcher = re.compile("%([A-Z0-9]+)%")


def fail(message):
    """ logs message before calling sys.exit
        XXX: why is this using print not log?
    """
    if isinstance(message, list) or isinstance(message, tuple):
        if len(message) > 1:
            message = "\n  - " + "\n  - ".join(message)
        else:
            message = " " + message[0]
    else:
        message = " " + message
    print("FATAL:%s" % message)
    sys.exit(-1)


def is_true(something):
    """ checks if something is truthy.
        for strings this is supposed to be one (lowercased) of "true", "1", "yes", "on"
    """
    if isinstance(something, str):
        return something.lower() in ("true", "1", "yes", "on")
    else:
        return bool(something)


def tag_replace(line, replacement_dict, default="UNDEFINED"):
    """
    Replaces a tag content with replacement information from the given
    replacement hash. The replacement must exist.
    :param line: The tag value
    :param replacement_dict: The hash to use for the replacements
    :return: The processed string
    """
    tags = tag_matcher.findall(line)
    for tag in tags:
        replacement = str(replacement_dict.get(tag.lower(), default))
        line = line.replace("%{}%".format(tag), replacement)
    return line


def getLogger(*args, **kwargs):
    """ returns a logger
        XXX: why not define this in settings?
    """
    logger = logging.getLogger(*args, **kwargs)
    logger.setLevel(settings.loglevel)
    return logger
