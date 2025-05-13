import os
import pyttsx3
import json
import sounddevice as sd
from scipy.io.wavfile import write

BOOKS_DIR = "Books"
MARKS_DIR = "Audiomarks"

engine = pyttsx3.init()

def record_voice_sample(filename="voice1.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(os.path.join("voices", filename), fs, recording)
    print(f"Voice sample saved as {filename}.")


def list_books():
    print("\nAvailable Books:")
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith('.txt')]
    for i, book in enumerate(books):
        print(f"{i + 1}. {book}")
    return books

def load_book(filename):
    with open(os.path.join(BOOKS_DIR, filename), 'r') as f:
        return f.readlines()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def save_audiomark(book_name, line_no):
    filepath = os.path.join(MARKS_DIR, f"{book_name}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            marks = json.load(f)
    else:
        marks = []

    marks.append(line_no)
    with open(filepath, 'w') as f:
        json.dump(marks, f)

    print(f"Audiomark added at line {line_no}.")

def get_audiomarks(book_name):
    filepath = os.path.join(MARKS_DIR, f"{book_name}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def main():
    books = list_books()
    choice = input("\nSelect a book to play: ")
    choice = int(choice) - 1
    selected_book = books[choice]
    lines = load_book(selected_book)

    marks = get_audiomarks(selected_book)
    print(f"\nExisting audiomarks: {marks}")
    start_line = int(input("Enter line number to start from (or 0): "))

    for i in range(start_line, len(lines)):
        print(f"\nLine {i}: {lines[i].strip()}")
        speak_text(lines[i])
        
        action = input("Press Enter to continue, 'm' to add audiomark, 'q' to quit: ")
        if action == 'm':
            save_audiomark(selected_book, i)
        elif action == 'q':
            print("Stopping playback.")
            break

if __name__ == "__main__":
    if not os.path.exists(MARKS_DIR):
        os.makedirs(MARKS_DIR)
    main()
