import pretty_midi
import numpy as np
# For plotting
import mir_eval.display
import librosa.display
import matplotlib.pyplot as plt
# For putting audio in the notebook
import IPython.display

'''

What's my plan with this? I want to be able to:

1. Select a short MIDI clip.
2. Generate something new and weird with it.
3. Save new midi.

Additionals:

- ran into trouble with MIDI that was too long, so figured out how to crop it down to 5 secs.
- ran into more trouble with MIDI that had tempo changes - for now, find one with a regular tempo
	but work on figuring out methods to normalize tempos of others.

'''

pm = pretty_midi.PrettyMIDI(initial_tempo=80)

inst = pretty_midi.Instrument(program=42, is_drum=False, name='my cello')
pm.instruments.append(inst)

velocity = 100
for pitch, start, end in zip([60, 62, 64], [0.2, 0.6, 1.0], [1.1, 1.7, 2.3]):
    inst.notes.append(pretty_midi.Note(velocity, pitch, start, end))
print(inst.notes)

# We'll just do a 1-semitone pitch ramp up
n_steps = 512
bend_range = 8192//2
for time, pitch in zip(np.linspace(1.5, 2.3, n_steps),
                       range(0, bend_range, bend_range//n_steps)):
    inst.pitch_bends.append(pretty_midi.PitchBend(pitch, time))

def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
    # Use librosa's specshow function for displaying the piano roll
    librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                             hop_length=1, sr=fs, x_axis='time', y_axis='cqt_note',
                             fmin=pretty_midi.note_number_to_hz(start_pitch))

plt.figure(figsize=(8, 4))
plot_piano_roll(pm, 56, 70)


pm = pretty_midi.PrettyMIDI('example.mid')

plt.figure(figsize=(12, 4))
plot_piano_roll(pm, 24, 84)

'''
'''
Ok, so I was able to load a midi file into a midi data object and convert it into a note sequence thusly:

import note_seq
import pretty_midi (not needed if I'm calling note_seq.midi_io.midi_to_note_sequence(midi_data)
midi_data = pretty_midi.PrettyMIDI('yourmidi.mid')
zug = note_seq.midi_io.midi_to_note_sequence(midi_data)
zug2 = note_seq.trim_note_sequence(zug, 0, 5.0)


*You can list methods for python objects with dir(object)!
Wait, that just lists all related vars. Have to do this:

object_methods = [method_name for method_name in dir(object)
                  if callable(getattr(object, method_name))]

def methods(obj):
  return [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]

Head of zug looks like:

ticks_per_quarter: 1024
time_signatures {
  numerator: 4
  denominator: 4
}
key_signatures {
  key: A_SHARP
}
tempos {
  qpm: 99.96051559633945
}

https://github.com/magenta/note-seq/blob/master/note_seq/sequences_lib.py
https://github.com/magenta/note-seq/blob/master/note_seq/midi_io.py
https://colab.research.google.com/notebooks/magenta/piano_transformer/piano_transformer.ipynb
https://github.com/magenta/note-seq/blob/master/note_seq/notebook_utils.py
https://github.com/magenta/note-seq/blob/master/note_seq/sequences_lib.py
https://craffel.github.io/pretty-midi/
https://towardsdatascience.com/importing-data-to-google-colab-the-clean-way-5ceef9e9e3c8
'''
