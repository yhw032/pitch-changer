# WAV Pitch Changer

A simple Python tool to change the pitch of WAV audio files by a given percentage using professional-quality Rubberband library.

## Features

- Change pitch of WAV files without affecting tempo/speed
- Simple command-line interface
- Percentage-based pitch adjustment (positive to increase, negative to decrease)
- Supports both mono and stereo audio files

## Requirements

- Python 3.6+
- Rubberband audio library (system dependency)
- Python packages: librosa, numpy, soundfile, pyrubberband

## Installation

### Step 1: Install Rubberband Library

**Rubberband must be installed on your system before installing Python packages.**

#### macOS
```bash
brew install rubberband
```

#### Ubuntu/Debian/Linux Mint
```bash
sudo apt-get update
sudo apt-get install rubberband-cli librubberband-dev
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install rubberband rubberband-devel
```

#### Arch Linux
```bash
sudo pacman -S rubberband
```

#### Windows
1. Download Rubberband from the official website: https://breakfastquay.com/rubberband/
2. Extract the downloaded archive to a location (e.g., `C:\Program Files\Rubberband`)
3. Add the Rubberband `bin` directory to your system PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the path to Rubberband's bin folder (e.g., `C:\Program Files\Rubberband\bin`)
   - Click "OK" to save

**Alternative for Windows:** Use WSL (Windows Subsystem for Linux) and follow the Ubuntu instructions. 

### Step 2: Clone Repository

```bash
git clone https://github.com/yhw032/pitch-changer.git
cd pitch-changer
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pitch_changer. py <input_file> <output_file> <pitch_percentage>
```

### Arguments

- `input_file`: Path to the input WAV file
- `output_file`: Path for the output WAV file
- `pitch_percentage`: Percentage to change pitch (e.g., 10 for 10% higher, -10 for 10% lower)

### Examples

Increase pitch by 10%:  
```bash
python pitch_changer.py input.wav output. wav 10
```

Decrease pitch by 15%:
```bash
python pitch_changer.py input.wav output.wav -15
```

Increase pitch by 25%:
```bash
python pitch_changer.py input.wav output.wav 25
```

Keep the same pitch (no change):
```bash
python pitch_changer.py input.wav output.wav 0
```

## How It Works

The tool uses professional audio processing libraries to achieve high-quality pitch shifting:

1. **Load**:  Uses `librosa` to load the WAV file with original sample rate preserved
2. **Calculate**: Converts percentage to semitones using the formula: **semitones = 12 × log₂(1 + percentage/100)**
3. **Process**: Applies pitch shift using `pyrubberband` (Rubberband library wrapper) which provides: 
   - Professional-quality time-stretching and pitch-shifting
   - Excellent transient preservation
   - Minimal audio artifacts
   - Natural sound quality
4. **Normalize**: Prevents clipping by normalizing audio if needed
5. **Save**: Outputs as 24-bit PCM WAV for maximum quality

## Troubleshooting

### "Rubberband not found" error

Make sure Rubberband is properly installed and accessible from your PATH:

**macOS/Linux:**
```bash
which rubberband
```

**Windows:**
```cmd
where rubberband
```

If the command returns nothing, Rubberband is not in your PATH.  Reinstall or add it to PATH.

### Import error for pyrubberband

If you get an import error, try reinstalling: 
```bash
pip uninstall pyrubberband
pip install pyrubberband
```

### Poor audio quality

- Ensure you're using the latest version with Rubberband
- Check that your input file is high quality (44.1kHz or 48kHz sample rate recommended)
- Avoid extreme pitch changes (beyond ±50%)

## Technical Details

- **Input formats**: WAV files (mono or stereo)
- **Output format**: 24-bit PCM WAV
- **Pitch shift range**: -50% to +100% (larger ranges may produce artifacts)
- **Quality**: Professional-grade using Rubberband library


## License

MIT License