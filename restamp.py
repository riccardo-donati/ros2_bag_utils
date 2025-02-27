import argparse
import subprocess
import os

def create_process_config(output_bag_folder, topics, duration):
    """
    Creates a process.config file with the specified commands and parameters.
    """
    config_content = f"""cut --duration {duration}
extract -t {' '.join(topics)}
restamp
"""
    with open("process.config", "w") as config_file:
        config_file.write(config_content)

def process_bag(input_bag_folder, output_bag_folder, topics, duration):
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
    create_process_config(output_bag_folder, topics, duration)

    try:
        # Run the ros2 bag process command
        command = ["ros2", "bag", "process", "-c", "process.config", input_bag_folder, "-o", output_bag_folder ]
        subprocess.run(command, check=True)

        print(f"Processing complete. Output bag folder: {output_bag_folder}")
    finally:
        # Remove the process.config file after processing
        if os.path.exists("process.config"):
            # os.remove("process.config")
            print("Removed process.config file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a ROS 2 bag folder using a process.config file.")
    parser.add_argument("input_bag_folder", type=str, help="Path to the input bag folder.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output bag folder.")
    parser.add_argument("--topics", type=str, nargs="+", required=True, help="List of topics to extract.")
    parser.add_argument("--duration", type=float, required=True, help="Duration to cut from the bag (in seconds).")

    args = parser.parse_args()

    process_bag(args.input_bag_folder, args.output, args.topics, args.duration)