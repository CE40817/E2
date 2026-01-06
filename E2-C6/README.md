# Ex7: SNI Ghost (domain fronting toy model)

Goal
- A middlebox blocks requests if it sees `forbidden.com` early in the connection.
- The origin server chooses content based on the `Host:` header.
- If you can make the middlebox see only `allowed.com` early, you can still reach the forbidden host at the origin.

Run
```bash
docker compose up --build
```

Targets
- Connect to `127.0.0.1:8443` (the middlebox).
- The origin is internal.

Student task
- Write `solve.py` so the origin returns the flag.
