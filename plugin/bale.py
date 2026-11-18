import requests
from apprise.decorators import notify


@notify(on="bale", name="Bale Messenger")
def send_bale(body, title, notify_type, meta, **kwargs):
    bot_id = meta.get("user")
    bot_secret = meta.get("password")
    chat_id = meta.get("host")

    if not bot_id or not bot_secret or not chat_id:
        return False

    token = f"{bot_id}:{bot_secret}"
    text = f"{title}\n{body}" if title else body

    try:
        response = requests.post(
            f"https://tapi.bale.ai/bot{token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        return isinstance(payload, dict) and payload.get("ok") is True

    except (requests.RequestException, ValueError):
        return False