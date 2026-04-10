# MAC Address Generator

A simple Python script that generates private (locally-administered, unicast) MAC addresses.

## Features

- Generates random private MAC addresses by default
- Allows specification of the first 1-3 bytes with remaining bytes randomly generated
- Supports bulk generation with count option (up to 10,000 addresses per run)
- Multiple output formats: colon, dash, dot (Cisco-style), or no separator
- Quiet mode (`-q`) for clean piping to other tools
- Ensures MAC addresses are locally-administered and unicast
- Supports both colon-separated and continuous hex input formats

## Usage

```text
python mac-generator.py [prefix] [options]
```

**Arguments:**

- `prefix` - Optional MAC prefix (1-3 bytes, e.g., '02', '02:00', '02:00:1A')

**Options:**

- `-c, --count COUNT` - Number of MAC addresses to generate (default: 1, max: 10,000)
- `-s, --separator FORMAT` - MAC address separator format: `colon`, `dash`, `dot`, or `none` (default: `colon`)
- `-l, --lowercase` - Output MAC address in lowercase (default: uppercase)
- `-q, --quiet` - Suppress header line, output only MAC addresses
- `-h, --help` - Show help message
- `-v, --version` - Show version information

## Examples

```text
# Generate single random MAC
$ python mac-generator.py
Generating 1 random private MAC address:
02:A7:3F:8B:1C:9D

# Generate MAC with prefix (supports both colon-separated and continuous formats)
$ python mac-generator.py 02
Generating 1 private MAC address with prefix 02:
02:7B:4E:9A:3F:1C

$ python mac-generator.py 02:00
Generating 1 private MAC address with prefix 02:00:
02:00:5B:8E:2A:7F

$ python mac-generator.py 02001A
Generating 1 private MAC address with prefix 02001A:
02:00:1A:B7:4C:9E

# Generate multiple MACs
$ python mac-generator.py -c 3
Generating 3 random private MAC addresses:
8A:96:69:80:C5:D3
AA:10:1C:E5:04:60
02:6E:0F:B7:12:12

# Generate multiple MACs with prefix
$ python mac-generator.py 02:00:1A -c 2
Generating 2 private MAC addresses with prefix 02:00:1A:
02:00:1A:1D:AD:62
02:00:1A:7D:3D:04

# Different separator formats
$ python mac-generator.py -s dash
Generating 1 random private MAC address:
02-A7-3F-8B-1C-9D

$ python mac-generator.py -s dot
Generating 1 random private MAC address:
02A7.3F8B.1C9D

$ python mac-generator.py -s none
Generating 1 random private MAC address:
02A73F8B1C9D

# Lowercase output
$ python mac-generator.py -l
Generating 1 random private MAC address:
02:a7:3f:8b:1c:9d

# Quiet mode (no header, useful for piping)
$ python mac-generator.py -q -c 3
8A:96:69:80:C5:D3
AA:10:1C:E5:04:60
02:6E:0F:B7:12:12
```

## MAC Address Format

The first byte of a MAC address contains two important control bits:

- **I/G (Individual/Group) bit** (bit 0): Determines if the address is unicast (0) or multicast/broadcast (1)
- **U/L (Universal/Local) bit** (bit 1): Determines if the address is universally administered by IEEE (0) or locally administered (1)

For private MAC addresses, we want:

- I/G = 0 (unicast)
- U/L = 1 (locally administered)

This combination means the first byte must always end in binary '10'.

**Examples:**

- `9A` (binary `10011010`) is valid - ends in `10`
- `9B` (binary `10011011`) is invalid - ends in `11`
- `9C` (binary `10011100`) is invalid - ends in `00`

## Validation

When providing a prefix, the script validates that:

- The first byte is a valid private MAC byte (ending in binary '10')
- All bytes are valid hexadecimal values
- The prefix length is 1-3 bytes

**Valid first bytes:**

```text
02, 06, 0A, 0E, 12, 16, 1A, 1E, 22, 26, 2A, 2E, 32, 36, 3A, 3E
42, 46, 4A, 4E, 52, 56, 5A, 5E, 62, 66, 6A, 6E, 72, 76, 7A, 7E
82, 86, 8A, 8E, 92, 96, 9A, 9E, A2, A6, AA, AE, B2, B6, BA, BE
C2, C6, CA, CE, D2, D6, DA, DE, E2, E6, EA, EE, F2, F6, FA, FE
```

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

- Input is case-insensitive
- Count option supports 1-10,000 addresses per run for performance and resource management
- Use `-q` for clean output suitable for piping to other tools
- Run `python mac-generator.py --help` for detailed usage information
