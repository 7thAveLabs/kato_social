# kato_social

Post images, videos, captions, and the generators for Kato's Instagram (@katobilling). This repo is public because Instagram downloads each file from its raw URL at publish time. Nothing here is sensitive.

- `queue.json`: up to three entries per day. `date` (America/Chicago) and `slot` decide when an entry posts; the date inside an id or file name is only a label and may differ.
  - `slot` 1 is the morning post (`post_time` 7:10 to 8:55) and goes to Instagram, Facebook and LinkedIn. Slots 2 (11:05 to 12:10) and 3 (17:40 to 19:30) go to Instagram and Facebook only. `networks` lists where an entry goes.
  - Other fields: `post_time` (HH:MM America/Chicago; add one hour for Toronto), `type` (`image`, `carousel`, `video`), file URLs, `caption`, `status` (`queued`, `posted`, `failed`, `skipped`).
- `posts/`: source for still and carousel posts (input to `render.py`).
- `images/`: rendered 1080x1350 JPEGs, plus `<id>_fallback.jpg` stills for videos.
- `videos/`: 1080x1920 MP4s and their cover images.
- `render.py`: `python3 render.py posts/<batch>.json images/`
- `anim.py` + `kinds.py` + `anims.json`: `python3 anim.py <name[,name]|all> <outdir> [preview]` (needs Playwright, Chrome, ffmpeg, numpy). `kinds.py` holds the Reel formats.
- `GUARDRAILS.md`: rules every post must pass.

Posts are scheduled in Metricool (brand "Kato") and publish on their own. A daily scheduled task checks that they went out, schedules anything missing, and writes new posts so the next 7 days are always full.
To stop a post, delete it in the Metricool planner.
