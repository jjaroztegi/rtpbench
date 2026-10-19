# rtpbench in CI

```sh
uv run --extra vad rtpbench target sip:agent@staging.example:5060 --out run
uv run rtpbench check run --policy rtpbench.toml --previous baseline/check.json
```

`rtpbench check` judges a finished target run against a policy and exits 1 when the run fails
it (2 when the policy is invalid), without placing calls: change the policy and check the same
run again. It writes `check.md`, the table of what held and what did not, and `check.json`, a
few kilobytes holding what the policy reads (verdicts, and every latency and barge-in turn).

## Policy

```toml
[cases]                       # every case run must pass, except these
hold = "fail"                 # allowed to fail; noted when it passes

[latency.clean]               # turn latency, ms, per profile
p50 = 2000
p95 = 2600

[barge-in.clean.interrupt]    # interrupt, backchannel or cough
stopped = 0.9                 # share of interjections the agent stopped for, at least
p95 = 600                     # stop time, ms

[regression]                  # with --previous: how far the p50 may grow, ms
latency = 50
barge-in = 100
```

Without `--policy`, every case must pass. An unknown name anywhere in the file is an error, so
a typo cannot turn a limit off.

- A case passes the policy only if it passed in every repeat. A case allowed to fail still fails
  the check when `--previous` shows it passing in every repeat there.
- A limit holds unless even the lowest true value the [error bar](calibration.md#error-bars)
  allows is over it: the detector's bias never fails a build. A turn the agent never answered
  counts as later than any limit; a limit on a call that was not run, or did not complete,
  fails. Turns timed across a wall-clock step are left out.
- A regression fails when the change in median from `--previous` is over the tolerance across
  its whole 95% interval (resampling calls, then the turns within them). The error bars are the
  same on both sides and cancel; what the interval holds is how the agent varies from turn to
  turn and call to call. Runs with other caller lines, another rtpbench or another codec are
  not compared, nor is a side with fewer than 10 turns: a barge-in call has about 5
  interruptions and 2 or 3 backchannels and coughs, so comparing them takes `--runs 2` and
  `--runs 4`.

On the baseline, with repeats split into disjoint groups of 1 to 5 calls and nothing changed,
a tolerance of 0 failed about 2% of latency comparisons, as a one-sided 97.5% bound should, and
one of 50 ms none of 1440. Past the tolerance, one clean call against another catches a change
of 10 ms on AI Voice Connector CE and 40 ms on LiveKit, whose turns vary more.

Keep a reviewed `check.json` as the baseline (in the repository, say) and replace it on
purpose. Compared with the last deploy instead, latency can grow by just under the tolerance
every time without failing once.
