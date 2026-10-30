
def analyze_transcript(text):
    text = text.lower()

    rules = {
        "Urgent Pressure": [
            "immediately", "right now", "urgent",
            "உடனே", "அவசரம்",
            "వెంటనే", "అత్యవసరం"
        ],

        "Financial Request": [
            "send money", "transfer money", "bank account",
            "பணம் அனுப்பு", "பணம் செலுத்து",
            "డబ్బులు పంపండి", "డబ్బు చెల్లించండి"
        ],

        "Sensitive Information": [
            "otp", "password", "pin number",
            "ஓடிபி", "கடவுச்சொல்",
            "ఓటీపీ", "పాస్‌వర్డ్"
        ],

        "Threat or Emergency": [
            "police", "arrest", "emergency",
            "காவல்துறை", "கைது",
            "పోలీసులు", "అరెస్ట్"
        ],

        "Secrecy": [
            "don't tell anyone", "keep it secret",
            "யாரிடமும் சொல்லாதே",
            "ఎవరికీ చెప్పకండి"
        ]
    }

    findings = []

    for category, keywords in rules.items():
        matches = [
            word for word in keywords
            if word in text
        ]

        if matches:
            findings.append({
                "category": category,
                "matched_terms": matches
            })

    return findings

