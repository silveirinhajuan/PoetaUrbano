import pyttsx3

async def speak_this(text: str) -> bool:
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)
    
    engine.save_to_file(text, 'audio.mp3')
    
    engine.runAndWait()
    
