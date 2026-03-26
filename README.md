# 🔐 iOS Security Research

Deep-dive notes on iOS security internals — BootROM exploits, Secure Enclave, activation lock architecture, and jailbreak techniques.

> Educational resource. For research and learning purposes only.

---

## Topics

| File | Contents |
|------|----------|
| [checkm8.md](research/checkm8.md) | CVE-2019-8900 — full technical breakdown |
| [secure-enclave.md](research/secure-enclave.md) | SEP architecture, UID key, T2 chip |
| [activation-lock.md](research/activation-lock.md) | How activation lock works end-to-end |
| [boot-chain.md](research/boot-chain.md) | iOS boot chain: BootROM → iBoot → kernel |
| [jailbreak-landscape.md](research/jailbreak-landscape.md) | Jailbreak types and current state |

---

## Quick reference: iOS boot chain

```
Power on
   │
   ▼
BootROM (immutable, in hardware)
   │  verifies iBoot signature
   ▼
iBoot (first-stage bootloader)
   │  verifies kernel + device tree
   ▼
XNU Kernel
   │
   ▼
launchd (PID 1) → system services → SpringBoard
```

**checkm8 targets the BootROM stage** — before any Apple-signed code loads.

---

## Chip security timeline

| Chip | Devices | BootROM exploit | Secure Boot | Notes |
|------|---------|-----------------|-------------|-------|
| A5 | iPhone 4S | ✅ checkm8 | Partial | limera1n era |
| A7–A11 | iPhone 5S–X | ✅ checkm8 | Yes | CVE-2019-8900 |
| A12 | iPhone XS/XR | ❌ | Yes + BPR | Secure Boot lockdown |
| A13+ | iPhone 11+ | ❌ | Yes + BPR | Pointer auth (PAC) |
| A14+ | iPhone 12+ | ❌ | Yes + BPR | Memory tagging (MTE) |

**BPR** = Boot Progress Register — can only be incremented, never decremented.

---

## Community resources

- **r/SetupA12** — A12+ activation research: https://reddit.com/r/SetupA12
- **The Apple Wiki** — checkm8 docs: https://theapplewiki.com/wiki/Checkm8_Exploit
- **iOS Activation Wiki** — full bypass guide: https://tom-app-a1353ad1.base44.app

---

> ⚠️ All information here is publicly documented security research. Never exploit vulnerabilities on devices you do not own.

*Maintained by [OutrageousStorm](https://github.com/OutrageousStorm)*
