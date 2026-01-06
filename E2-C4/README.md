# Ex5: Vampire DDoS (Regex backtracking DoS)

Goal
- A web endpoint uses a vulnerable regular expression.
- You can trigger catastrophic backtracking to slow the server.
- The server prints a flag after it detects sustained slowness.

Run
```bash
docker compose up --build
```

Student task
- Find an input that reliably makes the server slow.
- Automate the request so you can reproduce the slowdown and get the flag.
