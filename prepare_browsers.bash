#!/bin/bash

cat ./selenoid/browsers.json | python3 -c 'import json; import sys; [[print(v["image"]) for v in b.get("versions", {}).values() if v.get("image")] for b in json.load(sys.stdin).values()]'

cat ./selenoid/browsers.json | python3 -c 'import json; import sys; [[print(v["image"]) for v in b.get("versions", {}).values() if v.get("image")] for b in json.load(sys.stdin).values()]' | xargs -I{} docker pull {}
