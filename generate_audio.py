import asyncio
import edge_tts
import os

# Create the uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Audio samples in six languages
examples = {
    "english": {
        "suspicious": "Your bank account will be blocked immediately. Tell me your OTP and transfer money right now.",
        "normal": "Hello, how are you? I will meet you tomorrow at the college.",
        "emergency": "My friend has had an accident. Please call me as soon as possible.",
        "voice": "en-US-AriaNeural"
    },

    "tamil": {
        "suspicious": "உங்கள் வங்கி கணக்கு உடனடியாக முடக்கப்படும். உங்கள் OTP எண்ணைச் சொல்லுங்கள், உடனே பணத்தை அனுப்புங்கள்.",
        "normal": "வணக்கம், எப்படி இருக்கிறீர்கள்? நாளை கல்லூரியில் உங்களைச் சந்திக்கிறேன்.",
        "emergency": "என் நண்பருக்கு விபத்து ஏற்பட்டுள்ளது. தயவுசெய்து முடிந்தவரை விரைவாக என்னை அழைக்கவும்.",
        "voice": "ta-IN-PallaviNeural"
    },

    "telugu": {
        "suspicious": "మీ బ్యాంక్ ఖాతా వెంటనే బ్లాక్ చేయబడుతుంది. మీ ఓటీపీ చెప్పండి, వెంటనే డబ్బులు పంపండి.",
        "normal": "నమస్కారం, మీరు ఎలా ఉన్నారు? రేపు కాలేజీలో మిమ్మల్ని కలుస్తాను.",
        "emergency": "నా స్నేహితుడికి ప్రమాదం జరిగింది. దయచేసి వీలైనంత త్వరగా నాకు ఫోన్ చేయండి.",
        "voice": "te-IN-ShrutiNeural"
    },

    "hindi": {
        "suspicious": "आपका बैंक खाता तुरंत बंद कर दिया जाएगा। अपना ओटीपी बताइए और तुरंत पैसे भेजिए।",
        "normal": "नमस्ते, आप कैसे हैं? मैं कल कॉलेज में आपसे मिलूंगा।",
        "emergency": "मेरे दोस्त का एक्सीडेंट हो गया है। कृपया जल्द से जल्द मुझे फोन करें।",
        "voice": "hi-IN-SwaraNeural"
    },

    "malayalam": {
        "suspicious": "നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ട് ഉടൻ ബ്ലോക്ക് ചെയ്യും. നിങ്ങളുടെ ഒടിപി പറയൂ, ഉടൻ പണം അയയ്ക്കൂ.",
        "normal": "നമസ്കാരം, സുഖമാണോ? നാളെ കോളേജിൽ നിങ്ങളെ കാണാം.",
        "emergency": "എന്റെ സുഹൃത്തിന് അപകടം സംഭവിച്ചു. ദയവായി കഴിയുന്നത്ര വേഗം എന്നെ വിളിക്കൂ.",
        "voice": "ml-IN-SobhanaNeural"
    },

    "kannada": {
        "suspicious": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ತಕ್ಷಣವೇ ನಿರ್ಬಂಧಿಸಲಾಗುತ್ತದೆ. ನಿಮ್ಮ OTP ಹೇಳಿ, ತಕ್ಷಣ ಹಣ ಕಳುಹಿಸಿ.",
        "normal": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ? ನಾಳೆ ಕಾಲೇಜಿನಲ್ಲಿ ನಿಮ್ಮನ್ನು ಭೇಟಿಯಾಗುತ್ತೇನೆ.",
        "emergency": "ನನ್ನ ಸ್ನೇಹಿತನಿಗೆ ಅಪಘಾತವಾಗಿದೆ. ದಯವಿಟ್ಟು ಸಾಧ್ಯವಾದಷ್ಟು ಬೇಗ ನನಗೆ ಕರೆ ಮಾಡಿ.",
        "voice": "kn-IN-SapnaNeural"
    }
}


# Function to generate an audio file
async def generate_file(text, voice, filename):
    output_path = os.path.join("uploads", filename)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

    print(f"Generated successfully: {output_path}")


# Generate all audio samples
async def main():
    categories = ["suspicious", "normal", "emergency"]

    for language, data in examples.items():
        for category in categories:
            filename = f"{category}_{language}.mp3"

            try:
                await generate_file(
                    data[category],
                    data["voice"],
                    filename
                )

            except Exception as error:
                print(f"Failed to generate {filename}: {error}")


# Run the program
if __name__ == "__main__":
    asyncio.run(main())