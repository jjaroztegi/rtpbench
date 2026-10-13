# Speech corpus

8 kHz mono 16-bit clips for the speech calibrations. Each is the clean source: labels come
from `rtpbench.speech.label` on these files, nothing is stored alongside them.

| prefix | what | source | licence |
|---|---|---|---|
| `tts-davefx-` | Spanish (Spain), male | Piper voice `es_ES-davefx-medium`, dataset davefx | CC0 |
| `tts-sharvardm-`, `tts-sharvardf-` | Spanish (Spain), male / female | Piper `es_ES-sharvard-medium`, Sharvard corpus (Aubanel, García Lecumberri, Cooke, 2014) | CC BY 3.0 |
| `tts-ald-` | Spanish (Mexico), male | Piper `es_MX-ald-medium`, Ald dataset | Unlicense |
| `tts-ljspeech-` | English (US), female | Piper `en_US-ljspeech-high`, LJ Speech | public domain |
| `tts-cori-` | English (UK), female | Piper `en_GB-cori-high`, LibriVox recordings | public domain |
| `tts-libritts0-`, `tts-libritts3-` | English (US), speakers 0 and 3 | Piper `en_US-libritts_r-medium`, LibriTTS-R (Koizumi et al., 2023) | CC BY 4.0 |
| `human-es-f012-`, `human-es-f016-` | Spanish read speech, two readers | LibriVox, *Las Fábulas de Esopo, vol. 01*, fables 012 and 016 | public domain |
| `human-en-dr-`, `human-en-sc-` | English read speech, two readers | LibriVox, *Short Story Collection 006*: *After Twenty Years*, *A Child's Dream of a Star* | public domain |
| `cough-` | single coughs | Wikimedia Commons: Cough 1.ogg, Cough 2.ogg, Man coughing.ogg, Short coughs.ogg (public domain), Woman coughing three times.wav (CC0) | as listed |

TTS clips: `-sNN` a short reply, `-long` three sentences (barge-in), `-bc` a backchannel
("Ajá", "Sí, sí", "Vale", "Uh-huh", "Yeah", "Okay"). Generated with piper-tts 1.8.0 at default
settings and 0.3 s between sentences.

Processing: resampled to 8 kHz (polyphase, scipy `resample_poly`), scaled to an active speech
level of -24.5 dBFS (power mean of the 20 ms frames within 30 dB of the loudest, the level a
real agent was measured sending), TTS clips padded with 250 ms of digital silence on each side.
Human phrases are cut at pauses of at least 250 ms, keeping up to 250 ms of the pause on each
side (room tone, breath) with 5 ms fades at the cut. Coughs are single events with 150 ms
margins and the same padding as TTS.

## Caller lines (`lines/en/`)

What the caller says to a real agent (`rtpbench target`), same processing as the TTS clips:
Piper `en_US-ljspeech-high` (public domain) except the interruptions, `en_GB-cori-high` (public
domain).

- `turn-00`..`11`, one turn-latency call: "Hello, good morning." / "I'd like to check the
  status of an order." / "The order number is one, zero, zero, two." / "Yes, that's right." /
  "And when will it arrive, roughly?" / "What if I'm not at home that day?" / "All right." /
  "One more thing: can I change the delivery address?" / "Ten Main Street, second floor." / "Is
  there a charge for the change?" / "Understood. Can you send me a confirmation by email?" /
  "Perfect, that's all. Thank you very much."
- `prompt-00`..`09`, questions with long answers for barge-in: "Hello, can you explain how
  returns work?" / "What options do I have to pay for an order?" / "Tell me what happens if a
  parcel arrives damaged." / "How can I change the details of my account?" / "What is the
  difference between standard and express delivery?" / "Explain how the product warranty
  works." / "What do I have to do to cancel the service?" / "How are the delivery costs
  calculated?" / "What are the opening hours of customer service?" / "Can you explain how to use
  the mobile app?"; `prompt` is `prompt-00`, the cases' question.
- `interrupt-00`..`03`: "Sorry, a quick question." / "Wait, wait a moment." / "Sorry, I didn't
  understand that." / "Right, but what I need is something else."
- `transfer`: "I'd like to speak to a person, please. Put me through to an agent."

Left out: the `en_GB-vctk-medium` voice (a noise bed about 34 dB under its speech runs through
pauses and past both ends, so its boundaries cannot be labelled from energy) and every phrase
the labeller refused as too noisy.
