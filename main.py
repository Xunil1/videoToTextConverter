# Import libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mp


def video_to_audio(in_path, out_path):
    """Convert video file to audio file"""

    video = mp.VideoFileClip(in_path)
    video.audio.write_audiofile(out_path)


def large_audio_to_text(path):
    """Split audio into chunks and apply speech recognition"""

    # Open audio file with pydub
    sound = AudioSegment.from_wav(path)
    # Split audio where silence is 700ms or greater and get chunks
    chunks = split_on_silence(sound, min_silence_len=700, silence_thresh=sound.dBFS - 14, keep_silence=700)

    # Create folder to store audio chunks
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    # Process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # Export chunk and save in folder
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # Recognize chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Convert to text
            try:
                text = r.recognize_google(audio_listened, language="ru-RU")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text + "\n"
    # Return text for all chunks
    return whole_text


# Create a speech recognition object
r = sr.Recognizer()
# Video to audio to text

name = "l5"

video_to_audio(name + '.mp4', name + '.wav')
result = large_audio_to_text(name + '.wav')
# Print to shell and file
print(result)
print(result, file=open(name + '.txt', 'w'))