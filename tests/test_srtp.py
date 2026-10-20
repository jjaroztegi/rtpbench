import pytest

from rtpbench import rtp, srtp


def test_rfc3711_key_derivation() -> None:
    """RFC 3711 B.3."""
    master = bytes.fromhex("E1F97A0D3E018BE0D64FA32C06DE41390EC675AD498AFEEBB6960B3AABE6")
    ctx = srtp.Context("AES_CM_128_HMAC_SHA1_80", master)
    assert ctx.key.hex().upper() == "C61E7A93744F39EE10734AFE3FF7A087"
    assert ctx.salt.hex().upper() == "30CBBC08863D8C85D49DB34A9AE1"
    assert ctx.auth.hex().upper() == "CEBE321F6FF7716B6FD4AB49AF256A156D38BAA4"


def test_rfc3711_keystream() -> None:
    """RFC 3711 B.2: AES-CM keystream at ROC 0, seq 0, SSRC 0."""
    ctx = srtp.Context("AES_CM_128_HMAC_SHA1_80", bytes(30))
    ctx.key = bytes.fromhex("2B7E151628AED2A6ABF7158809CF4F3C")
    ctx.salt = bytes.fromhex("F0F1F2F3F4F5F6F7F8F9FAFBFCFD")
    assert ctx._ctr(0, 0, bytes(48)).hex().upper() == (
        "E03EAD0935C95E80E166B16DD92B4EB4D23513162B02D0F72A43A2FE4A5F97AB"
        "41E95B3BB0A2E8DD477901E4FCA894C0"
    )


def test_rfc7714_aes_gcm() -> None:
    """RFC 7714 16.1.1 and 16.1.2."""
    packet = bytes.fromhex(
        "8040f17b8041f8d35501a0b2" + b"Gallia est omnis divisa in partes tres".hex()
    )
    sealed = bytes.fromhex(
        "8040f17b8041f8d35501a0b2f24de3a3fb34de6cacba861c9d7e4bcabe633bd50d294e6f42a5f47a"
        "51c7d19b36de3adf8833899d7f27beb16a9152cf765ee4390cce"
    )
    ctx = srtp.Context("AEAD_AES_128_GCM", bytes(28))
    ctx.key, ctx.salt = bytes(range(16)), b"Quid pro quo"
    assert ctx.protect(packet, 0xF17B) == sealed
    assert ctx.open(sealed) == packet
    assert ctx.open(sealed[:-1] + b"\0") is None


@pytest.mark.parametrize("suite", list(srtp.SUITES))
def test_round_trip_across_a_seq_wrap_with_loss_and_reorder(suite: str) -> None:
    key = srtp.master()[suite]
    sender, receiver = srtp.Context(suite, key), srtp.Context(suite, key)
    seq0 = 65530
    sent = [
        sender.protect(rtp.pack(0, (seq0 + i) & 0xFFFF, 160 * i, 7, bytes([i]) * 160), seq0 + i)
        for i in range(20)
    ]
    order = [0, 1, 2, 3, 5, 4, 6, 9, 10, 8, 12, 19]  # lost: 7, 11, 13-18; 4 and 8 late
    got = [receiver.open(sent[i]) for i in order]
    assert [p and rtp.parse(p).payload[0] for p in got] == order  # type: ignore[union-attr]
    assert receiver.state[7] == (1, (seq0 + 19) & 0xFFFF)
    assert receiver.open(sent[3][:-1] + bytes([sent[3][-1] ^ 1])) is None
    assert srtp.Context(suite, srtp.master()[suite]).open(sent[19]) is None  # another key


def test_crypto_attribute() -> None:
    key = bytes(range(30))
    assert srtp.parse(srtp.line(3, "AES_CM_128_HMAC_SHA1_80", key)) == (
        3,
        "AES_CM_128_HMAC_SHA1_80",
        key,
    )
    lifetime = srtp.line(1, "AES_CM_128_HMAC_SHA1_32", key) + "|2^31"
    assert srtp.parse(lifetime)[2] == key
    for bad in (lifetime + "|1:4", srtp.line(1, "F8_128_HMAC_SHA1_80", key), "1 X inline:AA KDR=1"):
        with pytest.raises(ValueError, match="not supported"):
            srtp.parse(bad)


def test_a_new_key_keeps_the_rollover_counter() -> None:
    """Past a seq wrap, the peer's new key (a re-INVITE) still opens its packets, live and in
    a keyring, which judging uses."""
    suite = "AES_CM_128_HMAC_SHA1_80"
    old, new = srtp.master()[suite], srtp.master()[suite]
    seq0 = 65534

    def sent(key: bytes, i: int) -> bytes:
        packet = rtp.pack(0, (seq0 + i) & 0xFFFF, 160 * i, 7, b"x" * 160)
        return srtp.Context(suite, key).protect(packet, seq0 + i)

    rx = srtp.Context(suite, old)
    assert all(rx.open(sent(old, i)) for i in range(4))  # crosses the wrap: ROC 1
    rekeyed = srtp.Context(suite, new, rx.state)
    assert rekeyed.open(sent(new, 4)) is not None
    ring = srtp.Keyring([(suite, old), (suite, new)])
    assert all(ring.open(sent(old, i)) for i in range(4))
    assert ring.open(sent(new, 4)) is not None
    assert ring.failed == 0
