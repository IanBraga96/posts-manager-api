import re


def extract_mentions(content):
    """
    Extract mentions (@user) from content
    """
    pattern = r"@(\w+)"
    mentions = re.findall(pattern, content)
    return list(set(mentions))
