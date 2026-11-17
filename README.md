# kato_social

Post images, videos, captions, and the generators for Kato's Instagram (@katobilling). This repo is public because Instagram downloads each file from its raw URL at publish time. Nothing here is sensitive.

- `queue.json`: one entry per day (date in America/Chicago) with a random `post_time` (America/Chicago, between 7:10 and 8:55), type (`image`, `carousel`, `video`), file URLs, caption, and status (`queued`, `posted`, `failed`, `skipped`).
- `posts/`: source for still and carousel posts (input to `render.py`).
- `images/`: rendered 1080x1350 JPEGs, plus `<id>_fallback.jpg` stills for videos.
- `videos/`: 1080x1920 MP4s and their cover images.
- `render.py`: `python3 render.py posts/<batch>.json images/`
- `anim.py` + `anims.json`: `python3 anim.py <name|all> <outdir>` (needs Playwright, Chrome, ffmpeg, numpy).
- `GUARDRAILS.md`: rules every post must pass.

A daily scheduled task publishes today's entry through Windsor.ai and refills the queue when it runs low.
To stop a post, set its status to `skipped` in `queue.json` before 7:00 am Central.
