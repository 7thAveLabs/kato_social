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
9. All text on images is set in the serif (headline) font, except inside product UI cards. Captions: one to three short sentences, plain and calm, no emoji. Open with the point, because the first line is what shows in the feed. Use the words a dentist or office manager would type into search (dental billing, payment posting, EOB, ERA, dental practice) naturally in the sentences. Three to five specific hashtags at the end, never more than five; they label the topic and do not add reach. Push them out of sight: after the caption text, add five lines that each contain only a period, then the hashtags on the last line (caption text + "\n.\n.\n.\n.\n.\n" + hashtags). On education carousels, add one line inviting a share, such as "Send this to whoever handles payment posting at your practice." Shares to a friend are the strongest signal for reaching people who do not follow us.
10. Golf is an occasional campaign theme (at most one post a week), not the identity.

## Who we are talking to (founder direction, Nov 26, 2026)
Office managers and clinic owners. Every post is about a moment they recognize or about getting time back: the stack of EOBs, the deposit that does not match, month-end, the question nobody can answer without an afternoon of checking. Write the first line for the office manager who would forward it to the dentist, or the dentist who would forward it to the office manager.

## Daily schedule: 3 posts a day on Instagram and Facebook, 1 on LinkedIn
- Slot 1 (morning): the main post. Any type. Goes to Instagram, Facebook and the LinkedIn company page.
- Slot 2 (midday) and slot 3 (evening): Instagram and Facebook only. Reels by default; about one in seven is an education carousel.
- Never two posts in the same format on the same day (for example two definition Reels, or two message threads).
- Slot 1 rotation per 7 days: 2 to 3 videos, 2 to 3 stills or photo posts, 1 to 2 education carousels, at most 1 statistic.
- Do not repeat a headline or opening line used in the previous 4 weeks (check `posts/`, `anims.json` and `queue.json`). At most one golf theme a week.

## Videos
- Declare each video in `anims.json` and render with `python3 anim.py <name> <outdir>`. Check layout first with `python3 anim.py <name> <outdir> preview` and look at the three stills.
- Formats (`kind`): `chat` (message thread ending with Kato's reply), `todo` (a list that gets crossed off), `clock` (hands wind back), `match` (remittance against deposit, sample data), `define` (a billing term, defined), `bars` (a day re-divided), `typed` (a question, typed out and answered), `phone` (a text thread with Kato, see the rule below), and `stagger` (word by word). The built-in videos (`steps`, `golf`, `timeback`, `reconcile`) may be reused, but not within 4 weeks. New formats are welcome: add a builder to `kinds.py`.
- `phone` (texting Kato from a phone) advertises something we are still building. Every `phone` video must keep the note "In the works. Not live yet." on its end card and say in the caption that it is not live, with the line "Send us a DM with the word TEXT for early access." Remove this rule only when a founder says texting has shipped. At most two a week. It is Kato's own messaging screen: no platform names, logos or brand marks. Sample figures only, never a patient name, and the caption carries "Example shown with sample data." These may run up to 14 seconds.
- Use every format before repeating one, and do not use the same format twice in 3 days.
- Start with the hook: the first thing on screen is the recognizable moment or the question, not the brand line. Keep videos 7 to 11 seconds.
- Keep everything that matters between y=250 and y=1560; Reels cover the top and bottom of the frame.
- Illustrations of time (`clock`, `bars`) never show a number of hours or a percentage. They are pictures of the idea, not results.
- Sound: every video has its own sound. Videos from `kinds.py` get one generated from their name (`_auto_sound` in `anim.py`), which keeps its own pace and never plays a note per on-screen step. A hand-written `_snd_*` function can be named in the `sound` field instead. Audio is synthesized by `anim.py`; never add third-party music.
- Every video entry needs a cover and a 4:5 fallback still (both written by `anim.py`).
- Voiceover videos: when a founder supplies a recorded voiceover, it replaces the generated sound and its script is shown as on-screen text, because most viewers watch with sound off.

## What Instagram rewards (reviewed Nov 2026)
- Watch time, sends (shares by DM), and likes are the signals Instagram says matter most. Keep videos short (7 to 11 seconds) so they are watched to the end and loop.
- Reels reach people who do not follow us; carousels and stills mostly reach followers. In the first 10 days, Reels averaged 323 views on Instagram, the one carousel 225, and stills 67.
- Make education posts worth forwarding to a colleague. That is the test for a carousel.

## Photo posts
- Use only photos in `photos/` (see `photos/CREDITS.md`). In a slide, set `"photo": "<file name without .jpg>"`; render.py applies the filter and white serif text.
- A label is a short staggered line; a statistic uses `stat`, `sub` and `source`.
- At most 3 photo or statistic posts per 7 days, and do not reuse a photo within 3 weeks.
