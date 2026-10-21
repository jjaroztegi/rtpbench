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
  counts as later than any limit, and a limit on a call that did not complete fails. A limit on
  a call the run did not request (left out of `--only`, or a profile not run) is noted and not
  judged, so one policy serves split runs, such as cases nightly and latency on each deploy.
  Turns timed across a [wall-clock step](calibration.md#clock-steps-and-rate) are left out.
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

## GitHub Actions

```yaml
jobs:
  voice-agent:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    services:
      agent:
        image: registry.example/agent:${{ github.sha }}
    steps:
      - uses: actions/checkout@v6  # the policy and the baseline
      - uses: jjaroztegi/rtpbench@<commit SHA>  # vX.Y.Z
        env:
          RTPBENCH_SIP_USER: ${{ secrets.SIP_USER }}
          RTPBENCH_SIP_PASSWORD: ${{ secrets.SIP_PASSWORD }}
        with:
          target: sip:agent@agent:5060
          network: ${{ job.services.agent.network }}
          profiles: clean,lte
          policy: rtpbench.toml
          previous: rtpbench-baseline.json
```

The [action](../action.yml) runs `rtpbench target` and `rtpbench check` with its inputs, adds
`summary.md` and `check.md` to the job summary, uploads the report files (`summary.md`,
`report.html`, `results.json`, `conditions.json`, `check.*`) as an artifact, and fails the job
when the run fails the policy; its outputs are `results` (the directory) and `passed`. A job
takes as long as `rtpbench target`: this repository's [Action
workflow](../.github/workflows/action.yml), six calls on one profile, takes about 8 minutes on
`ubuntu-24.04`, building images included. Credentials go in the step's `env`, from secrets.
`upload: all` uploads the whole results directory, captures included; in a public repository
anyone can download it, and the captures of a run with credentials hold the SIP user name and
a digest of the password that a dictionary attack can test.

### Where the agent runs

- In the same job: a service container, as above, or `docker compose up -d` in an earlier step
  with `network` its network's name. Nothing crosses a NAT and nothing listens on the internet.
- Over the internet, from a GitHub-hosted runner: the runner takes no inbound traffic, so
  `advertise` cannot work, and only an agent that sends its audio and requests back to where
  ours come from (symmetric RTP and `rport`, as SBCs facing the internet do) can be called. The
  profile adds to a real path that the error bars do not cover and that changes between runs:
  give regressions a wider tolerance. Not yet tested.
- On a self-hosted runner (Linux, Docker 28 or later) beside the agent: a private network, or an
  agent that sends its audio to the offered address, with `advertise` and its ports forwarded
  to the runner. A dedicated host also times more steadily than a shared runner.

### Versioning

Pin the action by commit SHA, with the version in a comment (Dependabot and Renovate update
both). The action runs the rtpbench of that commit, so its checks and error bars change only
when the pin does; a baseline from another version is not compared, so replace it with the
upgrade. There is no moving major tag, which would change the judging under a build.
