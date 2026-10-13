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

Left out: the `en_GB-vctk-medium` voice (a noise bed about 34 dB under its speech runs through
pauses and past both ends, so its boundaries cannot be labelled from energy) and every phrase
the labeller refused as too noisy.
