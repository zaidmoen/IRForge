import re


def tokenize(text):
    """Turn text into lowercase word tokens"""
    return re.findall(r"[a-z0-9]+", text.lower())
