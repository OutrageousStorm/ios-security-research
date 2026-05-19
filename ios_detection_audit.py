#!/usr/bin/env python3
"""ios_detection_audit.py -- Audit iOS security signals via libimobiledevice
Shows what detection libraries can see: jailbreak, development mode, debugger
"""
import subprocess, json, argparse

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except:
        return ""

CHECKS = [
    ("Jailbreak: /var/mobile/Library/Cydia", "ideviceshell -c 'test -d /var/mobile/Library/Cydia'", 0),
    ("Jailbreak: /Applications/Cydia.app", "ideviceshell -c 'test -d /Applications/Cydia.app'", 0),
    ("Development mode", "ideviceshell -c 'launchctl list | grep -i debug'", 0),
    ("App Store restriction", "ideviceshell -c 'defaults read com.apple.preferences.security | grep -i appstore'", 0),
]

def audit():
    print("🔍 iOS Security Signal Audit\n")
    detected = 0
    for label, cmd, _ in CHECKS:
        result = run_cmd(cmd)
        is_detected = bool(result.strip())
        icon = "🔴" if is_detected else "✅"
        print(f"{icon} {label}")
        detected += is_detected
    print(f"\nDetected signals: {detected}/{len(CHECKS)}")

if __name__ == "__main__":
    audit()
