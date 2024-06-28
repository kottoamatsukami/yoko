def encode(address: tuple[str, int]) -> str:
    return f"{address[0]}:{address[1]}"


def decode(token: str) -> tuple[str, int]:
    addr, port = token.split(":")
    return addr, int(port)


__all__ = [
    "encode",
    "decode",
]