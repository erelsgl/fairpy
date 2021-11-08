"""
Run all the examples in the markdown files and insert the output into the files.
Uses `pweave`.
"""

import pweave

# pweave.weave('input_formats.source.md', output="input_formats.md")
pweave.publish("input_formats.source.py", doc_format="html", output="input_formats.html")  # markdown not supported
