"""Send today's Noon Verse alert to every phone in subscriptions.json.

Needs: pip install pywebpush
Needs: NOONVERSE_VAPID_KEY = the private key (PEM text). Never commit it.
Usage: python3 send_push.py "Body text"
"""
import json, os, sys, tempfile
from pywebpush import webpush, WebPushException

here = os.path.dirname(os.path.abspath(__file__))
subs = json.load(open(os.path.join(here, "subscriptions.json")))
pem = os.environ["NOONVERSE_VAPID_KEY"].replace("\\n", "\n")
with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
    f.write(pem)
    key_path = f.name

body = sys.argv[1] if len(sys.argv) > 1 else "Your verse for today is ready."
payload = json.dumps({"title": "Noon Verse", "body": body, "url": "./"})
sent = 0
for s in subs:
    try:
        webpush(subscription_info=s, data=payload, vapid_private_key=key_path,
                vapid_claims={"sub": "mailto:saniya@primusus.com"}, ttl=3600)
        sent += 1
    except WebPushException as e:
        print("failed:", s["endpoint"][:40], e.response.status_code if e.response is not None else e)
os.unlink(key_path)
print(f"sent {sent} of {len(subs)}")
