# Secure Enclave Processor (SEP)

Architecture and security properties of Apple's Secure Enclave.

---

## Overview

The Secure Enclave Processor (SEP) is a dedicated security coprocessor embedded in every Apple SoC from A7 (iPhone 5s, 2013) onwards. It runs its own OS (sepOS), has its own encrypted memory, and is completely isolated from the main application processor.

**Key property:** Even if the main CPU is fully compromised, the SEP remains secure. The UID key is never exposed outside the SEP.

---

## What the SEP does

| Function | Details |
|----------|---------|
| **UID key storage** | Unique 256-bit AES key fused at manufacture. Never readable by software. |
| **Biometric processing** | Touch ID / Face ID templates stored and compared inside SEP |
| **Disk encryption** | Derives per-file encryption keys from the UID key |
| **Activation binding** | Activation records are cryptographically tied to the UID key |
| **Secure boot** | Verifies its own firmware independently of the main CPU |
| **Counter lockout** | Enforces passcode attempt limits in hardware |

---

## UID Key

The UID key is the root of trust for device security:

```
UID key (fused in SEP at factory)
    │
    ├─► File system encryption (per-file keys derived via AES-CBC)
    ├─► Activation record binding (record is useless on any other device)
    ├─► Passcode key wrapping
    └─► Backup encryption
```

**You cannot extract the UID key.** Not with checkm8, not with NAND rework, not with any known technique. This is why "cloning" activations between devices is impossible.

---

## SEP generations

| Chip | SEP version | Notable additions |
|------|-------------|------------------|
| A7 (iPhone 5s) | SEP v1 | First SEP, Touch ID |
| A9 (iPhone 6S) | SEP v2 | Touch ID gen 2 |
| A11 (iPhone X) | SEP + Neural Engine | Face ID |
| A12 (iPhone XS) | SEP + Secure Storage | Encrypted key hierarchy |
| A14+ | SEP + PAC | Pointer Authentication Codes |
| M1/M2 (Mac) | T2 equivalent | Full disk encryption for Mac |

---

## Why checkm8 doesn't break SEP

checkm8 gives code execution in **BootROM** context — before iOS loads. But:

1. The SEP has its own independent boot process
2. SEP firmware is verified by the SEP itself, not the main CPU
3. The UID key never leaves the SEP — not even in DFU mode
4. SEP communication is through a mailbox interface; it ignores unsigned requests

Result: checkm8 can bypass activation at the software level (by patching the activation daemon), but the underlying device encryption and biometric data remain fully protected.

---

## References

- [Apple Platform Security Guide](https://support.apple.com/guide/security/welcome/web)
- [DEF CON 26 — Getting Into the Guts of the Secure Enclave Processor](https://www.youtube.com/watch?v=7UNeUT3tqFg)
