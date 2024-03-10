from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence  # To split the audio file on silent parts
import sys

def extend_silences(audio_file):
    sound = AudioSegment.from_file(audio_file, format="mp3")

    # Define silence to be anything under -35 dBFS
    silence_threshold = -35

    # Use detect_silence to find silences (returns a list of (start_i, end_i) tuples)
    silences = detect_silence(sound, min_silence_len=100, silence_thresh=silence_threshold)

    # Process each found silence
    chunks = []
    last_pos = 0
    for start_i, end_i in silences:
        duration = end_i - start_i
        if 450 <= duration <= 10000:  # Approximately 0.5s of silence
            # Adding the non-silent audio before the silence
            chunks.append(sound[last_pos:start_i])
            # Generate silence of 3s
            extended_silence = AudioSegment.silent(duration=4500)
            chunks.append(extended_silence)
            last_pos = end_i

    # Adding the last audio part
    chunks.append(sound[last_pos:])

    # Combine all the chunks back together
    extended_silence_audio = sum(chunks)

    # Export the result
    output_file = "output_extended_silences.mp3"
    extended_silence_audio.export(output_file, format="mp3")

    return output_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_file_path = sys.argv[1]
        result = extend_silences(audio_file_path)
        print(f"Processed audio saved to {result}")
    else:
        print("Usage: python script.py <path_to_mp3_file>")
