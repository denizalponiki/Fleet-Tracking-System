# ADR-005: Stateless authentication with JWT bearer tokens

- Status: Accepted
- Date: 2026-11-21
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: Ahmet Can Vurmaz (identity owner), Deniz Alp Oniki (DevOps), Mustafa Düşünceli (Frontend & UI)

## Context

Release 1 has its own user accounts with three roles (`STAFF`, `FLEET_MANAGER`,
`MAINTENANCE_OFFICER`); single sign-on is deferred (`docs/system_vision.md` §7.3). Every
operation except login needs an authenticated user and a role check on the server
(§10 Security). The contract already defines `POST /auth/login` returning `accessToken`,
`tokenType: Bearer` and `expiresIn: 3600`, and a global `bearerAuth` security scheme.
The API should stay stateless so it can restart during the demo without logging users out
in an inconsistent way, and the SPA calls it through the same origin (C4 Level 2).

## Decision

1. **Access token:** a signed JWT, algorithm **HS256**, secret from the `JWT_SECRET`
   environment variable (`.env`, never committed). Claims: `sub` (user id), `role`,
   `iat`, `exp`, `iss = fleetsync`. Lifetime **60 minutes** (`expiresIn: 3600`).
2. **Transport:** `Authorization: Bearer <token>` on every request except
   `POST /auth/login`. Missing, malformed, wrongly signed or expired tokens return
   `401 UNAUTHORIZED` (ADR-003).
3. **Authorisation on the server:** a FastAPI dependency `require_role(...)` in
   `app/shared/security.py` checks the role claim for each route, as stated in each
   operation's description in `openapi.yaml`. Ownership rules (a staff member sees only
   their own reservations) are checked in the module's service. Failures return
   `403 FORBIDDEN`.
4. **No refresh token in release 1.** After 60 minutes the user logs in again. Logout is
   done in the SPA by discarding the token.
5. **Token storage in the SPA:** in memory (React state), not in `localStorage`, to reduce
   exposure to XSS. A page reload requires logging in again; acceptable for release 1.
6. **Passwords:** stored only as **Argon2id** hashes (`argon2-cffi`), minimum length 8 as in
   `openapi.yaml`. Login answers `401 INVALID_CREDENTIALS` for both unknown email and wrong
   password, so it does not reveal which accounts exist.
7. **Role change:** a role change takes effect at the next login (at most 60 minutes later).

## Alternatives considered

| Option | Why not |
|---|---|
| Server-side sessions with a cookie | Needs a session store or sticky state and CSRF protection; the contract is already bearer-based |
| JWT in an HttpOnly cookie | Safer against XSS but needs CSRF tokens and changes the contract; reconsider if a refresh token is added |
| OAuth 2 / OpenID Connect with an identity provider | No institutional IdP available; deferred with SSO |
| RS256 (asymmetric keys) | Only one service verifies tokens; key management adds work without benefit |

## Consequences

- Positive: the API is stateless; any instance can verify a token; restarts do not need a
  session store.
- Positive: the same token works against the Prism mock (any bearer value) and the real API.
- Negative: a token cannot be revoked before it expires; a disabled user keeps access for up
  to 60 minutes. Accepted for release 1 given the short lifetime.
- Negative: storing the token in memory means a reload logs the user out.
- Follow-up: add `JWT_SECRET` to `.env.example` (DevOps, `docs/uml/deployment_diagram.md`
  DD-3); NFR document states the security measures (owner: QA and DevOps, approved by the
  Architect).

## Related

- `docs/openapi.yaml` `/auth/login`, `bearerAuth`, `TokenResponse`
- `docs/system_vision.md` §10 Security, Legal / ethical (KVKK)
- ADR-003 (error format)
- Issue #242
