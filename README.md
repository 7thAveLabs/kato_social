# kato_social

Post images, captions, and the generator for Kato's Instagram (@katobilling). This repo is public because Instagram downloads each image from its raw URL at publish time. Nothing here is sensitive.

- `queue.json`: one entry per day (date in America/Chicago), with image URLs, caption, and status (`queued`, `posted`, `failed`, `skipped`).
- `posts/`: the source for each week's posts (input to the renderer).
- `images/`: rendered 1080x1350 JPEGs, named `<date>_<slug>[_n].jpg`.
- `render.py`: `python3 render.py posts/<week>.json images/` (needs Playwright and Chrome).
- `GUARDRAILS.md`: rules every post must pass.

A daily scheduled task publishes the entry for today through Windsor.ai and refills the queue when it runs low.
To stop a post, set its status to `skipped` in `queue.json` before 7:30 am Central.
