#!/usr/bin/env ./venv/bin/python3

import mido
import sys
import time
from datetime import datetime
from simple_term_menu import TerminalMenu

def list_midi_ports():
    """List all available MIDI input ports"""
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(f"- {port}")

def record_midi():
    """Record MIDI events to a file"""
    # Check if any MIDI ports are available
    if not mido.get_input_names():
        print("No MIDI input ports found. Please connect your piano and try again.")
        sys.exit(1)

    # List available ports
    list_midi_ports()
    
    # Let user select the port
    ports = mido.get_input_names()
    terminal_menu = TerminalMenu(
        ports,
        title="Select MIDI input port:",
        menu_cursor="▶ ",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("bg_green", "fg_black"),
    )
    menu_index = terminal_menu.show()
    if menu_index is None:
        print("\nNo port selected. Exiting...")
        sys.exit(0)
        
    port_name = ports[menu_index]
    print(f"\nSelected MIDI input port: {port_name}")

    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"piano_recording_{timestamp}.mid"
    
    # Create a new MIDI file
    mid = mido.MidiFile(type=1, ticks_per_beat=480)
    
    # Create tempo track
    tempo_track = mido.MidiTrack()
    mid.tracks.append(tempo_track)
    
    # Add time signature and tempo events
    tempo_track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
    tempo_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    
    # Create track for piano events
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    print("\nRecording MIDI events... Press Ctrl+C to stop recording.")
    
    try:
        with mido.open_input(port_name) as port:
            start_time = time.time()
            
            while True:
                # Wait for MIDI message
                msg = port.receive()
                
                # Calculate time delta in MIDI ticks (480 per quarter note)
                current_time = time.time()
                delta_seconds = current_time - start_time
                msg.time = int(delta_seconds * 480)  # Convert to MIDI ticks
                
                # Add message to track
                track.append(msg)
                
                # Print message details
                if msg.type in ['note_on', 'note_off']:
                    note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][msg.note % 12]
                    octave = msg.note // 12 - 1
                    print(f"Note {'On' if msg.type == 'note_on' else 'Off'}: "
                          f"{note_name}{octave} (note={msg.note}, velocity={msg.velocity})")
                elif msg.type == 'control_change' and msg.control == 64:
                    print(f"Sustain Pedal: {'On' if msg.value >= 64 else 'Off'}")
                elif msg.type == 'control_change':
                    print(f"Control Change: control={msg.control}, value={msg.value}")
                
                start_time = current_time

    except KeyboardInterrupt:
        print("\nRecording stopped.")
    
    # Save the MIDI file
    mid.save(output_file)
    print(f"\nRecording saved to: {output_file}")

if __name__ == "__main__":
    record_midi()
