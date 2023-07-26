

import re


print(list(filter(None, re.split("([\?\(\)\/\-\+\{\}\>])", "/abc/"))))