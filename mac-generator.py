#!/usr/bin/env python3
"""
MAC Address Generator

Generates private (locally-administered, unicast) MAC addresses.
Can generate completely random addresses or allow specification of the first 1-3 bytes.

MIT License - see LICENSE file for details.
Copyright (c) 2025 Matthew Hatch
"""

__version__ = "1.1.0"

import argparse
import random
import re
import sys
from typing import List, Optional


def is_valid_hex_byte(byte_str: str) -> bool:
    """Check if a string represents a valid hex byte (00-FF)."""
    try:
        int(byte_str, 16)
        return len(byte_str) == 2 and all(c in '0123456789ABCDEFabcdef' for c in byte_str)
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


def generate_private_mac(prefix_bytes: Optional[List[int]] = None) -> str:
    """
    Generate a private MAC address.
    
    Args:
        prefix_bytes: Optional list of bytes to use as prefix (1-3 bytes)
    
    Returns:
        MAC address string in format XX:XX:XX:XX:XX:XX
    """
    if prefix_bytes is None:
        prefix_bytes = []
    
    if len(prefix_bytes) > 3:
        raise ValueError("Prefix cannot be longer than 3 bytes")
    
    # Start with the provided prefix bytes
    mac_bytes = prefix_bytes.copy()
    
    # Generate remaining bytes
    remaining_bytes = 6 - len(prefix_bytes)
    
    for i in range(remaining_bytes):
        if i == 0 and len(prefix_bytes) == 0:
            # First byte: ensure it's unicast (bit 0 = 0) and locally-administered (bit 1 = 1)
            # This means the first byte should end in binary '10' (U/L=1, I/G=0)
            # So the first byte should be in the range 0x02, 0x06, 0x0A, 0x0E, 0x12, 0x16, 0x1A, 0x1E, etc.
            # We can generate any number and then ensure bits 1 and 0 are set correctly
            byte_val = random.randint(0, 255)
            byte_val &= 0xFC  # Clear bits 1 and 0 (mask with 11111100)
            byte_val |= 0x02  # Set bit 1 (locally-administered) and keep bit 0 (unicast)
        else:
            # Other bytes: completely random
            byte_val = random.randint(0, 255)
        
        mac_bytes.append(byte_val)
    
    # Format as MAC address
    return ':'.join(f'{b:02X}' for b in mac_bytes)


def main():
    """Main function to handle command line arguments and generate MAC addresses."""
    parser = argparse.ArgumentParser(
        description="Generate private (locally-administered, unicast) MAC addresses.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mac-generator.py                   # Generate random private MAC
  python mac-generator.py -c 5              # Generate 5 random private MACs
  python mac-generator.py 02                # Generate MAC with prefix '02'
  python mac-generator.py 02:00 -c 3        # Generate 3 MACs with prefix '02:00'
  python mac-generator.py 02001A -c 10      # Generate 10 MACs with prefix '02:00:1A'

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
        
        # Generate the requested number of MAC addresses
        for i in range(args.count):
            mac_address = generate_private_mac(prefix_bytes)
            if args.prefix:
                print(f"Generated MAC with prefix {args.prefix}: {mac_address}")
            else:
                print(f"Generated random private MAC: {mac_address}")
            
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Run 'python mac-generator.py --help' for more information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
