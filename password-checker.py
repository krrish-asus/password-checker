# checker.py
import math
import re

COMMON_PASSWORDS = {
    "123456","password","123456789","12345678","12345","qwerty","abc123","password1"
}

def entropy(password):
    # estimate entropy based on character set size
    sets = 0
    if re.search(r'[a-z]', password): sets += 26
    if re.search(r'[A-Z]', password): sets += 26
    if re.search(r'\d', password): sets += 10
    if re.search(r'[^A-Za-z0-9]', password): sets += 32
    if sets == 0:
        return 0
    return round(len(password) * math.log2(sets), 2)

def score(password):
    e = entropy(password)
    length = len(password)
    reasons = []
    if password.lower() in COMMON_PASSWORDS:
        reasons.append("Very common password")
    if length < 8:
        reasons.append("Too short (minimum 8)")
    if re.search(r'(.)\1\1', password):
        reasons.append("Repeated characters")
    if re.search(r'(1234|abcd|qwerty)', password.lower()):
        reasons.append("Contains common pattern")
    # categories
    categories = sum(bool(re.search(p, password)) for p in [r'[a-z]', r'[A-Z]', r'\d', r'[^A-Za-z0-9]'])
    if categories < 3:
        reasons.append("Lacks character variety (use upper/lower/digits/symbols)")

    strength = "Weak"
    if e > 60 and length >= 12 and categories >= 3:
        strength = "Strong"
    elif e > 40 and length >= 10:
        strength = "Good"
    else:
        strength = "Weak"
    return {"password": password, "entropy": e, "strength": strength, "reasons": reasons}

def main():
    while True:
        pwd = input("Enter password (or 'q' to quit): ").strip()
        if pwd.lower() == 'q':
            break
        res = score(pwd)
        print(f"\nEntropy: {res['entropy']} bits")
        print(f"Strength: {res['strength']}")
        if res['reasons']:
            print("Issues:")
            for r in res['reasons']:
                print(" -", r)
        else:
            print("No obvious issues found.")
        print("-"*30)

if __name__ == "__main__":
    main()
