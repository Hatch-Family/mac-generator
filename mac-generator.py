#!/usr/bin/env python3
"""
MAC Address Generator

Generates private (locally-administered, unicast) MAC addresses.
Can generate completely random addresses or allow specification of the first 1-3 bytes.

MIT License - see LICENSE file for details.
Copyright (c) 2026 Matthew Hatch
"""

__version__ = "1.2.0"

import argparse
import random
import sys
from typing import List, Optional


def is_valid_hex_byte(byte_str: str) -> bool:
    """Check if a string represents a valid hex byte (00-FF)."""
    if len(byte_str) != 2:
        return False
    try:
        int(byte_str, 16)
        return True
    except ValueError:
        return False


def is_valid_private_mac_byte(byte_val: int) -> bool:
    """Check if a byte value is valid for the first byte of a private MAC address."""
    # For a private MAC, the first byte must end in binary '10' (U/L=1, I/G=0)
    # This means bits 1 and 0 must be 1 and 0 respectively
    return (byte_val & 0x03) == 0x02


def parse_mac_prefix(prefix: str) -> Optional[List[int]]:
    """
    Parse a MAC address prefix string (e.g., "02", "02:00", "02:00:1A").
    Returns a list of integers representing the bytes, or None if invalid.
    """
    if not prefix:
        return None
    
    # Remove any colons and convert to uppercase
    clean_prefix = prefix.replace(':', '').upper()
    
    # Check if the length is valid (must be even and at most 6 characters)
    if len(clean_prefix) % 2 != 0 or len(clean_prefix) > 6:
        return None
    
    # Split into bytes and validate each
    bytes_list = []
    for i in range(0, len(clean_prefix), 2):
        byte_str = clean_prefix[i:i+2]
        if not is_valid_hex_byte(byte_str):
            return None
        byte_val = int(byte_str, 16)
        
        # Validate that the first byte is a valid private MAC byte
        if i == 0 and not is_valid_private_mac_byte(byte_val):
            return None
        
        bytes_list.append(byte_val)
    
    return bytes_list


def format_mac(mac_bytes: List[int], separator: str = 'colon',
               lowercase: bool = False) -> str:
    """
    Format a list of 6 byte values into a MAC address string.

    Args:
        mac_bytes: List of 6 integers (0-255)
        separator: Format style - 'colon', 'dash', 'dot', or 'none'
        lowercase: If True, output hex digits in lowercase

    Returns:
        Formatted MAC address string
    """
    fmt = '{:02x}' if lowercase else '{:02X}'
    hex_bytes = [fmt.format(b) for b in mac_bytes]

    if separator == 'dash':
        return '-'.join(hex_bytes)
    elif separator == 'dot':
        flat = ''.join(hex_bytes)
        return f'{flat[0:4]}.{flat[4:8]}.{flat[8:12]}'
    elif separator == 'none':
        return ''.join(hex_bytes)
    else:
        return ':'.join(hex_bytes)


def generate_private_mac(prefix_bytes: Optional[List[int]] = None,
                         separator: str = 'colon',
                         lowercase: bool = False) -> str:
    """
    Generate a private MAC address.

    Args:
        prefix_bytes: Optional list of bytes to use as prefix (1-3 bytes)
        separator: Format style - 'colon', 'dash', 'dot', or 'none'
        lowercase: If True, output hex digits in lowercase

    Returns:
        Formatted MAC address string
    """
    if prefix_bytes is None:
        prefix_bytes = []

    if len(prefix_bytes) > 3:
        raise ValueError("Prefix cannot be longer than 3 bytes")

    mac_bytes = prefix_bytes.copy()
    remaining_bytes = 6 - len(prefix_bytes)

    for i in range(remaining_bytes):
        if i == 0 and len(prefix_bytes) == 0:
            # First byte: ensure it's unicast (bit 0 = 0) and locally-administered (bit 1 = 1)
            byte_val = random.randint(0, 255)
            byte_val &= 0xFC  # Clear bits 1 and 0 (mask with 11111100)
            byte_val |= 0x02  # Set bit 1 (locally-administered) and keep bit 0 (unicast)
        else:
            byte_val = random.randint(0, 255)

        mac_bytes.append(byte_val)

    return format_mac(mac_bytes, separator, lowercase)


def main():
    """Main function to handle command line arguments and generate MAC addresses."""
    parser = argparse.ArgumentParser(
        description="Generate private (locally-administered, unicast) MAC addresses.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mac-generator.py                       # Generate 1 random private MAC
  python mac-generator.py -c 5                  # Generate 5 random private MACs
  python mac-generator.py 02                    # Generate MAC with prefix '02'
  python mac-generator.py 02:00 -c 3            # Generate 3 MACs with prefix '02:00'
  python mac-generator.py 02001A -c 10          # Generate 10 MACs with prefix '02:00:1A'
  python mac-generator.py -s dash               # Generate MAC with dash separators
  python mac-generator.py -s dot -c 3           # Generate 3 MACs in Cisco dot format
  python mac-generator.py -l                    # Generate MAC in lowercase
  python mac-generator.py -q -c 100             # Generate 100 MACs with no header

Separator formats:
  colon  02:00:1A:B7:4C:9E   (default)
  dash   02-00-1A-B7-4C-9E
  dot    0200.1AB7.4C9E      (Cisco-style)
  none   02001AB74C9E

Note: The first byte must be a valid private MAC byte (ending in binary '10')
Valid first bytes include: 02, 06, 0A, 0E, 12, 16, 1A, 1E, 22, 26, 2A, 2E, etc.
        """
    )

    parser.add_argument(
        'prefix',
        nargs='?',
        help='Optional MAC prefix (1-3 bytes, e.g., "02", "02:00", "02:00:1A")'
    )

    parser.add_argument(
        '-c', '--count',
        type=int,
        default=1,
        help='Number of MAC addresses to generate (default: 1, max: 10,000)'
    )

    parser.add_argument(
        '-s', '--separator',
        choices=['colon', 'dash', 'dot', 'none'],
        default='colon',
        help='MAC address separator format (default: colon)'
    )

    parser.add_argument(
        '-l', '--lowercase',
        action='store_true',
        help='Output MAC address in lowercase (default: uppercase)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress header line, output only MAC addresses'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'MAC Address Generator v{__version__}'
    )

    args = parser.parse_args()

    # Validate count
    if args.count < 1:
        print("Error: Count must be at least 1")
        sys.exit(1)

    if args.count > 10000:
        print("Error: Count cannot exceed 10,000")
        print("For bulk generation beyond this limit, please run the command multiple times.")
        sys.exit(1)

    try:
        prefix_bytes = None
        if args.prefix:
            prefix_bytes = parse_mac_prefix(args.prefix)
            if prefix_bytes is None:
                print(f"Error: Invalid MAC prefix '{args.prefix}'")
                print()
                print("Prefix should be 1-3 hex bytes (e.g., '02', '02:00', '02:00:1A')")
                print()
                print("Note: The first byte must be a valid private MAC byte (ending in binary '10')")
                print("Valid first bytes include: 02, 06, 0A, 0E, 12, 16, 1A, 1E, 22, 26, 2A, 2E, etc.")
                print()
                print("Run 'python mac-generator.py --help' for more information.")
                sys.exit(1)

        if not args.quiet:
            addr_word = "address" if args.count == 1 else "addresses"
            if args.prefix:
                print(f"Generating {args.count} private MAC {addr_word} with prefix {args.prefix}:")
            else:
                print(f"Generating {args.count} random private MAC {addr_word}:")

        for _ in range(args.count):
            print(generate_private_mac(prefix_bytes, args.separator, args.lowercase))

    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Run 'python mac-generator.py --help' for more information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
