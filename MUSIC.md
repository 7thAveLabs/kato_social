# Music and sound on Kato Reels

From Nov 27, 2026 Reels use licensed music and sound effects from Epidemic Sound (Obay's account) in place of the generated sound.
Only the finished videos live in this repo. Never commit a downloaded track or sound effect file.

| Reel | Track | Artist |
|---|---|---|
| 2026-11-27_fri_list | For Chamela | Will Harrison |
| 2026-11-27_did_it_post | Streets of Missouri | Peace Reels |
| 2026-11-28_take_it_back | Next Time | Dovetail |
| 2026-11-28_era | Where I Want to Be | Sunfish Grove |
| 2026-11-29_three_checks | A Walk Among the Clouds | Imprismed |
| 2026-11-29_why_no_match | Scarily Similar | Alfie-Jay Winters |
| 2026-11-30_office_afternoon | Zaidi | Sonny Simba |
| 2026-11-29_records_reconciled (posts Nov 30) | Morning Light | Onda Norte |
| 2026-12-01_time_back (posts Dec 5) | Ice Fields | Martin Gauffin |
| 2026-12-01_ask_kato | jokk | bomull |
| 2026-12-01_reconciled | Starlight Over Frosty Plains | William Benckert |
| 2026-12-02_month_end | Through the Blaze | Rasmus Faber |
| 2026-12-02_who_posts | Walking Away | Peace Reels |
| 2026-12-03_bulk_payment | For Some Time (Instrumental Version) | Daniel Gunnarsson |
| 2026-12-03_says_paid | Snoozy Sue | Mid Knight |
| 2026-12-04_deposits_match | Meadows of North | William Claeson |
| 2026-12-04_eobs_posted | Toner | Ever So Blue |

Message sounds on the thread Reels: Epidemic Sound "User Interface, Alert, Notification, Message, Text 05" (sent, sound effect id d574019e-3f55-4784-b092-36ebb3fb4221) and "Text 02" (received, id 7bb0265e-6b48-4e13-a3be-83170b4255d1).

How a track is applied (`python3 score.py <video.mp4> <track.mp3>`, see its docstring): the video stream is kept as rendered; the track is cut from its first full section to the video's length,
faded in over 0.3 s and out over 1.4 s, levelled to about -17 LUFS, and mixed with any message sounds at the moments messages appear.
Do not reuse a track within 4 weeks.

Choosing tracks: instrumental only (no vocals), 70 to 125 bpm, moods such as hopeful, calm, relaxed, laid back, optimistic, warm. Avoid sad, dark, suspenseful, epic or children's music. Vary the genre from day to day (solo piano, acoustic guitar, lo-fi, soft house, light jazz). Add every new video's track to the table above.
