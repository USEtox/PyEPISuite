"""The EPI Suite version this release of PyEPISuite targets.

PyEPISuite tracks the EPI Suite API it speaks to, so this module is the single
source of truth: the response models, the cache namespace and the local-runtime
jar check all derive their expectations from `EPISUITE_VERSION`.

When EPI Suite publishes a new version, bump `EPISUITE_VERSION` here and the
rest follows. The server reports its own version at `GET /api` as
`info.version`, and the local jar reports it as `Implementation-Version` in its
manifest.
"""

from typing import Tuple

# The EPI Suite API/CLI version these models were generated against.
EPISUITE_VERSION = "1.1.0"

# Oldest EPI Suite the client can talk to. Currently the same as
# EPISUITE_VERSION: 1.1.0 renamed and restructured most response sections, and
# older builds serve no HTTP API at all.
MINIMUM_EPISUITE_VERSION = "1.1.0"


def version_tuple(text: str) -> Tuple[int, ...]:
    """Parse a dotted numeric version into a comparable tuple."""
    return tuple(int(part) for part in text.split('.'))


EPISUITE_VERSION_INFO = version_tuple(EPISUITE_VERSION)
MINIMUM_EPISUITE_VERSION_INFO = version_tuple(MINIMUM_EPISUITE_VERSION)
