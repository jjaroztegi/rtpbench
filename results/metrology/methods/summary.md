Turn latency, measured - truth, ms: p50 [p5, p95] over every turn (turns measured / turns where some were missed). Truth: from the caller's last labelled sample to the agent's first, as they crossed the caller's wire. A recording is two channels at the caller, the agent's placed by a jitter buffer, unless said; both edges detected.

| method | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| truth itself | +1877 [+1455, +2345] | +1885 [+1458, +2349] | +1958 [+1535, +2428] | +1965 [+1531, +2427] | +1957 [+1545, +2423] | +1961 [+1520, +2458] |
| rtpbench: wire, labelled end, webrtcvad onset | +9 [-2, +38] | +0 [-139, +13] | +7 [-4, +40] | -1 [-143, +15] | +1 [-16, +64] | -2 [-172, +31] |
| the agent's capture, labelled: an agent-side log | -0 [-0, -0] | -0 [-0, -0] | -80 [-87, -75] | -80 [-88, -73] | -88 [-156, -29] | -92 [-157, -40] |
| recording, rms at both edges | +88 [+34, +256] | +88 [+34, +257] | +87 [+33, +258] | +89 [+35, +261] | +110 [+24, +274] | +103 [+11, +267] |
| recording, webrtcvad at both edges | -9 [-63, +158] | -53 [-191, +117] | -11 [-64, +154] | -51 [-188, +113] | +6 [-80, +158] | -36 [-182, +104] |
| recording, silero at both edges | +20 [-65, +225] (207/215) | +30 [-54, +265] (207/215) | +19 [-64, +243] (207/215) | +37 [-53, +266] (207/215) | +34 [-58, +232] (207/215) | +37 [-92, +311] (206/215) |
| recording, silero16 at both edges | -20 [-66, +119] | -17 [-68, +135] | -19 [-70, +119] | -20 [-72, +142] | +2 [-79, +153] | -1 [-94, +170] |
| recording appending payloads as they arrive, webrtcvad | -9 [-63, +158] | -53 [-191, +117] | -991 [-2067, +7007] (176/215) | -968 [-2121, +6461] (165/215) | +1265 [-1805, +7018] (181/215) | +1350 [-1513, +6944] (181/215) |

Where a recording's error comes from: detected - labelled, ms, p50 [p5, p95]. A recording's error is about the agent's onset error - the caller's end error.

| edge | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| rms: caller's end | -65 [-240, -22] | -65 [-240, -22] | -65 [-240, -22] | -65 [-240, -22] | -65 [-240, -22] | -65 [-240, -22] |
| rms: agent's onset | +13 [+1, +59] | +13 [+1, +59] | +13 [-2, +60] | +13 [-0, +67] | +7 [-7, +89] | +6 [-11, +88] |
| webrtcvad: caller's end | +24 [-141, +69] | +42 [-121, +99] | +24 [-141, +69] | +42 [-121, +99] | +24 [-141, +69] | +42 [-121, +99] |
| webrtcvad: agent's onset | +9 [-2, +38] | +0 [-139, +13] | +7 [-4, +40] | -1 [-143, +15] | +1 [-16, +64] | -2 [-172, +31] |
| silero: caller's end | +64 [-11, +102] (210/215) | +68 [-36, +105] (210/215) | +64 [-11, +101] (210/215) | +68 [-36, +105] (210/215) | +64 [-11, +101] (210/215) | +68 [-36, +105] (210/215) |
| silero: agent's onset | +76 [+12, +264] (210/215) | +85 [+19, +304] (210/215) | +75 [+19, +272] (210/215) | +88 [+16, +302] (210/215) | +80 [+4, +256] (210/215) | +96 [+1, +321] (209/215) |
| silero16: caller's end | +48 [-79, +85] | +53 [-86, +94] | +48 [-79, +85] | +53 [-86, +94] | +48 [-80, +85] | +53 [-86, +94] |
| silero16: agent's onset | +25 [+0, +123] | +26 [+3, +151] | +23 [+1, +132] | +28 [+0, +150] | +18 [-6, +137] | +29 [-9, +184] |

Per call, the mean of the recording's gaps of at least 500 ms (Coval's Latency) - the mean of the call's true latencies, ms: median [min, max] over calls (gaps counted / turns)

| detector | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| rms | +107 [+107, +107] (215/215) | +107 [+107, +108] (215/215) | +107 [+103, +110] (215/215) | +108 [+106, +109] (215/215) | +132 [+80, +146] (215/215) | +120 [+67, +143] (215/215) |
| webrtcvad | +5 [+0, +9] (215/215) | -53 [-55, -49] (215/215) | +7 [-3, +7] (215/215) | -52 [-56, -50] (215/215) | +29 [-28, +41] (215/215) | -40 [-93, -18] (215/215) |
| silero | +66 [+31, +274] (207/215) | +68 [+45, +290] (207/215) | +56 [+40, +280] (207/215) | +75 [+59, +293] (207/215) | +80 [+22, +306] (207/215) | +85 [+34, +321] (206/215) |
| silero16 | -3 [-7, +1] (215/215) | +2 [-4, +9] (215/215) | -4 [-11, +2] (215/215) | +1 [-2, +7] (215/215) | +31 [-24, +40] (215/215) | +27 [-36, +41] (215/215) |

