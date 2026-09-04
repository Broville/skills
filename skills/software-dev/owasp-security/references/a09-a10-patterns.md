# OWASP A09 and A10 Implementation Patterns

Load this reference when implementing structured security logging or an SSRF-resistant outbound request path. Adapt examples to the project's framework and threat model; these snippets are starting points, not complete controls.

## A09: Structured Security Events

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()],
});

function logSecurityEvent(event: string, details: Record<string, unknown>) {
  logger.warn({ type: 'security', event, ...details });
}

logSecurityEvent('failed_login', { accountId, sourceIp, userAgent });
logSecurityEvent('access_denied', { actorId, resource, action });
```

Do not log passwords, session tokens, API keys, full request bodies, or regulated personal data. Use stable actor and request identifiers, define retention and access controls, protect integrity, and test that alert-worthy events reach the monitoring system.

## A10: SSRF-Resistant Outbound Requests

Use a maintained URL-policy or network library when possible. A robust implementation must:

1. Parse the URL and allow only required schemes and ports.
2. Match the normalized hostname against a strict allowlist.
3. Resolve every address and reject loopback, private, link-local, multicast, unspecified, and other non-public ranges for IPv4 and IPv6.
4. Connect only to the validated address while preserving the expected TLS server name.
5. Disable redirects or repeat the full policy for every redirect target.
6. Set small connection, response, and body-size limits.
7. Enforce the same policy with network egress controls.

```typescript
import { URL } from 'node:url';

const ALLOWED_HOSTS = new Set(['api.example.com', 'cdn.example.com']);

function validateOutboundUrl(candidate: string): URL {
  const url = new URL(candidate);
  if (url.protocol !== 'https:' || !ALLOWED_HOSTS.has(url.hostname)) {
    throw new Error('Outbound destination is not allowed');
  }
  return url;
}
```

The example performs only the first policy layer. The implementation must still validate DNS results, pin the validated destination for the connection, control redirects, and restrict network egress.
