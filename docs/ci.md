# rtpbench in CI

```sh
uv run --extra vad rtpbench target sip:agent@staging.example:5060 --out run
uv run rtpbench check run --policy rtpbench.toml --previous baseline/check.json
```

`rtpbench check` judges a finished target run against a policy and exits 1 when the run fails
it (2 when the policy, the run or the previous `check.json` cannot be read), without placing
calls: change the policy and check the same
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
  not compared, nor is a side with fewer than 10 turns (for barge-in, interjections the agent
  stopped for). A barge-in call has 10 interjections,
  drawn as about half interruptions and a quarter each backchannels and coughs, so comparing
  interruptions takes `--runs 2` or more, the others about 5; `check.md` says when a side has
  too few.

A tolerance of 0 fails about 1 in 40 runs of an unchanged agent: the interval's lower end is
over 0 that often by chance. Give each regression a tolerance.

Keep a reviewed `check.json` as the baseline (in the repository, say) and replace it on
purpose. Compared with the last deploy instead, latency can grow by just under the tolerance
every time without failing once.
