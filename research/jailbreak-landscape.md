# Jailbreak Landscape (2025–2026)

Current state of iOS jailbreaking — what works, what doesn't, and where research is headed.

---

## Active jailbreaks

| Jailbreak | Type | Chips | iOS | Status |
|-----------|------|-------|-----|--------|
| **palera1n** | Semi-tethered | A8–A11 | 15.0–16.x | ✅ Active |
| **checkra1n** | Semi-tethered | A8–A11 | 12.0–14.8.1 | ✅ Stable |
| **Dopamine** | Semi-untethered | A12–A15 | 15.0–15.4.1 | ✅ Active |
| **TrollStore** | Permanent signing | A8–A17 | 14.0–17.0 | ✅ Active (not jailbreak) |

---

## Jailbreak types explained

**Untethered** — Survives reboot without any action. Exploit runs automatically from on-device code. The gold standard. Currently: no active untethered jailbreak for iOS 15+.

**Semi-untethered** — Survives reboot but requires re-running an on-device app to re-jailbreak. Example: Dopamine (run app after each reboot).

**Semi-tethered** — Requires connection to a PC to re-jailbreak after reboot. Example: palera1n (connect USB, run palera1n on host machine).

**Tethered** — Cannot boot at all without the host tool. Impractical for daily use. Mostly historical.

---

## TrollStore (not a jailbreak)

TrollStore is a permanent IPA installer that exploits CoreTrust bugs to install apps with arbitrary entitlements — without a jailbreak.

| iOS | TrollStore version | Method |
|-----|-------------------|--------|
| 14.0–14.8.1 | TrollStore 1/2 | Multiple install methods |
| 15.0–15.5b4 | TrollStore 1/2 | Via TrollHelper / misaka |
| 15.5–15.7.x | TrollStore 2 | Via TrollInstallerMDC |
| 16.0–16.6.1 | TrollStore 2 | Via TrollInstallerX |
| 16.7–17.0 | TrollStore 2 | Via kfd exploit |

TrollStore-installed apps persist through reboots with no re-signing needed.

---

## Why A12+ jailbreaks are rare

1. **PAC (Pointer Authentication Codes)** — function pointers are cryptographically signed; forging them requires leaking the PAC key
2. **PPL (Page Protection Layer)** — prevents modifying page tables even from kernel context
3. **KTRR hardened** — kernel text is read-only in hardware
4. **BPR** — boot progress can't be rolled back
5. **No bootrom exploit** — A12+ BootROM is different silicon, different USB stack

Each of these must be bypassed independently. Finding a chain of exploits that defeats all of them simultaneously is extremely difficult.

---

## Where research is focused

- **CoreTrust bugs** — signing exploits that allow permanent app installation (TrollStore)
- **kfd exploits** — kernel-level file descriptor exploits for read/write primitives
- **PUAF (Physical Use-After-Free)** — memory corruption in IOSurface/IOKit
- **WebKit 0-days** — browser-based entry points (jailbreak.me style)
- **SEP research** — the last frontier; no public SEP exploit exists

---

## Historical timeline

| Year | Milestone |
|------|-----------|
| 2007 | First iPhone jailbreak (AppSnapp) |
| 2010 | JailbreakMe 2.0 (browser-based, Star) |
| 2014 | Pangu untethered (iOS 7.1–8.1) |
| 2019 | checkm8 discovered (axi0mX, A5–A11 forever) |
| 2020 | checkra1n goes mainstream |
| 2021 | unc0ver supports A12+ (15.0) |
| 2022 | Dopamine (A12–A15, 15.0–15.4.1) |
| 2022 | TrollStore released (permanent app signing) |
| 2023 | palera1n goes stable for iOS 15–16 |
| 2024 | kfd exploits extend TrollStore to iOS 17.0 |
| 2025 | Active research continues; no iOS 17+ full jailbreak |
