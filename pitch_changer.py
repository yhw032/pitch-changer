#!/usr/bin/env python3
"""
WAV Pitch Changer

A simple tool to change the pitch of WAV audio files by a given percentage.
Uses Rubberband for high-quality pitch shifting with advanced options.
"""

import sys
import os
import numpy as np
import soundfile as sf
import pyrubberband as pyrb


def percentage_to_semitones(percentage):
    """
    Convert pitch change percentage to semitones. 
    
    Args:
        percentage (float): Pitch change percentage (e.g., 10 for 10% higher)
    
    Returns:
        float:  Pitch shift in semitones
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
        # Load the audio file - use soundfile directly for better quality
        print(f"Loading audio file: {input_file}")
        audio, sample_rate = sf.read(input_file, always_2d=False)
        
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Audio shape: {audio.shape}")
        print(f"Audio dtype: {audio.dtype}")
        
        # Convert percentage to semitones
        semitones = percentage_to_semitones(pitch_percentage)
        print(f"Pitch change:  {pitch_percentage}% ({semitones:.2f} semitones)")
        
        # Ensure audio is in float32 format for processing
        if audio.dtype != np.float32:
            print(f"Converting audio from {audio.dtype} to float32")
            audio = audio.astype(np.float32)
        
        # Normalize input to prevent clipping during processing
        input_max = np.abs(audio).max()
        if input_max > 0:
            audio = audio / input_max
            print(f"Input normalized (original peak: {input_max:.4f})")
        
        # Apply pitch shift using Rubberband with high-quality settings
        print("Applying pitch shift with Rubberband (high quality mode)...")
        
        if audio.ndim == 1:
            # Mono audio
            audio_shifted = pyrb.pitch_shift(
                audio, 
                sample_rate, 
                semitones,
                rbargs={
                    '--fine':  '',           # Use finer processing
                    '--formant': '',        # Preserve formants (important for vocals)
                    '--pitch-hq': '',       # High quality pitch mode
                }
            )
        else:
            # Stereo or multi-channel audio
            # Process each channel separately for best quality
            print(f"Processing {audio.shape[1]} channels separately...")
            channels_shifted = []
            
            for i in range(audio.shape[1]):
                print(f"  Processing channel {i+1}/{audio.shape[1]}...")
                channel_shifted = pyrb.pitch_shift(
                    audio[:, i], 
                    sample_rate, 
                    semitones,
                    rbargs={
                        '--fine': '',
                        '--formant': '',
                        '--pitch-hq':  '',
                    }
                )
                channels_shifted.append(channel_shifted)
            
            # Combine channels back
            audio_shifted = np.column_stack(channels_shifted)
        
        # Restore original amplitude
        if input_max > 0:
            audio_shifted = audio_shifted * input_max
            print(f"Amplitude restored to original level")
        
        # Check for clipping and normalize if necessary
        output_max = np.abs(audio_shifted).max()
        if output_max > 1.0:
            print(f"Warning: Output would clip (peak: {output_max:.2f}), normalizing to 0.95")
            audio_shifted = audio_shifted / output_max * 0.95
        elif output_max > 0.95:
            print(f"Output peak:  {output_max:.2f} (close to maximum)")
        else:
            print(f"Output peak: {output_max:.2f}")
        
        # Save the output file with highest quality settings
        print(f"Saving output file: {output_file}")
        sf.write(
            output_file,
            audio_shifted,
            sample_rate,
            subtype='PCM_24'  # 24-bit PCM
        )
        
        print("Done!  Pitch changed successfully with high quality.")
        
    except FileNotFoundError: 
        print(f"Error:  Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) != 4:
        print("Usage: python pitch_changer.py <input_file> <output_file> <pitch_percentage>")
        print("\nExamples:")
        print("  python pitch_changer.py input.wav output.wav 10    # Increase pitch by 10%")
        print("  python pitch_changer.py input.wav output. wav -10   # Decrease pitch by 10%")
        print("\nFor best quality:")
        print("  - Use input files with 44.1kHz or higher sample rate")
        print("  - Keep pitch changes moderate (±20% or less)")
        print("  - Use uncompressed WAV files as input")
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
    
    # Validate pitch percentage range
    if abs(pitch_percentage) > 50:
        print(f"Warning: Large pitch change ({pitch_percentage}%) may produce artifacts.")
        print("For best quality, consider staying within ±20%.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Change the pitch
    change_pitch(input_file, output_file, pitch_percentage)


if __name__ == "__main__":
    main()