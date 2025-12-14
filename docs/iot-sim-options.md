# IoT SIM Options for Perth Metro

## Data Requirements

Each sensor transmits:
- ~500 bytes per message (JSON payload)
- 1 message per minute = 43,200 messages/month
- **~20-25 MB/month per sensor** (with overhead)

For 4 prototypes: ~100 MB/month total

---

## Australian IoT SIM Providers Comparison

### Tier 1: Lowest Cost (Recommended for Prototype)

#### M2MSIM.com.au ⭐ Best Value
| Plan | Monthly Cost | Data | Per MB (excess) |
|------|--------------|------|-----------------|
| 5MB | $3.00 | 5MB pooled | ~$0.60/MB |
| 10MB | $4.00 | 10MB pooled | ~$0.40/MB |
| Custom | Contact | 50MB+ | Negotiable |

- **Networks:** Telstra, Optus, Vodafone (roaming on all)
- **Bands:** 3G, 4G, LTE-M, NB-IoT
- **SIM cost:** $2 per SIM
- **Inactive SIM:** $1/month
- **Platform:** Cisco Jasper (enterprise-grade management)
- **Billing:** Monthly or annual

**For 4 prototypes @ 25MB each = 100MB/month**
- Option: 10x 10MB SIMs pooled = $40/month for 100MB
- Or negotiate custom 100MB plan

Website: [m2msim.com.au](https://www.m2msim.com.au/)

---

#### Cmobile (Optus Network)
| Feature | Details |
|---------|---------|
| Network | Optus 4G only |
| SIM cost | $4.00 ($3.50 bulk) |
| Excess data | $0.05/MB |
| SMS | $0.15 each |
| Contract | No lock-in |

**Pooled data plans** - all SIMs share one data allocation.

**For 4 prototypes @ 25MB each:**
- Buy appropriate pooled plan
- Excess at $0.05/MB is very cheap

Website: [cmobile.com.au](https://www.cmobile.com.au/m2m-sims-and-iot-plans/)

---

### Tier 2: Global/Flexible Options

#### Things Mobile (Global)
| Feature | Details |
|---------|---------|
| Coverage | 165+ countries incl. Australia |
| Per MB | $0.12 USD (~$0.18 AUD) |
| Monthly fee | $0.30 per active network |
| Billing | Pay-as-you-go, per KB |
| SIM cost | ~$5 |

**Pros:** No commitment, works internationally
**Cons:** Slightly higher per-MB cost

Website: [thingsmobile.com](https://www.thingsmobile.com/)

---

#### Hologram (Global)
| Feature | Details |
|---------|---------|
| Coverage | 200+ countries |
| Pay-as-you-go | $0.40/MB (expensive) |
| Plans | From $0.05/MB at volume |
| Platform | Excellent developer tools |

**Pros:** Best developer experience, global
**Cons:** Expensive for low volume

Website: [hologram.io](https://www.hologram.io/)

---

### Tier 3: Carrier Direct (More Expensive)

#### Telstra IoT
| Plan | Monthly | Data |
|------|---------|------|
| IoT Starter | ~$5 | 5MB |
| IoT Basic | ~$10 | 25MB |
| Shared pools | Custom | Varies |

- **SIM cost:** $2 per SIM
- **Network:** Telstra (best regional coverage)
- **Support:** Enterprise-grade
- **Cons:** More expensive, designed for business

Website: [telstra.com.au/small-business/internet-of-things](https://www.telstra.com.au/small-business/internet-of-things/data-sim-plans)

---

## Recommendation for 4 Prototypes

### Option A: M2MSIM (Best for Perth Metro)
```
4x SIMs @ 10MB each = $16/month base
Pooled = 40MB shared
If you exceed: negotiate custom plan
Setup: 4x $2 SIM = $8 one-time
```
**Total: ~$24 first month, $16/month ongoing**

### Option B: Cmobile (Simplest)
```
1x pooled plan (100-200MB)
4x SIMs @ $4 = $16 one-time
Excess data: $0.05/MB (very cheap)
```
**Total: Depends on plan, but excess is cheap**

### Option C: Things Mobile (Most Flexible)
```
4x SIMs @ $5 = $20 one-time
Pay only for what you use
~$0.18/MB = ~$18/month for 100MB
```
**Total: ~$38 first month, ~$18/month ongoing**

---

## SIM Module Compatibility

Your SIM7000A supports:
- LTE Cat-M1 (LTE-M)
- NB-IoT
- 2G fallback (being phased out)

**All listed providers support LTE-M on Australian networks.**

### APN Settings (Examples)

```cpp
// M2MSIM / Telstra
#define APN "telstra.m2m"

// Optus
#define APN "yesinternet"

// Vodafone
#define APN "live.vodafone.com"

// Things Mobile
#define APN "TM"
```

---

## Order of Operations

1. **Order SIMs** from M2MSIM or Cmobile (2-5 day delivery)
2. **Activate** via their web portal
3. **Configure APN** in firmware
4. **Test connectivity** before field deployment

---

## Sources

- [M2MSIM.com.au](https://www.m2msim.com.au/)
- [Cmobile IoT Plans](https://www.cmobile.com.au/m2m-sims-and-iot-plans/)
- [Things Mobile Australia](https://www.thingsmobile.com/)
- [Telstra IoT Plans](https://www.telstra.com.au/small-business/internet-of-things/data-sim-plans)
