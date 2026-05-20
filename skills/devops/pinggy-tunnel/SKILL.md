---
name: pinggy-tunnel
description: Expose local services to the public internet via Pinggy SSH tunnels. Zero-install — uses the system SSH client for HTTP/HTTPS/TCP tunnels with optional auth gates and CORS.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to expose a local port, share a dev server, or get a public URL
  - User needs to receive webhook callbacks during local development
  - User wants to tunnel a local service without installing cloudflared or ngrok
  - User asks for a quick public URL for testing or demonstration
related_skills:
  - deployment-procedures
  - watchers
---

# Pinggy Tunnel

## Description

Expose a local service (dev server, webhook receiver, MCP endpoint, demo) to the public internet using a Pinggy SSH reverse tunnel. No daemon to install — the system's SSH client connects to `a.pinggy.io:443` and Pinggy returns a public HTTP/HTTPS URL.

**Third-party risk notice:** All data flows through Pinggy's SSH relay server. Do not tunnel sensitive services without enabling access control (`b:`, `k:`, or `w:` flags). Free-tier tunnels expire after 60 minutes. For production use, consider self-hosted alternatives or Pinggy's paid tier.

Free tier: 60-minute tunnels, random subdomain, no signup required. Pro tier adds persistent subdomains and removes the time cap.

## Prerequisites

- `ssh` on PATH (verify with `ssh -V`) — default on Linux, macOS, and Windows 10+
- A local service listening on `127.0.0.1:<port>` before starting the tunnel
- Optional: `PINGGY_TOKEN` env var for Pro features (persistent subdomain, no time cap)

## Steps

### Step 1: Confirm a Local Origin Is Listening

```bash
curl -sI http://127.0.0.1:8000/ | head -1
# Expect: HTTP/1.x 200 (or any non-connection-refused response)
```

If nothing is listening, start a simple server first:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

### Step 2: Launch the Tunnel as a Background Process

```bash
LOG=/tmp/pinggy-8000.log
nohup ssh -p 443 \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    -R0:localhost:8000 free@a.pinggy.io \
    > "$LOG" 2>&1 &
echo $! > /tmp/pinggy-8000.pid
```

`StrictHostKeyChecking=no` and `UserKnownHostsFile=/dev/null` skip the first-run host-key prompt. `ServerAliveInterval=30` prevents idle NAT disconnections.

### Step 3: Parse the Public URL

```bash
sleep 4
grep -oE 'https://[a-z0-9-]+\.[a-z]+\.pinggy\.link' /tmp/pinggy-8000.log | head -1
```

Expected output resembles:
```
https://yqycl-98-162-69-48.a.free.pinggy.link
```

### Step 4: Verify the Tunnel Works

```bash
curl -sI https://<the-url>/ | head -3
# Expect 200/302/whatever the local origin returns
```

A `502 Bad Gateway` means the SSH session is up but the local origin is not listening — return to Step 1.

### Step 5: Tear Down

```bash
kill "$(cat /tmp/pinggy-8000.pid)"
# Or if the pid file was lost:
pkill -f 'ssh -p 443 .* free@a\.pinggy\.io'
```

### Access Control Flags

Pinggy stacks control flags in the SSH username separated by `+`. Always quote the full `user@host` argument:

| Keyword | Effect |
|---------|--------|
| `b:user:pass` | HTTP Basic auth gate |
| `k:token` | Bearer-token gate (`Authorization: Bearer <token>`) |
| `w:CIDR` | IP whitelist (single IP or CIDR) |
| `co` | Add CORS headers (`Access-Control-Allow-Origin: *`) |
| `x:https` | Force HTTPS redirect |

Combine freely: `"b:admin:secret+co+x:https+free@a.pinggy.io"`

## Pitfalls

1. **60-minute hard cap on the free tier.** The SSH session terminates at 60 minutes and the URL goes dead. For longer shares, use `PINGGY_TOKEN` (Pro) or auto-restart with a shell loop (note: the URL changes on every restart for free-tier).
2. **Free-tier URL is random and changes on restart.** Never bookmark or hardcode it. Re-parse from the log each time.
3. **Concurrent free tunnels limited to one per source IP.** Starting a second tunnel from the same machine usually kills the first. Pro tier lifts this.
4. **Don't tunnel sensitive services without access control.** A bare HTTP tunnel is reachable by anyone with the URL. Always use `b:`, `k:`, or `w:` for non-public services.
5. **`+` in usernames must be quoted.** Always wrap the `user@host` argument in double quotes to avoid shell interpretation issues.

## Verification

1. **End-to-end: spin up a trivial origin, tunnel it, hit it, tear down:**
   ```bash
   python3 -m http.server 18000 --bind 127.0.0.1 >/tmp/origin.log 2>&1 &
   ORIGIN_PID=$!
   
   nohup ssh -p 443 \
       -o StrictHostKeyChecking=no \
       -o UserKnownHostsFile=/dev/null \
       -R0:localhost:18000 free@a.pinggy.io >/tmp/pinggy-verify.log 2>&1 &
   SSH_PID=$!
   
   sleep 5
   URL=$(grep -oE 'https://[a-z0-9-]+\.[a-z]+\.pinggy\.link' /tmp/pinggy-verify.log | head -1)
   curl -sI "$URL/" | head -1
   # Expect: HTTP/2 200
   
   kill "$SSH_PID" "$ORIGIN_PID"
   ```