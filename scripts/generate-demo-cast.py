#!/usr/bin/env python3
"""Generate asciicast v2 file for FormBackend demo GIF."""

import json
import time
import os

CAST_PATH = os.environ.get("CAST_PATH", "/tmp/formbackend-demo.cast")

events = []

def at(time_sec, event_type, data):
    events.append([time_sec, event_type, data])

t = 0.0

# Header / title screen
at(t, "o", "\033[2J\033[H")
t += 0.3
at(t, "o", "\033[1;36m")
at(t, "o", "┌─────────────────────────────────────────────────────────────────────┐\r\n")
at(t, "o", "│        \033[1;33mFormBackend API\033[1;36m — Demo in 10 Seconds                      │\r\n")
at(t, "o", "└─────────────────────────────────────────────────────────────────────┘\033[0m\r\n")
t += 0.1
at(t, "o", "\033[2mOpen-core self-hosted form backend.\033[0m\r\n")
at(t, "o", "\033[2mCollect HTML form submissions without writing backend code.\033[0m\r\n")
t += 0.5

# Step 1
at(t, "o", "\r\n\033[1;33m▸ Step 1: Deploy\033[0m\r\n")
at(t, "o", "\033[2m────────────────────────────────────────────────────────────────────\033[0m\r\n")
t += 0.2
at(t, "o", "\033[32m$ \033[0m")
at(t, "o", "docker run -d --name formbackend \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -e DATABASE_URL=postgresql://user:pass@db:5432/formbackend \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -e JWT_SECRET=change-me-to-a-random-secret \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -p 8000:8000 \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  ghcr.io/naswarch/formbackend:latest\r\n")
t += 0.8
at(t, "o", "\r\n\033[2ma1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6\033[0m\r\n")
t += 0.3

# Step 2
at(t, "o", "\r\n\033[1;33m▸ Step 2: Create a form\033[0m\r\n")
at(t, "o", "\033[2m────────────────────────────────────────────────────────────────────\033[0m\r\n")
t += 0.2
at(t, "o", "\033[32m$ \033[0m")
at(t, "o", "curl -X POST http://localhost:8000/api/forms \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -H \"Authorization: Bearer \033[2m<your-token>\033[0m\" \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -H \"Content-Type: application/json\" \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -d '{\"name\":\"Contact Form\"}'\r\n")
t += 1.0
at(t, "o", "\r\n\033[36m{\r\n  \"endpoint\": \"f-abc123\",\r\n  \"name\": \"Contact Form\",\r\n  \"status\": \"active\"\r\n}\033[0m\r\n")
t += 0.5

# Step 3
at(t, "o", "\r\n\033[1;33m▸ Step 3: Add to your HTML\033[0m\r\n")
at(t, "o", "\033[2m────────────────────────────────────────────────────────────────────\033[0m\r\n")
t += 0.2
at(t, "o", "\033[2m  <form action=\"http://localhost:8000/api/f/f-abc123\" method=\"POST\">\033[0m\r\n")
t += 0.03
at(t, "o", "\033[2m    <input type=\"text\" name=\"name\" placeholder=\"Your name\">\033[0m\r\n")
t += 0.03
at(t, "o", "\033[2m    <input type=\"email\" name=\"email\" placeholder=\"Your email\">\033[0m\r\n")
t += 0.03
at(t, "o", "\033[2m    <textarea name=\"message\" placeholder=\"Your message\"></textarea>\033[0m\r\n")
t += 0.03
at(t, "o", "\033[2m    <button type=\"submit\">Send</button>\033[0m\r\n")
at(t, "o", "\033[2m  </form>\033[0m\r\n")
t += 0.5

# Step 4
at(t, "o", "\r\n\033[1;33m▸ Step 4: Submit data\033[0m\r\n")
at(t, "o", "\033[2m────────────────────────────────────────────────────────────────────\033[0m\r\n")
t += 0.2
at(t, "o", "\033[32m$ \033[0m")
at(t, "o", "curl -X POST http://localhost:8000/api/f/f-abc123 \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -d \"name=Jane Doe\" \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -d \"email=jane@example.com\" \\\r\n")
t += 0.03
at(t, "o", "  \033[2m\\\033[0m  -d \"message=This took me 10 seconds!\"\r\n")
t += 1.2
at(t, "o", "\r\n\033[32m{\r\n  \"success\": true,\r\n  \"message\": \"Form submitted successfully\",\r\n  \"id\": \"sub_xyz789\"\r\n}\033[0m\r\n")
t += 0.3

# Done
at(t, "o", "\r\n\033[1;33m✓ Done!\033[0m \033[2mSubmission stored. Email notification sent. Dashboard updated.\033[0m\r\n")
t += 0.1
at(t, "o", "\r\n\033[2m────────────────────────────────────────────────────────────────────\033[0m\r\n")
at(t, "o", "\r\n\033[1m📊 50 free submissions/month · Pay-as-you-grow from 8€\033[0m\r\n")
at(t, "o", "\033[1m🔗 \033[34mhttps://github.com/NasWarch/formbackend\033[0m\r\n")
at(t, "o", "\033[1m🐳 docker run ghcr.io/naswarch/formbackend:latest\033[0m\r\n")
at(t, "o", "\r\n")

# Build the asciicast
header = {
    "version": 2,
    "width": 90,
    "height": 24,
    "timestamp": int(time.time()),
    "title": "FormBackend API - Demo",
    "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"},
}

lines = [json.dumps(header)]
for ts, etype, data in events:
    lines.append(json.dumps([round(ts, 2), etype, data]))

with open(CAST_PATH, "w") as f:
    f.write("\n".join(lines))
    f.write("\n")

print(f"Cast file written: {CAST_PATH} ({len(events)} events, {t:.1f}s duration)")
