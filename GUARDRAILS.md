# Content guardrails for @katobilling

Every post and caption must pass all of these. If a draft cannot, drop it and write a different one.

1. No invented customers, quotes, hours saved, dollar results, percentages, or statistics. Industry statistics are allowed only if they are listed in STATS.md, worded as recorded there, with the source shown on the image and in the caption. Never present an industry statistic as a Kato result.
2. Describe only what joinkato.com says Kato handles today: payment posting and reconciliation (remittance, bank deposit verification, PMS posting, flagging what does not match). No claims about claim submission, denials, eligibility, banking, cards, or financing.
3. Never name a specific PMS as supported and never claim write access to one.
4. Product visuals use made-up sample data only (never real practice, patient, or payer data). No disclaimer label on the image (founder decision, Nov 16, 2026). When an image shows a product screen with dollar amounts, add "Example shown with sample data." to the caption.
5. Say "payer", not "insurance company". No em dashes. Product name is Kato.
6. No buttons, links, URLs, or "swipe"/"tap" prompts on images. Nothing on a post is tappable.
7. Lead with time back and relief from billing. Not a dashboard, not a copilot, not outsourced billing, not an AI chatbot.
8. Do not mention competitors. Do not reuse another brand's lines.
9. All text on images is set in the serif (headline) font, except inside product UI cards. Captions: one to three short sentences, plain and calm, no emoji. Open with the point, because the first line is what shows in the feed. Use the words a dentist or office manager would type into search (dental billing, payment posting, EOB, ERA, dental practice) naturally in the sentences. Three to five specific hashtags at the end, never more than five; they label the topic and do not add reach. On education carousels, add one line inviting a share, such as "Send this to whoever handles payment posting at your practice." Shares to a friend are the strongest signal for reaching people who do not follow us.
10. Golf is an occasional campaign theme (at most one post a week), not the identity.

## Rotation (per 7 days)
- 2 to 3 videos (see below), never on consecutive days
- 2 to 3 benefit-line stills (staggered type or headline on `wash`, `blur`, `bone`, or `dark`; at most one golf theme)
- 1 to 2 education carousels (4 to 5 slides, one billing concept each)
- at most 1 product card still
Do not repeat a headline used in the previous 4 weeks (check `posts/` and `queue.json`).

## Videos
- New text videos: add an entry to `anims.json` (word-by-word headline, 3 to 5 short lines) and render with `python3 anim.py <name> <outdir>`.
- The built-in videos (`steps`, `golf`, `timeback`, `reconcile`) may be reused, but not within 4 weeks of their last use.
- Sound: every video gets its own sound, designed around what happens in it (see the `_snd_*` functions in `anim.py`). No chime-per-step patterns and no sound that rises with each movement. For a new text video, write a new `_snd_*` function and name it in the `sound` field in `anims.json`; do not reuse another video's sound within 4 weeks. Audio is synthesized by `anim.py`; never add third-party music.
- Every video entry needs a cover and a 4:5 fallback still (both written by `anim.py`).

## What Instagram rewards (reviewed Nov 2026)
- Watch time, sends (shares by DM), and likes are the signals Instagram says matter most. Keep videos short (7 to 10 seconds) so they are watched to the end and loop.
- Reels reach people who do not follow us; carousels and stills mostly reach followers. Keep at least 4 videos in every 14 days.
- Make education posts worth forwarding to a colleague. That is the test for a carousel.

## Photo posts
- Use only photos in `photos/` (see `photos/CREDITS.md`). In a slide, set `"photo": "<file name without .jpg>"`; render.py applies the filter and white serif text.
- A label is a short staggered line; a statistic uses `stat`, `sub` and `source`.
- At most 3 photo or statistic posts per 7 days, and do not reuse a photo within 4 weeks.
