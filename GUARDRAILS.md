# Content guardrails for @katobilling

Every post and caption must pass all of these. If a draft cannot, drop it and write a different one.

1. No invented customers, quotes, hours saved, dollar results, percentages, or statistics. Use a number only if a founder supplied it with a source.
2. Describe only what joinkato.com says Kato handles today: payment posting and reconciliation (remittance, bank deposit verification, PMS posting, flagging what does not match). No claims about claim submission, denials, eligibility, banking, cards, or financing.
3. Never name a specific PMS as supported and never claim write access to one.
4. Product visuals use made-up sample data only (never real practice, patient, or payer data). No disclaimer label on the image (founder decision, Nov 16, 2026). When an image shows a product screen with dollar amounts, add "Example shown with sample data." to the caption.
5. Say "payer", not "insurance company". No em dashes. Product name is Kato.
6. No buttons, links, URLs, or "swipe"/"tap" prompts on images. Nothing on a post is tappable.
7. Lead with time back and relief from billing. Not a dashboard, not a copilot, not outsourced billing, not an AI chatbot.
8. Do not mention competitors. Do not reuse another brand's lines.
9. All text on images is set in the serif (headline) font, except inside product UI cards. Captions: one to three short sentences, plain and calm, at most three hashtags, no emoji.
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
- Vary the music: use a different `music` profile (calm, marimba, bell, keys, swell) from the previous video. Audio is synthesized by `anim.py`; never add third-party music.
- Every video entry needs a cover and a 4:5 fallback still (both written by `anim.py`).
