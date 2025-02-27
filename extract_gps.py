import argparse
import subprocess
import os

def create_process_config(output_bag_folder, topics, duration, start=None, end=None, restamp=True):
    """Creates a process.config file with the specified commands and parameters."""
    # Start building the cut command
    cut_command = "cut"
    
    if duration is not None:
        cut_command += f" --duration {duration}"
    if start is not None and end is not None:
        cut_command += f" --start {start} --end {end}"
    elif start is not None:
        cut_command += f" --start {start}"
    
    # Build the process.config content
    config_content = f"""{cut_command}
extract -t {' '.join(topics)}
"""
    
    # Add restamp if requested
    if restamp:
        config_content += "\nrestamp"

    # Write to process.config
    with open("process.config", "w") as config_file:
        config_file.write(config_content)

def process_bag(input_bag_folder, output_bag_folder, topics, duration, start=None, end=None, restamp=True):
    """
    Processes the input bag folder using the commands specified in process.config.
    """
    # Normalize the input and output paths to remove any trailing slashes
    input_bag_folder = os.path.normpath(input_bag_folder)
    output_bag_folder = os.path.normpath(output_bag_folder)

    # Convert paths to absolute paths
    input_bag_folder = os.path.abspath(input_bag_folder)
    output_bag_folder = os.path.abspath(output_bag_folder)

    # Create the process.config file
    create_process_config(output_bag_folder, topics, duration, start, end, restamp)

    try:
        # Run the ros2 bag process command
        command = ["ros2", "bag", "process", "-c", "process.config", input_bag_folder, "-o", output_bag_folder]
        subprocess.run(command, check=True)

        print(f"Processing complete. Output bag folder: {output_bag_folder}")
    finally:
        # Remove the process.config file after processing
        if os.path.exists("process.config"):
            os.remove("process.config")
            print("Removed process.config file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a ROS 2 bag folder using a process.config file.")
    parser.add_argument("input_bag_folder", type=str, help="Path to the input bag folder.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output bag folder.")
    parser.add_argument("--topics", type=str, nargs="+", required=True, help="List of topics to extract.")
    parser.add_argument("--duration", type=float, help="Duration to cut from the bag (in seconds).")
    parser.add_argument("--start", type=float, help="Start time for cutting the bag (in seconds).")
    parser.add_argument("--end", type=float, help="End time for cutting the bag (in seconds).")
    parser.add_argument("--restamp", action="store_true", help="Include the restamping step in the process.")

    args = parser.parse_args()

    # Pass restamp as True if --restamp is specified
    process_bag(args.input_bag_folder, args.output, args.topics, args.duration, args.start, args.end, restamp=args.restamp)
