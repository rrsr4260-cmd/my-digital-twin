import librosa
import soundfile as sf

audio, sr = librosa.load("data/voice/my_voice.wav", sr=22050)
sf.write("data/voice/my_voice.wav", audio, 22050)

print("Voice converted to correct format.")