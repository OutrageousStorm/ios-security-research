# iOS Activation Lock — Architecture

How Apple's Activation Lock system works from a security research perspective.

---

## System overview

```
┌──────────────┐        TLS POST          ┌──────────────────┐
│  iOS Device  │ ──────────────────────►   │ albert.apple.com │
│              │  ECID + IMEI + DevCert    │ (Activation Srv) │
│              │ ◄──────────────────────   │                  │
│              │  Signed activation record │                  │
└──────────────┘  (or error if locked)     └────────┬─────────┘
                                                    │
                                              ┌─────▼─────┐
                                              │   GSX DB   │
                                              │ IMEI→AppleID│
                                              │ Find My flag│
                                              └────────────┘
```

---

## Activation flow (detailed)

### Step 1: Device setup begins
When iOS boots to the Hello screen, `mobileactivationd` daemon starts and:
1. Reads the device's ECID (Exclusive Chip ID) from the Secure Enclave
2. Reads the IMEI from the baseband processor
3. Loads the Apple Device Certificate (pre-provisioned at factory)

### Step 2: Server handshake
The device POSTs to `albert.apple.com` with:
```json
{
  "ActivationInfo": {
    "UniqueChipID": "<ECID>",
    "InternationalMobileEquipmentIdentity": "<IMEI>",
    "DeviceCertRequest": "<DER-encoded CSR>"
  }
}
```

### Step 3: Server decision
Apple's activation server:
1. Looks up the IMEI in the **GSX database**
2. Checks if Find My iPhone was enabled (Activation Lock flag)
3. If locked: returns HTTP 403 + error body
4. If clear: issues a signed **activation record** (wildcard activation ticket)

### Step 4: Device stores record
The activation record is:
- Signed by Apple's CA
- Bound to the device's UID key (SEP)
- Written to `/var/root/Library/Lockdown/activation_records/`
- Verified by the kernel on each boot

---

## What bypass tools target

| Target | Method | Persistence |
|--------|--------|-------------|
| `mobileactivationd` | Patch the daemon to skip server check | Until restore (ramdisk) |
| Activation record file | Write a fake/spoofed record to disk | Until file is verified |
| In-memory injection | Inject record into running memory | Until reboot (tethered) |
| NAND storage | Modify activation partition directly | Permanent (hardware) |
| GSX database | Legitimate unlock request | Permanent (server-side) |

---

## The UID key problem

The activation record is cryptographically bound to the device's UID key:

```
ActivationRecord = Sign(Apple_CA, {
  ECID: device_ecid,
  DeviceBinding: HMAC(UID_Key, activation_nonce),
  WildcardTicket: signed_ticket
})
```

This means:
- ✗ You can't copy a valid activation record from one device to another
- ✗ You can't forge a record without Apple's signing key
- ✓ You CAN inject a spoofed record if the verification daemon is patched
- ✓ You CAN modify the NAND to trick the device into thinking it's already activated

---

## GSX unlock (the "real" unlock)

The only permanent, survives-everything unlock is a GSX database modification:

1. Carrier submits IMEI to Apple via GSX portal
2. Apple removes the Activation Lock flag from the IMEI record
3. Device contacts albert.apple.com → gets a valid activation record
4. Done forever — survives restores, updates, everything

This is what happens when you:
- Ask your carrier to unlock your phone
- Get Apple Support to remove Find My
- Purchase an "official iCloud removal" service (they submit to GSX)

---

## Attack surface summary

```
Level 0 (easiest):  Patch mobileactivationd in ramdisk  → A5–A11 via checkm8
Level 1 (medium):   Inject tethered activation record    → A12+ via Janus
Level 2 (hard):     NAND rework to modify stored data    → A12+ via hardware
Level 3 (hardest):  GSX database modification            → Server-side
Level ∞ (impossible): Break SEP / forge Apple's CA key   → Not happening
```
