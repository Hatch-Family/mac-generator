# MAC Address Generator

A simple Python script that generates private (locally-administered, unicast) MAC addresses.

## Features

- Generates random private MAC addresses by default
- Allows specification of the first 1-3 bytes with remaining bytes randomly generated
- Ensures MAC addresses are locally-administered and unicast
- Supports both colon-separated and continuous hex input formats

## Usage

### Command Line Options

```text
python mac_generator.py [prefix] [options]
```

**Arguments:**

- `prefix` - Optional MAC prefix (1-3 bytes, e.g., '02', '02:00', '02:00:1A')

**Options:**

- `-h, --help` - Show help message
- `-v, --version` - Show version information

### Generate a random private MAC address

```text
python mac_generator.py

or

./mac_generator.py
```

### Generate MAC address with specific first byte

```text
python mac_generator.py 02
```

### Generate MAC address with specific first two bytes

```text
python mac_generator.py 02:00

or

python mac_generator.py 0200
```

### Generate MAC address with specific first three bytes

```text
python mac_generator.py 02:00:1A

or

python mac_generator.py 02001A
```

## Examples

```text
$ python mac_generator.py
Generated random private MAC: 02:A7:3F:8B:1C:9D

$ python mac_generator.py 02
Generated MAC with prefix 02: 02:7B:4E:9A:3F:1C

$ python mac_generator.py 02:00
Generated MAC with prefix 02:00: 02:00:5B:8E:2A:7F

$ python mac_generator.py 02001A
Generated MAC with prefix 02001A: 02:00:1A:B7:4C:9E
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

- The script accepts both colon-separated (02:00:1A) and continuous (02001A) input formats
- Input is case-insensitive
- Invalid prefixes will result in an error message with usage instructions
- Run `python mac_generator.py --help` for detailed usage information
