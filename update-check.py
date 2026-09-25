"""Update VERSION and deb/PACKAGE to the latest Proton Mail Bridge release.

Only writes the files; committing and opening a pull request is left to the
workflow so every version bump gets reviewed before it is built and published.
"""

import json
import os
import re
import sys
import urllib.request

API_URL = "https://api.github.com/repos/ProtonMail/proton-bridge/releases/latest"
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")


def fetch_latest_release():
    request = urllib.request.Request(API_URL, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    release = fetch_latest_release()

    version = release.get("tag_name", "")
    if not VERSION_RE.match(version):
        sys.exit(f"Unexpected release tag: {version!r}")

    debs = [
        asset["browser_download_url"]
        for asset in release.get("assets", [])
        if asset["name"].endswith("_amd64.deb")
    ]
    if len(debs) != 1:
        sys.exit(f"Expected exactly one amd64 .deb in release {version}, found {len(debs)}")

    print(f"Latest release is: {version}")

    with open("VERSION", "w") as f:
        f.write(version)

    with open("deb/PACKAGE", "w") as f:
        f.write(debs[0])

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a") as f:
            f.write(f"version={version}\n")


if __name__ == "__main__":
    main()
