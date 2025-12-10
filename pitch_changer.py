#!/usr/bin/env python3
"""
WAV Pitch Changer

A simple tool to change the pitch of WAV audio files by a given percentage.
"""

import sys
import os
import numpy as np
import librosa
import soundfile as sf


def percentage_to_semitones(percentage):
    """
    Convert pitch change percentage to semitones.
    
    Args:
        percentage (float): Pitch change percentage (e.g., 10 for 10% higher)
    
    Returns:
        float: Pitch shift in semitones
    """
    # Formula: semitones = 12 * log2(1 + percentage/100)
    return 12 * np.log2(1 + percentage / 100)


def change_pitch(input_file, output_file, pitch_percentage):
    """
    Change the pitch of a WAV file by a given percentage.
    
    Args:
        input_file (str): Path to input WAV file
        output_file (str): Path to output WAV file
        pitch_percentage (float): Percentage to change pitch
    """
    try:
        # Load the audio file
        print(f"Loading audio file: {input_file}")
        audio, sample_rate = librosa.load(input_file, sr=None, mono=False)
        
        # Convert percentage to semitones
        semitones = percentage_to_semitones(pitch_percentage)
        print(f"Pitch change: {pitch_percentage}% ({semitones:.2f} semitones)")
        
        # Apply pitch shift
        print("Applying pitch shift...")
        if audio.ndim == 1:
            # Mono audio
            audio_shifted = librosa.effects.pitch_shift(audio, sr=sample_rate, n_steps=semitones)
        else:
            # Stereo or multi-channel audio
            audio_shifted = np.array([
                librosa.effects.pitch_shift(audio[i], sr=sample_rate, n_steps=semitones)
                for i in range(audio. shape[0])
            ])
        
        # Save the output file
        print(f"Saving output file: {output_file}")
        sf.write(output_file, audio_shifted. T if audio.ndim > 1 else audio_shifted, sample_rate)
        
        print("Done!  Pitch changed successfully.")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e: 
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) != 4:
        print("Usage: python pitch_changer.py <input_file> <output_file> <pitch_percentage>")
        print("\nExamples:")
        print("  python pitch_changer.py input.wav output.wav 10    # Increase pitch by 10%")
        print("  python pitch_changer.py input.wav output.wav -10   # Decrease pitch by 10%")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys. argv[2]
    
    try:
        pitch_percentage = float(sys.argv[3])
    except ValueError:
        print("Error:  Pitch percentage must be a number.")
        sys.exit(1)
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    # Validate pitch percentage range (optional:  you can adjust limits)
    if pitch_percentage < -50 or pitch_percentage > 100:
        print("Warning: Extreme pitch changes may produce unexpected results.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Change the pitch
    change_pitch(input_file, output_file, pitch_percentage)


if __name__ == "__main__":
    main()