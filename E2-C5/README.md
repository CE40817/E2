# Ex6: Silent Jammer (selective jamming)

Goal
- A sender transmits frames.
- A receiver sends an ACK when a frame is correct.
- You can jam only the ACK at the right time.
- If you jam too much, the receiver detects you.

Run
```bash
docker compose up --build
```

Student task
- Implement `solve_jam.py` so the receiver prints a flag.
