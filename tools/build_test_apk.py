"""Build and verify the test APK on Windows or Linux."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = os.name == "nt"
APK_DIR = ROOT / "smarttubetv/build/outputs/apk/stbeta/debug"
OUTPUT = ROOT / "build/maintenance"


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def capture(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checks", action="store_true", help="Also run unit tests and lint")
    options = parser.parse_args()
    sdk_value = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    java_value = os.environ.get("JAVA_HOME")
    if not sdk_value or not java_value:
        parser.error("Set ANDROID_HOME and JAVA_HOME (JDK 17); see RUNBOOK.md")
    if (ROOT / "keystore.properties").exists():
        parser.error("Use a checkout without release signing configuration for test APKs")
    sdk = Path(sdk_value)
    suffix = ".exe" if WINDOWS else ""
    java = Path(java_value) / "bin" / ("java" + suffix)
    tools = sdk / "build-tools/30.0.3"
    aapt = tools / ("aapt" + suffix)
    apksigner = tools / "lib/apksigner.jar"
    for required in (java, aapt, apksigner, sdk / "platforms/android-34/android.jar",
                     sdk / "ndk/21.0.6113669/source.properties"):
        if not required.is_file():
            parser.error(f"Missing toolchain component: {required}")

    gradle = ("cmd.exe", "/d", "/c", "gradlew.bat") if WINDOWS else ("bash", "./gradlew")
    tasks = [":smarttubetv:assembleStbetaDebug"]
    if options.checks:
        tasks.extend((":common:testStbetaDebugUnitTest", ":smarttubetv:lintStbetaDebug"))
    run(*gradle, "--no-daemon", *tasks)
    apks = sorted(APK_DIR.glob("*_armeabi-v7a.apk"))
    if len(apks) != 1:
        raise SystemExit(f"Expected one ARMv7 APK in {APK_DIR}; clean the module build and retry")
    apk = apks[0]
    run(str(java), "-jar", str(apksigner), "verify", "--min-sdk-version", "30", str(apk))
    info = capture(str(aapt), "dump", "badging", str(apk))
    if not re.search(r"^package: name='org\.smarttube\.beta' ", info, re.M):
        raise SystemExit("Unexpected APK application ID")
    if not re.search(r"^native-code: 'armeabi-v7a'\s*$", info, re.M):
        raise SystemExit("Unexpected APK architecture")

    commit = capture("git", "rev-parse", "HEAD")
    dirty = bool(capture("git", "status", "--porcelain", "--ignore-submodules=none"))
    submodules = capture("git", "submodule", "status", "--recursive").splitlines()
    filename = "SmartTube-test-armv7.apk"
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(apk, OUTPUT / filename)
    (OUTPUT / "SHA256SUMS").write_text(f"{digest}  {filename}\n", encoding="ascii")
    metadata = {"commit": commit, "dirty": dirty, "submodules": submodules,
                "checks_requested": options.checks, "apk": filename, "sha256": digest}
    (OUTPUT / "build-info.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {OUTPUT / filename} (source {commit}, dirty={dirty})")


if __name__ == "__main__":
    main()
