#!/usr/bin/env python3
# ==============================================
#   GVDILIX WORDLIST FORGE - PERSONAL EDITION
#   Professional Wordlist Generator (EXACT COUNT)
# ==============================================

import os
import random
import string
import time
import glob
from datetime import datetime


# ==========[ UI BANNER ]==========
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
╔══════════════════════════════════════════════════════════╗
║        🔥 G V D I L I X   W O R D F O R G E 🔥          ║
║                PERSONAL EDITION  v8.0                   ║
║        Exact Count Wordlist Generator + Viewer          ║
╚══════════════════════════════════════════════════════════╝
""")


# ==========[ VIEW WORDLISTS ]==========
def view_wordlists():
    banner()
    print("📁 WORDLIST VIEWER\n")

    folder = "GVDILIX_OUTPUT"

    # Check if folder exists
    if not os.path.exists(folder):
        print(f"[!] Folder '{folder}' doesn't exist yet.")
        print(f"[!] Generate some wordlists first!")
        input("\nPress Enter to continue...")
        return

    # Get all text files in the folder
    files = glob.glob(f"{folder}/*.txt")

    if not files:
        print(f"[!] No wordlist files found in '{folder}'.")
        print(f"[!] Generate some wordlists first!")
        input("\nPress Enter to continue...")
        return

    print(f"Found {len(files)} wordlist(s):\n")

    # Display files with numbers
    for i, filepath in enumerate(sorted(files, key=os.path.getmtime, reverse=True), 1):
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        line_count = 0

        # Count lines quickly
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
        except:
            line_count = "Unknown"

        modified = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(filepath)))

        print(f"  {i:2}. {filename}")
        print(f"      Size: {size:,} bytes | Lines: {line_count:,}")
        print(f"      Modified: {modified}")
        print()

    # Let user choose a file
    while True:
        try:
            choice = input(f"\nEnter file number to view (1-{len(files)}) or 'b' to go back: ").strip().lower()

            if choice == 'b':
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(files):
                selected_file = sorted(files, key=os.path.getmtime, reverse=True)[choice_num - 1]
                view_file_contents(selected_file)
                break
            else:
                print(f"[!] Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("[!] Please enter a valid number or 'b' to go back")


def view_file_contents(filepath):
    """Display contents of a wordlist file"""
    banner()
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)

    print(f"📄 VIEWING: {filename}\n")
    print(f"File: {filepath}")
    print(f"Size: {size:,} bytes")

    # Count lines
    line_count = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_count, _ in enumerate(f, 1):
                pass
    except:
        line_count = "Unknown"

    print(f"Lines: {line_count:,}")
    print("-" * 50)

    # Ask how many lines to display
    print("\nHow many lines would you like to see?")
    print("  1) First 10 lines")
    print("  2) First 50 lines")
    print("  3) First 100 lines")
    print("  4) First 500 lines")
    print("  5) View all lines (may be slow for large files)")
    print("  6) Random sample of 20 lines")
    print("  7) Go back")

    view_choice = input("\nChoose option (1-7): ").strip()

    if view_choice == '7':
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = []

            if view_choice == '1':
                lines = [f.readline().strip() for _ in range(10) if f.readline()]
                print(f"\nFirst 10 lines of {filename}:\n")
            elif view_choice == '2':
                lines = [f.readline().strip() for _ in range(50) if f.readline()]
                print(f"\nFirst 50 lines of {filename}:\n")
            elif view_choice == '3':
                lines = [f.readline().strip() for _ in range(100) if f.readline()]
                print(f"\nFirst 100 lines of {filename}:\n")
            elif view_choice == '4':
                lines = [f.readline().strip() for _ in range(500) if f.readline()]
                print(f"\nFirst 500 lines of {filename}:\n")
            elif view_choice == '5':
                print(f"\nALL lines of {filename} (this may take a moment):\n")
                lines = [line.strip() for line in f]
            elif view_choice == '6':
                # Read all lines first for random sampling
                all_lines = [line.strip() for line in f]
                if len(all_lines) > 20:
                    lines = random.sample(all_lines, 20)
                    print(f"\nRandom 20 lines from {filename}:\n")
                else:
                    lines = all_lines
                    print(f"\nAll {len(lines)} lines from {filename}:\n")
            else:
                print("[!] Invalid choice. Showing first 10 lines.")
                f.seek(0)
                lines = [f.readline().strip() for _ in range(10) if f.readline()]
                print(f"\nFirst 10 lines of {filename}:\n")

            # Display lines
            for i, line in enumerate(lines, 1):
                print(f"{i:6}. {line}")

            if view_choice != '5' and view_choice != '6' and len(lines) < line_count:
                print(f"\n... and {line_count - len(lines):,} more lines!")

    except Exception as e:
        print(f"[!] Error reading file: {e}")

    print("\n" + "=" * 50)

    # File operations menu
    print("\n📋 FILE OPERATIONS:")
    print("  1) View more lines")
    print("  2) Copy file path to clipboard (if supported)")
    print("  3) Delete this file")
    print("  4) Back to file list")
    print("  5) Main menu")

    op_choice = input("\nChoose option (1-5): ").strip()

    if op_choice == '1':
        view_file_contents(filepath)
    elif op_choice == '2':
        try:
            # Try to copy to clipboard
            import pyperclip
            pyperclip.copy(filepath)
            print(f"[✓] File path copied to clipboard: {filepath}")
        except:
            print(f"[!] Cannot copy to clipboard. Manual path: {filepath}")
        input("\nPress Enter to continue...")
        view_file_contents(filepath)
    elif op_choice == '3':
        confirm = input(f"\n⚠️  DELETE '{filename}'? This cannot be undone! (y/N): ").strip().lower()
        if confirm == 'y':
            try:
                os.remove(filepath)
                print(f"[✓] File '{filename}' deleted successfully!")
            except Exception as e:
                print(f"[!] Error deleting file: {e}")
            input("\nPress Enter to continue...")
            view_wordlists()
        else:
            view_file_contents(filepath)
    elif op_choice == '4':
        view_wordlists()
    elif op_choice == '5':
        return


# ==========[ L33T TRANSFORMATIONS ]==========
def get_leet_variations(word):
    variations = []
    if not word:
        return variations

    # Basic leet substitutions
    leet_map = {
        'a': ['@', '4'],
        'e': ['3', '€'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'l': ['1'],
        'g': ['9'],
        'b': ['8'],
        'z': ['2']
    }

    # Add original word
    variations.append(word)
    variations.append(word.lower())
    variations.append(word.upper())
    variations.append(word.capitalize())

    # Generate leet variations
    for i in range(min(3, len(word))):  # Generate 3 leet variations max
        leet_word = list(word.lower())
        # Replace 1-3 characters with leet
        for _ in range(random.randint(1, 3)):
            idx = random.randint(0, len(leet_word) - 1)
            char = leet_word[idx]
            if char in leet_map:
                leet_word[idx] = random.choice(leet_map[char])
        variations.append(''.join(leet_word))

    return variations


# ==========[ PASSWORD GENERATOR ]==========
class PasswordGenerator:
    def __init__(self, user_data):
        self.data = user_data
        self.all_words = []
        self.symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=']
        self.numbers = ['123', '1234', '12345', '123456', '111', '222', '333', '444', '555',
                        '666', '777', '888', '999', '000', '1111', '2222', '3333', '2020',
                        '2021', '2022', '2023', '2024', '2025']

    def extract_words(self):
        """Extract all possible words from user data"""
        words_set = set()

        # Personal information
        fields = ['name', 'surname', 'nick', 'city', 'country']
        for field in fields:
            value = self.data.get(field, '').strip()
            if value:
                words_set.add(value.lower())
                words_set.add(value.capitalize())

        # Favorite teams and sports
        favorite_fields = ['team', 'player', 'sport']
        for field in favorite_fields:
            value = self.data.get(field, '').strip()
            if value:
                # Split by comma for multiple entries
                items = value.split(',')
                for item in items:
                    item = item.strip()
                    if item:
                        words_set.add(item.lower())
                        words_set.add(item.capitalize())

        # Family and important people
        family_fields = ['spouse', 'child', 'pet', 'mother', 'father']
        for field in family_fields:
            value = self.data.get(field, '').strip()
            if value:
                words_set.add(value.lower())
                words_set.add(value.capitalize())

        # Important dates (birth, anniversary, etc.)
        date_fields = ['birth', 'anniversary']
        for field in date_fields:
            value = self.data.get(field, '').strip()
            if value:
                # Clean date to get only digits
                date_digits = ''.join(filter(str.isdigit, value))
                if date_digits:
                    if len(date_digits) >= 4:
                        words_set.add(date_digits[-4:])  # Full year
                        words_set.add(date_digits[-2:])  # Last 2 digits
                    if len(date_digits) == 8:  # Full date DDMMYYYY
                        words_set.add(date_digits[:4])  # DDMM
                        words_set.add(date_digits[4:])  # YYYY

        # Contact information
        contact_fields = ['phone', 'email_local']
        for field in contact_fields:
            value = self.data.get(field, '').strip()
            if value:
                # For phone numbers, extract digits
                if field == 'phone':
                    phone_digits = ''.join(filter(str.isdigit, value))
                    if phone_digits:
                        words_set.add(phone_digits[-4:])  # Last 4 digits
                        if len(phone_digits) >= 6:
                            words_set.add(phone_digits[-6:])  # Last 6 digits
                        if len(phone_digits) >= 10:
                            words_set.add(phone_digits[-10:])  # Last 10 digits
                else:
                    words_set.add(value.lower())

        # Hobbies and interests
        hobbies = self.data.get('hobby', '').strip()
        if hobbies:
            for item in hobbies.split(','):
                item = item.strip()
                if item:
                    words_set.add(item.lower())
                    words_set.add(item.capitalize())

        # Job and education
        job_fields = ['job', 'company', 'school', 'university']
        for field in job_fields:
            value = self.data.get(field, '').strip()
            if value:
                words_set.add(value.lower())
                words_set.add(value.capitalize())

        # Car and bike models
        vehicle_fields = ['car', 'bike']
        for field in vehicle_fields:
            value = self.data.get(field, '').strip()
            if value:
                words_set.add(value.lower())
                words_set.add(value.capitalize())

        # Favorite things
        favorites = self.data.get('favorite', '').strip()
        if favorites:
            for item in favorites.split(','):
                item = item.strip()
                if item:
                    words_set.add(item.lower())
                    words_set.add(item.capitalize())

        return list(words_set)

    def generate_base_combinations(self, words):
        """Generate base password combinations"""
        combinations = set()

        print("[+] Generating base combinations...")

        # Single words with numbers
        for word in words:
            # Word + common numbers
            for num in self.numbers[:10]:  # Use first 10 numbers
                combinations.add(f"{word}{num}")
                combinations.add(f"{num}{word}")

            # Word + birth year if available
            birth = self.data.get('birth', '').strip()
            if birth:
                birth_digits = ''.join(filter(str.isdigit, birth))
                if birth_digits and len(birth_digits) >= 2:
                    year2 = birth_digits[-2:]
                    year4 = birth_digits[-4:] if len(birth_digits) >= 4 else year2
                    combinations.add(f"{word}{year2}")
                    combinations.add(f"{word}{year4}")
                    combinations.add(f"{year2}{word}")
                    combinations.add(f"{year4}{word}")

            # Word + phone last 4 if available
            phone = self.data.get('phone', '').strip()
            if phone:
                phone_digits = ''.join(filter(str.isdigit, phone))
                if phone_digits and len(phone_digits) >= 4:
                    last4 = phone_digits[-4:]
                    combinations.add(f"{word}{last4}")
                    combinations.add(f"{last4}{word}")

            # Word with symbols
            for symbol in self.symbols[:5]:  # Use first 5 symbols
                combinations.add(f"{word}{symbol}")
                combinations.add(f"{symbol}{word}")

        # Word + word combinations
        if len(words) >= 2:
            for i in range(min(20, len(words))):  # Limit to 20 words to avoid explosion
                for j in range(min(20, len(words))):
                    if i != j:
                        word1 = words[i]
                        word2 = words[j]
                        # Direct combination
                        combinations.add(f"{word1}{word2}")
                        combinations.add(f"{word2}{word1}")
                        # With separator
                        for sep in ['', '_', '-', '.', '@']:
                            combinations.add(f"{word1}{sep}{word2}")
                            combinations.add(f"{word2}{sep}{word1}")

        # Special combinations for sports teams with jersey numbers
        team = self.data.get('team', '').strip()
        if team:
            team_lower = team.lower()
            # Common jersey numbers
            jersey_numbers = ['1', '7', '8', '9', '10', '11', '17', '23', '24', '99']
            for num in jersey_numbers:
                combinations.add(f"{team_lower}{num}")
                combinations.add(f"{team}{num}")
                combinations.add(f"{team_lower}{num}!")
                combinations.add(f"{team}{num}!")

        return list(combinations)

    def expand_with_variations(self, base_passwords, target_count):
        """Expand base passwords with variations to reach target count"""
        all_passwords = set(base_passwords)

        print(f"[+] Starting with {len(all_passwords)} base passwords")
        print(f"[+] Expanding to reach {target_count}...")

        # If we already have enough, return
        if len(all_passwords) >= target_count:
            return list(all_passwords)[:target_count]

        # Stage 1: Add leet variations
        stage1_count = len(all_passwords)
        if stage1_count < target_count:
            print("[+] Stage 1: Adding leet variations...")
            base_list = list(all_passwords)
            for password in base_list:
                if len(all_passwords) >= target_count * 2:  # Generate extra for selection
                    break
                # Simple leet transformation
                leet_pass = password
                replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
                for old, new in replacements.items():
                    if random.random() > 0.7:  # 30% chance to replace each character
                        leet_pass = leet_pass.replace(old, new).replace(old.upper(), new)
                if leet_pass != password:
                    all_passwords.add(leet_pass)

        # Stage 2: Add symbol variations
        stage2_count = len(all_passwords)
        if stage2_count < target_count * 2:
            print("[+] Stage 2: Adding symbol variations...")
            base_list = list(all_passwords)
            for password in base_list:
                if len(all_passwords) >= target_count * 3:  # Generate extra
                    break
                # Add symbols at beginning/end
                for symbol in self.symbols[:3]:
                    all_passwords.add(f"{symbol}{password}")
                    all_passwords.add(f"{password}{symbol}")
                    all_passwords.add(f"{symbol}{password}{symbol}")

        # Stage 3: Random mutations (guaranteed to reach target)
        print("[+] Stage 3: Random mutations (guaranteed)...")
        attempts = 0
        max_attempts = target_count * 10  # Safety limit

        while len(all_passwords) < target_count and attempts < max_attempts:
            attempts += 1

            # Create new password from scratch if needed
            if random.random() < 0.3 or len(all_passwords) < 100:
                # Create completely random password
                length = random.randint(6, 12)
                new_pass = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
                # Add symbol
                if random.random() > 0.5:
                    new_pass += random.choice(self.symbols)
                all_passwords.add(new_pass)
            else:
                # Mutate existing password
                base_pass = random.choice(list(all_passwords))

                # Apply random mutation
                mutation_type = random.randint(1, 8)

                if mutation_type == 1:
                    # Add number
                    new_pass = base_pass + str(random.randint(0, 9999))
                elif mutation_type == 2:
                    # Add symbol
                    new_pass = base_pass + random.choice(self.symbols)
                elif mutation_type == 3:
                    # Capitalize random letters
                    chars = list(base_pass)
                    for i in range(random.randint(1, 3)):
                        if i < len(chars) and chars[i].isalpha():
                            chars[i] = chars[i].upper()
                    new_pass = ''.join(chars)
                elif mutation_type == 4:
                    # Reverse
                    new_pass = base_pass[::-1]
                elif mutation_type == 5:
                    # Double the password
                    new_pass = base_pass * 2
                elif mutation_type == 6:
                    # Add birth year if available
                    birth = self.data.get('birth', '').strip()
                    if birth:
                        birth_digits = ''.join(filter(str.isdigit, birth))
                        if birth_digits and len(birth_digits) >= 2:
                            new_pass = base_pass + birth_digits[-2:]
                        else:
                            new_pass = base_pass + str(random.randint(10, 99))
                    else:
                        new_pass = base_pass + str(random.randint(10, 99))
                elif mutation_type == 7:
                    # Add phone last digits if available
                    phone = self.data.get('phone', '').strip()
                    if phone:
                        phone_digits = ''.join(filter(str.isdigit, phone))
                        if phone_digits and len(phone_digits) >= 4:
                            new_pass = base_pass + phone_digits[-4:]
                        else:
                            new_pass = base_pass + str(random.randint(1000, 9999))
                    else:
                        new_pass = base_pass + str(random.randint(1000, 9999))
                else:
                    # Random suffix
                    suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 4)))
                    new_pass = base_pass + suffix

                all_passwords.add(new_pass)

            # Progress indicator
            if attempts % 1000 == 0:
                print(f"  Generated: {len(all_passwords):,} / {target_count:,}")

        # Final check - if still not enough, add completely random passwords
        if len(all_passwords) < target_count:
            print(f"[!] Generating {target_count - len(all_passwords):,} random passwords as fallback...")
            needed = target_count - len(all_passwords)
            for i in range(needed):
                # Generate random password
                length = random.randint(8, 15)
                parts = []
                parts.append(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6))))
                parts.append(str(random.randint(100, 9999)))
                if random.random() > 0.5:
                    parts.append(random.choice(self.symbols))

                new_pass = ''.join(parts)
                all_passwords.add(new_pass)

        return list(all_passwords)[:target_count]

    def generate(self, target_count):
        """Main generation method - GUARANTEED to return exactly target_count passwords"""
        print(f"\n[+] Target: {target_count:,} passwords")

        # Step 1: Extract all words from user data
        base_words = self.extract_words()
        print(f"[+] Extracted {len(base_words)} base words")

        # Step 2: Generate leet variations for base words
        all_words = []
        for word in base_words:
            all_words.extend(get_leet_variations(word))
        # Remove duplicates while preserving some order
        unique_words = []
        seen = set()
        for word in all_words:
            if word not in seen:
                seen.add(word)
                unique_words.append(word)
        print(f"[+] After leet variations: {len(unique_words)} unique words")

        # Step 3: Generate base combinations
        base_combinations = self.generate_base_combinations(unique_words)
        print(f"[+] Generated {len(base_combinations):,} base combinations")

        # Step 4: Expand to reach target count (GUARANTEED)
        final_passwords = self.expand_with_variations(base_combinations, target_count)

        # Ensure exact count
        if len(final_passwords) > target_count:
            final_passwords = final_passwords[:target_count]
        elif len(final_passwords) < target_count:
            # This should never happen, but just in case
            print(f"[!] WARNING: Only generated {len(final_passwords):,} passwords")
            print(f"[!] Adding random passwords to reach {target_count:,}...")
            while len(final_passwords) < target_count:
                random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
                final_passwords.append(random_pass)

        return final_passwords


# ==========[ GENERATE WORDLIST ]==========
def generate_wordlist():
    banner()
    print(">>> PERSONAL INFORMATION COLLECTION\n")
    print("📝 Enter target's personal details (leave blank if unknown)")
    print("-" * 50)

    data = {
        # Basic personal info
        "name": input(" First Name         : ").strip() or "John",
        "surname": input(" Last Name          : ").strip() or "Doe",
        "nick": input(" Nicknames (comma)  : ").strip() or "johnny,jd",

        # Family & important people
        "spouse": input(" Spouse/Partner     : ").strip(),
        "child": input(" Children names     : ").strip(),
        "pet": input(" Pet names          : ").strip(),
        "mother": input(" Mother's name      : ").strip(),
        "father": input(" Father's name      : ").strip(),

        # Dates
        "birth": input(" Birth date (YYYY)  : ").strip() or "1990",
        "anniversary": input(" Anniversary date   : ").strip(),

        # Location
        "city": input(" City               : ").strip() or "London",
        "country": input(" Country            : ").strip() or "UK",

        # Sports & Teams
        "team": input(" Favorite Team      : ").strip() or "lakers",
        "player": input(" Favorite Player    : ").strip(),
        "sport": input(" Favorite Sport     : ").strip() or "football",

        # Hobbies & Interests
        "hobby": input(" Hobbies (comma)    : ").strip() or "gaming,reading",

        # Work & Education
        "job": input(" Job/Profession     : ").strip(),
        "company": input(" Company name       : ").strip(),
        "school": input(" High School        : ").strip(),
        "university": input(" University         : ").strip(),

        # Vehicles
        "car": input(" Car model          : ").strip(),
        "bike": input(" Bike/Motorcycle    : ").strip(),

        # Contact info
        "phone": input(" Phone Number       : ").strip() or "1234567890",
        "email_local": input(" Email (before @)   : ").strip(),

        # Favorites
        "favorite": input(" Other favorites (comma): ").strip() or "password,secret",
    }

    print("\n" + "=" * 50)
    print("📊 WORDLIST SIZE OPTIONS")
    print("=" * 50)
    print("""
   1) 1,000      (Quick test)
   2) 10,000     (Small)
   3) 25,000     (Medium)
   4) 50,000     (Large)  ← RECOMMENDED
   5) 100,000    (Huge)
   6) 250,000    (Massive)
   7) 500,000    (Insane)
   8) 1,000,000  (Extreme)
-------------------------------------------
""")

    choice = input(" Select option (1-8): ").strip()

    sizes = {
        "1": 1000, "2": 10000, "3": 25000, "4": 50000,
        "5": 100000, "6": 250000, "7": 500000, "8": 1000000
    }

    if choice not in sizes:
        print(f"[!] Invalid choice. Defaulting to 50,000")
        choice = "4"

    target = sizes[choice]

    print(f"\n[+] Generating EXACTLY {target:,} personal passwords...")
    print("[+] Based on target's personal information...")
    start_time = time.time()

    # Initialize generator
    generator = PasswordGenerator(data)

    # Generate passwords (GUARANTEED)
    wordlist = generator.generate(target)

    # Save to file
    folder = "GVDILIX_OUTPUT"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_name = data['name'].lower() if data['name'] else "target"
    filename = f"{folder}/{target_name}_{target}_{timestamp}.txt"

    print(f"[+] Saving {len(wordlist):,} passwords to {filename}...")

    with open(filename, "w", encoding='utf-8') as f:
        for i, password in enumerate(wordlist, 1):
            f.write(f"{password}\n")

    end_time = time.time() - start_time

    print(f"\n✅ SUCCESS: Generated EXACTLY {len(wordlist):,} personal passwords")
    print(f"✅ File: {filename}")
    print(f"✅ Time: {end_time:.2f} seconds ({end_time / 60:.2f} minutes)")
    print(f"✅ Speed: {len(wordlist) / end_time:.0f} passwords/second")

    # Show sample
    print("\n📋 Sample passwords (first 10):")
    print("-" * 30)
    for i, pw in enumerate(wordlist[:10], 1):
        print(f"   {i:2}. {pw}")

    if len(wordlist) > 10:
        print(f"   ... and {len(wordlist) - 10:,} more!")

    print("\n🔥 GVDILIX - Personal Wordlist Complete!")
    input("\nPress Enter to return to main menu...")


# ==========[ MAIN MENU ]==========
def main_menu():
    while True:
        banner()
        print("📋 MAIN MENU\n")
        print("  1) Generate Personal Wordlist")
        print("  2) View/Manage Existing Wordlists")
        print("  3) Exit Program")
        print("\n" + "=" * 50)

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '1':
            generate_wordlist()
        elif choice == '2':
            view_wordlists()
        elif choice == '3':
            banner()
            print("\n👋 Thank you for using GVDILIX WordForge!")
            print("   Stay secure! 🔒\n")
            break
        else:
            print("[!] Invalid choice. Please select 1, 2, or 3.")
            time.sleep(1)


# ==========[ MAIN PROGRAM ]==========
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Process interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("[!] Please report this issue")
        import traceback

        traceback.print_exc()
        input("\nPress Enter to exit...")
