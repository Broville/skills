---
name: domain-intel
description: Passive domain reconnaissance using Python stdlib — subdomain discovery, SSL inspection, WHOIS lookup, DNS records, and availability checks with no API keys required
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks about subdomains of a domain
  - User wants to check SSL certificate details, expiry, or SANs
  - User asks who registered a domain or when it expires
  - User wants DNS records (A, AAAA, MX, NS, TXT, CNAME) for a domain
  - User asks if a domain name is available for registration
related_skills:
  - searxng-search
  - security-best-practices
---

# Domain Intelligence — Passive OSINT

## Description

Passive domain reconnaissance using only Python stdlib. Zero dependencies. Zero API keys. Works on Linux, macOS, and Windows. Includes subdomain discovery via Certificate Transparency logs, SSL certificate inspection, WHOIS lookups, DNS record resolution, domain availability checks, and bulk multi-domain analysis.

## Prerequisites

- Python 3.8+ (stdlib only: `socket`, `ssl`, `urllib`, `json`, `concurrent.futures`)
- Internet access for `crt.sh`, WHOIS servers, and Google DNS-over-HTTPS
- Note: WHOIS queries use TCP port 43 — may be blocked on restrictive networks

## Steps

### 1. Subdomain discovery (Certificate Transparency logs)

```bash
python3 SKILL_DIR/scripts/domain_intel.py subdomains example.com
```

Queries `crt.sh` HTTPS endpoint for all certificates issued for the domain. Returns a JSON list of subdomains found in certificate Subject Alternative Names (SANs).

### 2. SSL certificate inspection

```bash
python3 SKILL_DIR/scripts/domain_intel.py ssl example.com
```

Connects to the target on port 443 and inspects the TLS certificate. Returns: expiry date, cipher suite, SANs, issuer, subject.

This is the only "active" operation in the skill — it makes a TCP connection to the target domain.

### 3. WHOIS lookup

```bash
python3 SKILL_DIR/scripts/domain_intel.py whois example.com
```

Queries authoritative WHOIS servers (TCP port 43) for 100+ TLDs. Returns: registrar, creation date, expiration date, name servers, registrant info (if not redacted under GDPR).

### 4. DNS records

```bash
python3 SKILL_DIR/scripts/domain_intel.py dns example.com
```

Resolves A, AAAA, MX, NS, TXT, and CNAME records using Google DNS-over-HTTPS (HTTPS, firewall-friendly).

### 5. Domain availability check

```bash
python3 SKILL_DIR/scripts/domain_intel.py available coolstartup.io
```

Heuristic availability check using three passive signals:
1. DNS resolution (no DNS likely = unregistered)
2. WHOIS record presence
3. SSL certificate existence

Note: This is heuristic, not authoritative — confirm with a registrar for definitive availability.

### 6. Bulk multi-domain analysis

```bash
python3 SKILL_DIR/scripts/domain_intel.py bulk example.com github.com google.com
python3 SKILL_DIR/scripts/domain_intel.py bulk example.com github.com --checks ssl,dns
```

Run multiple checks on multiple domains in parallel. Use `--checks` to limit which checks run.

`SKILL_DIR` is the directory containing this SKILL.md file. All output is structured JSON.

## When to Use This vs Other Tools

| Task | Better Tool | Why |
|------|-------------|-----|
| "What does example.com do?" | web_extract | Gets page content, not DNS/WHOIS data |
| "Find info about a company" | web_search | General research, not domain-specific |
| "Is this website safe?" | web_search | Reputation checks need web context |
| "Check if a URL is reachable" | `curl -I` | Simple HTTP check |
| "Find subdomains of X" | **This skill** | Only passive source for this |
| "When does the SSL cert expire?" | **This skill** | Built-in tools can't inspect TLS |
| "Who registered this domain?" | **This skill** | WHOIS data not in web search |
| "Is coolstartup.io available?" | **This skill** | Passive availability via DNS+WHOIS+SSL |

## Pitfalls

1. **WHOIS port 43 may be blocked** — Restrictive corporate networks or firewalls may block TCP port 43. If WHOIS queries fail, try from a different network or use a VPN.
2. **GDPR redacts registrant info** — Many European WHOIS servers redact personal data. The tool will return what's available but note this limitation to the user.
3. **crt.sh is slow for popular domains** — Domains with thousands of certificates (e.g., large CDNs) can take 30+ seconds. Set reasonable expectations with the user before querying widely-used domains.
4. **Availability checks are heuristic** — The three-signal approach (DNS + WHOIS + SSL) is not authoritative. A newly registered domain may not have DNS or SSL yet, leading to false "available" results. Always confirm with a registrar API for definitive checks.
5. **SSL check is an active connection** — All other operations are passive (querying public databases), but `ssl` connects to the target domain on port 443. This may show up in server logs.

## Verification

1. **Subdomain discovery works**: Run `python3 SKILL_DIR/scripts/domain_intel.py subdomains github.com` and confirm it returns a JSON list with multiple subdomains
2. **SSL inspection works**: Run `python3 SKILL_DIR/scripts/domain_intel.py ssl github.com` and confirm it returns certificate expiry, issuer, and SANs
3. **DNS resolution works**: Run `python3 SKILL_DIR/scripts/domain_intel.py dns github.com` and confirm it returns A, MX, and NS records with values

## Cross-References

- **searxng-search** — General web research for domain/company context
- **security-best-practices** — Security assessment follow-up on discovered subdomains