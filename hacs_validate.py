import json
import os
import sys


def check_manifest():
    manifest_path = "custom_components/ww_kundenportal/manifest.json"
    if not os.path.exists(manifest_path):
        print(f"ERROR: {manifest_path} not found.")
        return False

    try:
        with open(manifest_path, "r") as f:
            data = json.load(f)

        required = [
            "domain",
            "name",
            "documentation",
            "dependencies",
            "codeowners",
            "requirements",
            "version",
            "iot_class",
        ]
        missing = [k for k in required if k not in data]

        if missing:
            print(f"ERROR: Missing keys in manifest.json: {missing}")
            return False

        print("Manifest JSON is valid.")
        print(f"Version: {data['version']}")
        print(f"Domain: {data['domain']}")

        if data["domain"] != "ww_kundenportal":
            print(
                f"ERROR: Domain mismatch. Expected 'ww_kundenportal', got '{data['domain']}'"
            )
            return False

        return True
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in manifest.json: {e}")
        return False


def check_hacs_json():
    hacs_path = "hacs.json"
    if os.path.exists(hacs_path):
        print("hacs.json found.")
        try:
            with open(hacs_path, "r") as f:
                json.load(f)
            print("hacs.json is valid.")
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON in hacs.json")
    else:
        print("WARNING: hacs.json not found (optional but recommended)")


def check_structure():
    required_files = [
        "custom_components/ww_kundenportal/__init__.py",
        "custom_components/ww_kundenportal/manifest.json",
        "custom_components/ww_kundenportal/const.py",
        "custom_components/ww_kundenportal/sensor.py",
        "custom_components/ww_kundenportal/config_flow.py",
    ]
    for p in required_files:
        if not os.path.exists(p):
            print(f"ERROR: Missing file {p}")
            return False
    print("Directory structure looks correct.")
    return True


if __name__ == "__main__":
    print("--- HACS Validation ---")
    v1 = check_manifest()
    v2 = check_structure()
    check_hacs_json()

    if v1 and v2:
        print("\nSUCCESS: Component structure appears valid for HACS.")
        print(
            "Ensure you have created a GitHub Release tagged exactly matching the manifest version."
        )
    else:
        print("\nFAILURE: Issues found.")
        sys.exit(1)
