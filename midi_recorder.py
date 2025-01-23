#!/usr/bin/env python3

import mido
import sys
import time
from datetime import datetime

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
    
    # Get the first available port
    port_name = mido.get_input_names()[0]
    print(f"\nUsing MIDI input port: {port_name}")

    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"piano_recording_{timestamp}.mid"
    
    # Create a new MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    print("\nRecording MIDI events... Press Ctrl+C to stop recording.")
    
    try:
        with mido.open_input(port_name) as port:
            start_time = time.time()
            
            while True:
                # Wait for MIDI message
                msg = port.receive()
                
                # Calculate time since last message
                current_time = time.time()
                delta_time = int((current_time - start_time) * 1000)  # Convert to milliseconds
                msg.time = delta_time
                
                # Add message to track
                track.append(msg)
                
                # Print message details
                if msg.type in ['note_on', 'note_off']:
                    print(f"Note {'On' if msg.type == 'note_on' else 'Off'}: "
                          f"Note={msg.note}, Velocity={msg.velocity}")
                elif msg.type == 'control_change' and msg.control == 64:
                    print(f"Sustain Pedal: {'On' if msg.value >= 64 else 'Off'}")
                
                start_time = current_time

    except KeyboardInterrupt:
        print("\nRecording stopped.")
    
    # Save the MIDI file
    mid.save(output_file)
    print(f"\nRecording saved to: {output_file}")

if __name__ == "__main__":
    record_midi()
