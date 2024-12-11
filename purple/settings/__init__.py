# Copyright The IETF Trust 2024, All Rights Reserved
"""Django settings"""

import os

deployment_mode = os.environ.get("PURPLE_DEPLOYMENT_MODE", "production")
if deployment_mode == "development":
    from .development import *
elif deployment_mode == "build":
    from .build import *
else:
    from .production import *
