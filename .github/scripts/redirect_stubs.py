"""Replace each page in a built site with a redirect to edgeric.ucsd.edu.

Used for the edgeric.github.io build, so that domain sends visitors and
crawlers to the canonical site. Usage: redirect_stubs.py <build dir>
"""
import html
import os
import sys

BASE = "https://edgeric.ucsd.edu/"
STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>EdgeRIC has moved</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({js} + location.search + location.hash);</script>
</head>
<body><p>EdgeRIC is now at <a href="{url}">{url}</a>.</p></body>
</html>
"""

root = sys.argv[1]
for folder, _, files in os.walk(root):
    for name in files:
        if not name.endswith(".html") or name.startswith("google"):
            continue
        path = os.path.join(folder, name)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        url = BASE + ("" if rel == "index.html" else rel)
        with open(path, "w") as f:
            f.write(STUB.format(url=html.escape(url), js='"%s"' % url))
