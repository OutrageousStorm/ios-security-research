# iOS Entitlements & Sandbox

How iOS app sandboxing works and what entitlements control.

---

## The iOS sandbox

Every iOS app runs in a strict sandbox:
- Each app has its own isolated container (`/var/mobile/Containers/Data/Application/<UUID>/`)
- Apps cannot access other apps' files (without permission)
- System resources require explicit entitlements
- Enforced by the kernel and `sandbox` kext (MACF)

---

## What are entitlements?

Entitlements are key-value pairs embedded in the app's code signature that grant specific privileges. Apple's servers verify these when signing apps.

```bash
# Extract entitlements from an IPA
ldid -e Payload/App.app/App

# Or with codesign on macOS
codesign -d --entitlements - App.app/App
```

---

## Common entitlements

| Entitlement | What it grants |
|-------------|----------------|
| `com.apple.security.application-groups` | Shared data between app + extensions |
| `com.apple.developer.associated-domains` | Universal Links, Sign in with Apple |
| `com.apple.developer.healthkit` | HealthKit access |
| `keychain-access-groups` | Keychain sharing between apps |
| `com.apple.developer.siri` | SiriKit integration |
| `com.apple.developer.push-notification` | Push notifications (APNs) |
| `com.apple.developer.nfc.readersession.formats` | NFC reading |
| `com.apple.developer.networking.networkextension` | VPN, DNS proxying |

---

## Privileged entitlements (platform apps only)

These entitlements exist in Apple's own apps and cannot be used by third-party apps:

```
com.apple.private.security.no-sandbox   ← completely disables sandbox
com.apple.private.security.disk-device-access
com.apple.private.MobileContainerManager.allowed
com.apple.private.springboard
com.apple.springboard.opensensitiveurl
```

**Jailbreaks use these:** Bootstrapping a jailbreak involves using patched entitlements to grant privileged access to the jailbreak daemon.

---

## Sandbox escape techniques (historical)

| CVE | Year | Method |
|-----|------|--------|
| CVE-2019-8605 | 2019 | Sock port UAF — kernel memory corruption |
| CVE-2020-9907 | 2020 | Memory corruption in IOMobileFrameBuffer |
| CVE-2021-30983 | 2021 | IOMFB integer overflow → kernel r/w |
| CVE-2022-22587 | 2022 | IOMobileFrameBuffer memory corruption (0-day) |
| CVE-2023-28206 | 2023 | IOSurfaceAccelerator OOB write |

Each required: initial exploit → kernel read/write primitive → patch sandbox → load unsigned code.

---

## Entitlement injection (jailbreak technique)

```bash
# After gaining kernel r/w, inject entitlements into a target process:
# 1. Find the process's task port
# 2. Read the __LINKEDIT segment for code signature
# 3. Patch the entitlement blob (DER-encoded plist)
# 4. Update the SHA-256 hash chain
# Tools: ldid, codesign, substrate

# Simplified with ldid:
ldid -S entitlements.xml App.app/App
```

---

## Resources

- [Apple Platform Security Guide — App Sandbox](https://support.apple.com/guide/security/app-sandbox-sec15bfe098e/web)
- [Jonathan Levin — *iOS Internals* Vol. II](http://newosxbook.com)
- [Project Zero blog](https://googleprojectzero.blogspot.com) — ongoing iOS vuln research
