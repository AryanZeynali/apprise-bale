<div align="center">

# Apprise Bale

**Send text notifications to Bale from Apprise.**

A lightweight, file-based Apprise custom notification plugin for the Bale Bot API.

[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue.svg)](LICENSE)
![Integration: custom plugin](https://img.shields.io/badge/Apprise-custom_plugin-6950a1)
![Scope: text only](https://img.shields.io/badge/messages-text_only-168b74)

</div>

> This is a community custom plugin. It is not built into or officially supported by Apprise.

## What it supports

| Capability | Support |
| --- | --- |
| Apprise CLI | Yes, with `-P` / `--plugin-path` |
| Apprise Python library | Yes, with `AppriseAsset(plugin_paths=...)` |
| Apprise API container | Yes, with `APPRISE_PLUGIN_PATHS` |
| Bale messages | Text via `sendMessage`, with an optional title prefix |
| Destinations | One Bale chat per URL |
| Attachments and media | Not supported |

The plugin calls Bale's `sendMessage` method over HTTPS. When a title is provided, the sent text is `title`, a newline, then the body. Requests time out after 15 seconds. Text is forwarded as-is; Bale applies its default text formatting.

## Requirements

- Python installed for Apprise CLI or library use
- [Apprise](https://github.com/caronc/apprise)
- `requests`
- A Bale bot token and a chat the bot can message

Install the Python dependencies for CLI or library use:

```bash
python -m pip install apprise requests
```

## Create a Bale bot and find a chat ID

1. Create a bot with [Bale's BotFather](https://ble.ir/botfather) and keep the token private. Bale issues a token in the form `bot_id:token_secret`.
2. Open a conversation with the bot and send `/start` so Bale has an update for your chat. For a group, add the bot and grant the permissions it needs to send messages.
3. Use Bale's [`getUpdates` method](https://docs.bale.ai/) to inspect the update. The request URL has this shape: `https://tapi.bale.ai/bot<BOT_ID>:<TOKEN_SECRET>/getUpdates`. Read the numeric value at `result[].message.chat.id`; if you use a webhook, follow Bale's instructions for switching to `getUpdates` first. Keep the token private when calling the method.

This project documents numeric chat IDs. Keep the complete Apprise URL private because it contains the bot token.

## Configure the Apprise URL

```text
bale://<bot_id>:<token_secret>@<chat_id>
```

| URL part | Value |
| --- | --- |
| `bot_id` | The number before `:` in the Bale bot token |
| `token_secret` | The part of the Bale bot token after `:` |
| `chat_id` | The numeric Bale chat ID |

If Bale gives you a token in the form `BOT_ID:TOKEN_SECRET`, split it at the colon as shown above. Replace every value in the examples below with your own. Do not commit real URLs or tokens to source control.

## Use with the Apprise CLI

Clone this repository, then run Apprise with the `plugin` directory on its plugin path:

```bash
git clone https://github.com/pooya220/apprise-bale.git
cd apprise-bale

apprise \
  -P ./plugin \
  --title "Deployment complete" \
  --body "The service is ready." \
  'bale://BOT_ID:TOKEN_SECRET@CHAT_ID'
```

`-P` and `--plugin-path` tell the CLI where to scan for custom plugins. The directory scan is not recursive, so point it directly at the directory containing `bale.py`.

## Use with the Apprise Python library

```python
import os

from apprise import Apprise, AppriseAsset

asset = AppriseAsset(plugin_paths=["./plugin"])
app = Apprise(asset=asset)
app.add(os.environ["BALE_URL"])

sent = app.notify(
    title="Deployment complete",
    body="The service is ready.",
)
if not sent:
    raise SystemExit("Apprise could not send the Bale notification")
```

Set `BALE_URL` in your process environment to the URL from the previous section. Keep the value in a protected secret store or local environment file that is not committed.

## Use with the Apprise API container

Save this as `compose.yaml` in the repository root. It mounts only the plugin directory and keeps the example API bound to the local machine:

```yaml
services:
  apprise:
    image: caronc/apprise:latest
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      APPRISE_PLUGIN_PATHS: /plugin
      APPRISE_STATELESS_MODE: enabled
    volumes:
      - ./plugin:/plugin:ro
```

Start the API:

```bash
docker compose up -d
```

Send a stateless notification to `http://127.0.0.1:8000/notify`:

```bash
curl --request POST \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["bale://BOT_ID:TOKEN_SECRET@CHAT_ID"],
    "title": "Deployment complete",
    "body": "The service is ready."
  }' \
  http://127.0.0.1:8000/notify
```

The API reads custom plugin files from the path in `APPRISE_PLUGIN_PATHS`. This local example does not enable authentication; keep it on a trusted machine or network, and configure authentication and HTTPS before allowing remote access. For a real deployment, store the Bale URL in a protected Apprise configuration and send to its key instead of placing the URL in each request.

## Troubleshooting

- **Unknown `bale://` schema:** confirm the plugin path points to the directory containing `bale.py`; restart the Apprise API after changing mounted plugin files.
- **Delivery fails:** check the bot token and numeric chat ID, and confirm the bot can send messages in that chat. Bale must return `ok: true` for Apprise to report success.
- **No chat ID appears:** send a message to the bot, then check for a pending update with `getUpdates`. A configured webhook may affect update retrieval.

## Security

The bot token is part of the URL. Treat the full `bale://` URL like a password: keep it out of public repositories, screenshots, logs, and shared shell history. Apprise imports custom plugin modules during plugin discovery, so only load code from a source you trust.

## Project links

- [Bale Bot API documentation](https://docs.bale.ai/)
- [Apprise custom notification decorator](https://appriseit.com/library/extending/decorator/)
- [Apprise CLI plugin paths](https://appriseit.com/cli/usage/)
- [Apprise API environment variables](https://appriseit.com/api/reference/environment/)
- [Apprise API notification usage](https://appriseit.com/api/usage/)
- [Apprise project](https://github.com/caronc/apprise)

## License

[BSD 2-Clause](LICENSE)