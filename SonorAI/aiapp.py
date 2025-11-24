import numpy as np
import librosa
import soundfile as sf
import crepe
from collections import defaultdict
import tensorflow

from music21 import pitch, stream
from music21.instrument import AcousticGuitar
from music21.tempo import MetronomeMark
from music21.meter.base import TimeSignature
from music21.note import Note, Rest
from music21.chord import Chord
from music21.metadata import Metadata

class AudioAnalysis: 
    @staticmethod
    def frequency_to_midi(frequency): 
        """Convert frequency (hz) to MIDI note integer"""
        if frequency <= 0 or np.isnan(frequency) or frequency is None: 
            return None
        else: 
            midi_float = 69+12*np.log2(frequency/440.0)
            return int(np.round(midi_float)) # Round to avoid accidental sharps
    
    @staticmethod
    def midi_to_note(midi): 
        """Convert MIDI note integer to human readable note"""
        pitch_object = pitch.Pitch(midi=midi)
        return pitch_object.nameWithOctave # Return symbol
    
    @classmethod
    def ai_analysis(cls, audio_file, confidence_threshold=0.55, min_length=0.03, delta=0.005): 
        """Get notes using CREPE neural network analysis"""
        # Load audio_file using librosa (y=audio waveform, sr=sample rate)
        # NOTE: sr=None preserves file sample rate, mono=True assumes 1 audio source
        y, sr = librosa.load(path=audio_file, sr=None, mono=True)
        
        # Apply CREPE nn analysis
        time, frequency, confidence, _ = crepe.predict(audio=y, sr=sr, viterbi=True)
        
        # Get MIDI note integers for each time frame and trim low confidence notes
        midi_ints = [cls.frequency_to_midi(f) for f in frequency]
        for idx in range(len(time)): 
            if confidence[idx] < confidence_threshold: 
                midi_ints[idx] = None
        
        # Group notes to compute note periods
        notes = [] # Add dict("midi_int", "start_time", "end_time", "length") objects
        for i in range(len(time)): 
            # Skip blank time frame
            if midi_ints[i] is None: 
                continue

            # Create note for active time frame
            else: 
                note = {
                    "midi_int": midi_ints[i], 
                    "start_time": time[i] - delta, 
                    "end_time": None, 
                    "length": None
                }

                # Find end_time by similar sequential MIDI note integers
                j = i+1
                while midi_ints[j] == note["midi_int"] and j < len(time): 
                    j += 1
                note["end_time"] = time[j-1] + delta
                note["length"] = note["end_time"] - note["start_time"]

                # Trim short notes
                if note["length"] >= min_length: 
                    notes.append(note)

        return notes, y, sr
    
    @staticmethod
    def get_tempo(y, sr): 
        """Get tempo using librosa"""
        # Separate harmonics and percussives
        _, y_percussive = librosa.effects.hpss(y)
        # Get tempo using librosa.beat.beat_track with percussive waveform
        tempo, _ = librosa.beat.beat_track(y=y_percussive, sr=sr)
        # If tempo retrieval fails, assume 120.0
        if tempo <= 0: 
            tempo = 120.0
        return float(tempo)
    
    @staticmethod
    def get_quarter_frame(time, tempo): 
        """
        Get quarter-note-based frame position using time (seconds) 
        NOTE: Rounds to minimum length sixteenth-notes
        """
        # Find frame position for the quarter-note
        quarter_frame = time*tempo/60.0
        # Get rounded frame position for the quarter-note
        # NOTE: 1 sixteenth-note = 1/4 quarter-note
        return float(np.round(4.0*quarter_frame)/4.0)
    
    @classmethod
    def generate_musicxml(cls, notes, tempo, output_path, title, epsilon=1e-8): 
        """Get musicxml file contents using class functions"""
        # Compute quarter start position and length for each note
        for note in notes: 
            note["quarter_start"] = cls.get_quarter_frame(note["start_time"], tempo)
            note["quarter_length"] = cls.get_quarter_frame(note["length"], tempo)
        
        # Group notes into frames to account for chords by comparing quarter_start
        frames = defaultdict(list)
        for note in notes: 
            frames[note["quarter_start"]].append(note)
        
        # Create MusicXML elements
        score = stream.Score() # Parent container, contains the parts
        part = stream.Part() # Child container, contains the music data
        
        # Fill MusicXML part data
        part.append(AcousticGuitar()) # Add accoustic guitar
        part.append(MetronomeMark(number=tempo)) # Add tempo
        part.append(TimeSignature('4/4')) # Add time signature (assumes 4/4)

        frame_positions = sorted(frames.keys())
        prev = 0.0
        forward = None
        for curr in frame_positions: 
            # Check for rest
            if curr - prev > epsilon: 
                r = Rest(length=curr-prev)
                part.append(r)
            # Add single note
            if len(frames[curr]) == 1: 
                note = frames[curr][0]
                forward = note["quarter_length"]
                n = Note(midi=note["midi_int"], quarterLength=forward)
                part.append(n)
            # Add chord
            else: 
                midi_ints = []
                lengths = []
                for note in frames[curr]: 
                    midi_ints.append(note["midi_int"])
                    lengths.append(note["quarter_length"])
                forward = max(lengths)
                c = Chord(midi_ints, quarterLength=forward)
                part.append(c)
            # Update prev
            prev = curr + forward

        # Fill MusicXML score data
        score.insert(0, Metadata())
        score.metadata.title = title
        score.append(part) # Add part
        score.write(fmt="musicxml", fp=output_path) # Write to MusicXML file

    @classmethod
    def audio_analysis(cls, audio_file, output_path="out.musicxml", title="Untitled document", epsilon=1e-8, confidence_threshold=0.55, min_length=0.03, delta=0.005): 
        notes, y, sr = cls.ai_analysis(audio_file=audio_file, confidence_threshold=confidence_threshold, min_length=min_length, delta=delta)
        tempo = cls.get_tempo(y, sr)
        cls.generate_musicxml(notes=notes, tempo=tempo, output_path=output_path, title=title, epsilon=epsilon)
