import os
import sys
import subprocess
import time

# Configuration
INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'
SCRIPT_NAME = 'pitch_changer.py'

def run_batch(pitch_percentage):
    # 1. Check and create directories
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: '{INPUT_DIR}' folder not found. Please create it and add WAV files.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📂 Created '{OUTPUT_DIR}' folder.")

    # 2. Get list of files to process
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.wav')]
    total_files = len(files)

    if total_files == 0:
        print(f"⚠️ No WAV files found in '{INPUT_DIR}'.")
        return

    print("=" * 60)
    print(f"🚀 Starting Batch Processing")
    print(f"   - Total files: {total_files}")
    print(f"   - Pitch change: {pitch_percentage}%")
    print("=" * 60)

    success_count = 0
    fail_count = 0
    start_time = time.time()

    # 3. Iterate and process files
    for i, filename in enumerate(files, 1):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"\n[{i}/{total_files}] Processing: {filename} ...")
        
        # Execute pitch_changer.py using subprocess
        # Uses the current python interpreter (sys.executable)
        cmd = [
            sys.executable,       # python command
            SCRIPT_NAME,          # script to run
            input_path,           # input file path
            output_path,          # output file path
            str(pitch_percentage) # pitch percentage
        ]

        try:
            # Run external script
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ Success")
                success_count += 1
            else:
                print(f"   ❌ Failed")
                print(f"      [Error Log]\n{result.stdout}\n{result.stderr}")
                fail_count += 1
                
        except Exception as e:
            print(f"   ❌ Execution Error: {str(e)}")
            fail_count += 1

    # 4. Final Report
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🎉 All tasks completed.")
    print(f"   - Total duration: {duration:.2f}s")
    print(f"   - Success: {success_count}")
    print(f"   - Failed:  {fail_count}")
    print(f"   - Output location: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batch_runner.py <pitch_percentage>")
        print("Example: python batch_runner.py 10")
        sys.exit(1)
    
    try:
        percentage = float(sys.argv[1])
        run_batch(percentage)
    except ValueError:
        print("Error: Pitch percentage must be a number.")