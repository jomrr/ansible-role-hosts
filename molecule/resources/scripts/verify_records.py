"""Verify hosts records and name resolution for the target's IPv6 availability."""

import ipaddress
import json
import socket
import sys
from pathlib import Path


def verify_resolution(
    expected_records: dict[str, list[str]], names: set[str], ipv6_available: bool
) -> None:
    """Check names resolve, or are omitted when they only have unavailable IPv6."""
    for name, addresses in expected_records.items():
        expected = {
            str(address)
            for address in map(ipaddress.ip_address, addresses)
            if ipv6_available or address.version == 4
        }
        if not expected:
            assert name not in names, (name, "IPv6-only hosts record remains")
            continue
        actual = {
            str(ipaddress.ip_address(str(result[4][0])))
            for result in socket.getaddrinfo(
                name, None, socket.AF_UNSPEC, socket.SOCK_STREAM
            )
        }
        assert actual == expected, (name, expected, actual)


def verify_additional_records(
    lines: list[str], expected_records: list[list[str]], ipv6_available: bool
) -> None:
    """Check the optional heading and exact order of additional addresses and names."""
    expected = [
        record
        for record in expected_records
        if ipv6_available or ipaddress.ip_address(record[0]).version == 4
    ]
    heading = "# Additional host records"
    assert lines.count(heading) == bool(expected), (heading, expected, lines)
    if expected:
        actual = [
            record
            for line in lines[lines.index(heading) + 1 :]
            if (record := line.split("#", 1)[0].split())
        ]
        assert actual == expected, ("additional hosts records", expected, actual)


def verify_records(
    absent_names: list[str], expect_ipv6: bool, additional_records: list[list[str]]
) -> set[str]:
    """Check hosts file content independently of other NSS name sources."""
    lines = Path("/etc/hosts").read_text(encoding="utf-8").splitlines()
    verify_additional_records(lines, additional_records, expect_ipv6)
    records = [line.split("#", 1)[0].split() for line in lines]
    names = {name for record in records for name in record[1:]}
    for name in absent_names:
        assert name not in names, (name, "obsolete hosts record remains")
    has_ipv6 = any(":" in record[0] for record in records if record)
    assert has_ipv6 == expect_ipv6, ("IPv6 records", expect_ipv6, has_ipv6)
    assert any(
        record[0] == "127.0.0.1" and "localhost" in record[1:]
        for record in records
        if record
    ), "IPv4 localhost record is missing"
    return names


def main() -> None:
    """Adapt existing record expectations to the unmodified target system."""
    try:
        ipv6_available = bool(
            Path("/proc/net/if_inet6").read_text(encoding="utf-8").strip()
        )
    except FileNotFoundError:
        ipv6_available = False
    names = verify_records(
        json.loads(sys.argv[2]), ipv6_available, json.loads(sys.argv[3])
    )
    verify_resolution(json.loads(sys.argv[1]), names, ipv6_available)


if __name__ == "__main__":
    main()
