import mido
from mido import MidiFile, MidiTrack, Message
import csv
import ast

def intervals_to_midi_pattern(intervals, start_note=60):
	"""
	Converts a list of intervals into a MIDI pattern (sequence of notes).

	:param intervals: A list of intervals (difference in pitch between notes).
	:param start_note: The MIDI note number to start the pattern from.
	:return: A list of MIDI note numbers forming the pattern.
	"""
	pattern = [start_note]
	for interval in intervals:
		pattern.append(pattern[-1] + interval)
	return pattern


def interpolate_cc_values(track, start_value, end_value, duration, control=2):
    """
    Adds interpolated CC values over the duration of a note.

    :param track: The MIDI track to append the messages to.
    :param start_value: The starting value of the CC.
    :param end_value: The ending value of the CC.
    :param duration: The duration over which to interpolate.
    :param control: The CC number to interpolate (default is 2).
    """
    num_steps = 10  # The number of steps you want to interpolate over
    step_duration = duration // num_steps
    for i in range(num_steps):
        interpolated_value = int(start_value + (end_value - start_value) * (i / num_steps))
        track.append(Message('control_change', control=control, value=interpolated_value, time=step_duration))

def append_pattern_to_track(track, pattern, bar_duration=1920):
	"""
	Appends a MIDI pattern to a track, followed by silence to align the next pattern to a new bar.

	:param track: The MIDI track to append the pattern to.
	:param pattern: The MIDI pattern to append.
	:param bar_duration: The duration of a bar in MIDI ticks (default is 1920 for a 4/4 bar).
	"""
	is_downbeat = True
	pattern_duration = 0
	previous_note = None  # Initialize previous note
	first_note=60
	is_first_note = True
	previous_top_note = first_note
	subpattern_duration = 0
	beat_duration = 480
	
	for note in pattern:
		# Check if current note is a top note
		is_top_note = is_downbeat and (previous_note is None or note > previous_note)

		# Set velocity based on whether it's a top note
		velocity = 120 if is_top_note else 30

		# Duration of a note alternates for a swing rhythm
		note_duration = 320 if is_downbeat else 140 # the upbeat is shorter to allow for silence before a top_note

		if is_top_note:
			if 'top_note_on' in locals():  # Turn off the previous top note if it's still playing
				track.append(Message('note_off', note=top_note_on, velocity=velocity, time=0))
				beat_align = beat_duration-(subpattern_duration%beat_duration)
				track.append(Message('note_off', note=0, velocity=0, time=beat_align))  # 20 ticks of silence
			top_note_on = note  # Remember the top note
			note_on = Message('note_on', note=top_note_on, velocity=velocity, time=0)
			track.append(note_on)  # Start playing the top note
			track.append(Message('control_change', control=2, value=70, time=0))  # Start of new subpattern
			subpattern_duration = 0  # Reset subpattern duration
			track.append(Message('note_off', note=0, velocity=0, time=320))

		# For other notes, play them normally
		if not is_top_note or note != top_note_on:
			note_on = Message('note_on', note=note, velocity=velocity, time=0)
			breath_value = 50 if is_downbeat else 30
			track.append(Message('control_change', control=2, value=breath_value, time=0))  # Start of new subpattern
			note_off = Message('note_off', note=note, velocity=velocity, time=note_duration)
			track.append(note_on)
			track.append(note_off)

		subpattern_duration += note_duration
		previous_note = note  # Update the previous note
		pattern_duration += note_duration
		is_downbeat = not is_downbeat

	# Turn off the last top note
	if 'top_note_on' in locals():
		track.append(Message('note_off', note=top_note_on, velocity=velocity, time=0))

	# Add silence to align the start of the next pattern with a new bar
	remaining_duration = bar_duration - (pattern_duration % bar_duration)
	if remaining_duration < bar_duration:
		track.append(Message('note_off', note=0, velocity=0, time=remaining_duration))
	# Add an extra bar of silence
	track.append(Message('note_off', note=0, velocity=0, time=bar_duration))
	

def send_all_notes_off(channel, midi_port):
	"""
	Sends an 'All Notes Off' message on the specified channel.

	:param channel: The MIDI channel (0-15).
	:param midi_port: The MIDI output port to send the message to.
	"""
	# MIDI 'All Notes Off' is a Control Change with controller number 123 and value 0
	all_notes_off = Message('control_change', channel=channel, control=123, value=0)
	midi_port.send(all_notes_off)


def create_combined_midi(patterns, output_file):
	"""
	Creates a single MIDI file from a list of MIDI patterns, each starting at a new bar.

	:param patterns: A list of MIDI patterns.
	:param output_file: The filename for the output MIDI file.
	"""
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)
	
	for pattern in patterns:
		append_pattern_to_track(track, pattern)

	mid.save(output_file)

def create_midi_for_single_pattern(pattern, pattern_id, index, num_instances, bar_duration=1920):
	"""
	Creates an individual MIDI file for a given pattern.

	:param pattern: The MIDI pattern.
	:param pattern_id: The ID of the pattern.
	:param index: The index number of the pattern.
	:param num_instances: The number of instances of the pattern.
	:param bar_duration: The duration of a bar in MIDI ticks.
	"""
	filename = f"pattern_{index}_{num_instances}_{pattern_id}.mid"
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)

	append_pattern_to_track(track, pattern, bar_duration)
	mid.save(filename)

# Read melodic patterns from CSV file and create individual MIDI files
patterns = []
with open('JazzPatt.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	next(reader)  # Skip the header row
	for index, row in enumerate(reader, start=1):
		# Convert the string representation of the list into a Python list
		pattern = ast.literal_eval(row[0]) # The interval patterns are in the first column
		pattern_id = row[1] # There's a pattern ID in the second column
		num_instances = row[2] # The third column contains the number of instances with that pattern in the corpus
		midi_pattern = intervals_to_midi_pattern(pattern)
		patterns.append(midi_pattern)
		create_midi_for_single_pattern(midi_pattern, pattern_id, index, num_instances)

# Create a combined MIDI file with all patterns
output_file = "JazzPatterns.midi"
create_combined_midi(patterns, output_file)