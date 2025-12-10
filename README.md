# WAV Pitch Changer

A simple Python tool to change the pitch of WAV audio files by a given percentage. 

## Features

- Change pitch of WAV files without affecting tempo/speed
- Simple command-line interface
- Percentage-based pitch adjustment (positive to increase, negative to decrease)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yhw032/pitch-changer.git
cd pitch-changer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.6+
- librosa
- numpy
- soundfile

## Usage

```bash
python pitch_changer.py <input_file> <output_file> <pitch_percentage>
```

### Arguments

- `input_file`: Path to the input WAV file
- `output_file`: Path for the output WAV file
- `pitch_percentage`: Percentage to change pitch (e.g., 10 for 10% higher, -10 for 10% lower)

### Examples

Increase pitch by 10%: 
```bash
python pitch_changer.py input.wav output.wav 10
```

Decrease pitch by 15%:
```bash
python pitch_changer.py input.wav output.wav -15
```

Keep the same pitch (no change):
```bash
python pitch_changer.py input. wav output.wav 0
```

## How It Works

The tool uses the `librosa` library to:
1. Load the WAV file
2. Calculate the pitch shift in semitones from the percentage
3. Apply the pitch shift without changing tempo
4. Save the result as a new WAV file

The conversion formula:  **semitones = 12 × log₂(1 + percentage/100)**

## License

MIT License