"""Check that the course's required Python version is available."""

import sys


MINIMUM_VERSION = (3, 12)


def main() -> None:
    """Print the installed version and report whether setup succeeded."""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version < MINIMUM_VERSION:
        required = ".".join(map(str, MINIMUM_VERSION))
        raise SystemExit(f"Python {required} or newer is required.")

    print("Setup successful! You are ready for class.")


if __name__ == "__main__":
    main()
