# iOS Boot Chain

How an iPhone boots — from power-on to SpringBoard.

---

## Full boot sequence

```
┌─────────────────────────────────────────────────────┐
│  STEP 1: BootROM                                     │
│  • Stored in read-only silicon (immutable)           │
│  • First code executed on power-on                   │
│  • Verifies iBoot signature using Apple root CA      │
│  • Entry point for checkm8 (DFU mode)                │
└────────────────────┬────────────────────────────────┘
                     │ verified
┌────────────────────▼────────────────────────────────┐
│  STEP 2: iBoot (Low-level bootloader)                │
│  • Loads device tree, kernel, and kernel extensions  │
│  • Verifies each against Apple-signed manifests      │
│  • Sets up memory protection (KTRR/PPL on A10+)      │
│  • Handles recovery mode and DFU transitions         │
└────────────────────┬────────────────────────────────┘
                     │ verified
┌────────────────────▼────────────────────────────────┐
│  STEP 3: XNU Kernel                                  │
│  • Hybrid Mach/BSD kernel                            │
│  • Sets up virtual memory, processes, IPC            │
│  • Loads kernel extensions (kexts)                   │
│  • Enforces code signing for all userspace code      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  STEP 4: launchd (PID 1)                             │
│  • First userspace process                           │
│  • Starts all system daemons                         │
│  • Includes: mobileactivationd (activation check)   │
└────────────────────┬────────────────────────────────┘
                     │ if activated
┌────────────────────▼────────────────────────────────┐
│  STEP 5: SpringBoard                                 │
│  • The iOS home screen / UI shell                    │
│  • Manages app launching and display                 │
└─────────────────────────────────────────────────────┘
```

---

## Where bypass tools intervene

| Method | Boot stage | How |
|--------|-----------|-----|
| checkm8 ramdisk | BootROM → before iBoot | Loads unsigned ramdisk instead of normal iOS |
| Janus tethered | After kernel, before launchd | Patches mobileactivationd in memory |
| NAND rework | Pre-boot (hardware) | Modifies activation data at rest on NAND |
| GSX unlock | Server-side | Changes Apple's database; device activates normally |

---

## Security features per generation

| Feature | Introduced | Purpose |
|---------|-----------|---------|
| Secure Boot | A7 | Chain of trust from BootROM |
| KPP (Kernel Patch Protection) | A9 | Prevents kernel patching at runtime |
| KTRR | A10 | Hardware read-only kernel text region |
| PPL (Page Protection Layer) | A12 | Protects page tables from modification |
| PAC (Pointer Authentication) | A12 | Cryptographic signing of function pointers |
| BPR (Boot Progress Register) | A12 | One-way register; prevents downgrade attacks |
| MTE (Memory Tagging) | A14 | Tags memory allocations to detect UAF |

**Note:** PAC and BPR are major reasons why checkm8-style exploits don't work on A12+.
