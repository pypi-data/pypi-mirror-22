*************
Parsing Tools
*************

This repository contains multiple small projects each of which can be used
separately.

This would be a great package to use when creating your own custom Django
REST Framework renderers and parsers based on a custom MIME types.

Current Projects
================

mimeparser
----------

This tool would be used to parse HTTP headers to derive the 'best fit' mime
type. It handles suffix and quality parsing and can be used to find the best
match from an `Accept` header from a list of available mime types.

xml2dict
--------

This tool should be able to parse any XML document into Python objects. The
output will become very verbose since it will include all attributes,
elements and namespaces found in the XML document.
