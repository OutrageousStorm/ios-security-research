# checkm8 — CVE-2019-8900

Technical breakdown of the checkm8 BootROM exploit.

**Disclosed by:** axi0mX  
**Date:** September 27, 2019  
**CVE:** CVE-2019-8900  
**Type:** Use-after-free in USB DFU handler  
**Affected chips:** A5 through A11 (iPhone 4S through iPhone X)

---

## What is it?

checkm8 is an unpatchable vulnerability in Apple's **BootROM** — the first code that runs when a device powers on. It exists in the USB Device Firmware Upgrade (DFU) mode handler, specifically in how the BootROM manages USB setup packets.

Because BootROM is stored in **read-only silicon**, Apple cannot patch it via software updates on existing hardware. Every A5–A11 device ever made is permanently vulnerable.

---

## The vulnerability

The bug is a **use-after-free** in the USB control transfer handler:

1. BootROM allocates a buffer for the DFU image transfer
2. An attacker sends a specially crafted USB setup packet that triggers the buffer to be freed prematurely
3. The BootROM continues using the freed pointer (UAF)
4. By sending additional crafted packets, the attacker reclaims the freed memory with controlled data
5. This redirects execution to attacker-controlled code

The key insight: USB setup packets can stall and unstall independently, and the timing window in the BootROM's USB stack was exploitable with precise packet sequencing.

---

## What it enables

With code execution in BootROM context, an attacker can:

- **Load unsigned code** — bypass Apple's code signing entirely at the hardware level
- **Boot a custom ramdisk** — a temporary OS in RAM for patching, data extraction, or bypass
- **Dump the BootROM** itself for further analysis
- **Patch the kernel** before it loads
- **Bypass activation lock** — patch the activation validation daemon before iOS boots

---

## What it does NOT do

- ✗ Does not break the Secure Enclave (SEP runs independently)
- ✗ Does not decrypt user data (still protected by UID key in SEP)
- ✗ Does not survive a restore (ramdisk-based changes are temporary)
- ✗ Does not affect A12+ chips (different BootROM, different USB stack)

---

## Exploitation flow

```
1. Put device in DFU mode (hold buttons)
2. Send crafted USB setup packets to trigger UAF
3. Heap spray to gain controlled execution
4. Overwrite BootROM exception vectors
5. Load and execute unsigned payload (e.g. pongoOS or custom ramdisk)
6. Payload patches activation daemon or loads full OS environment
```

Tools that use checkm8: `checkra1n`, `palera1n`, `ipwndfu`, `Sliver`, `F3arRa1n`

---

## References

- [The Apple Wiki — checkm8](https://theapplewiki.com/wiki/Checkm8_Exploit)
- [SentinelOne analysis](https://www.sentinelone.com/blog/checkm8-5-things-you-should-know-new-ios-boot-rom-exploit/)
- [axi0mX original tweet](https://twitter.com/axi0mx/status/1177542201670168576)
- [Technical PDF analysis](https://www.elabforensics.com/wp-content/uploads/sites/4/2021/01/Technical-analysis-of-the-checkm8-exploit.pdf)
