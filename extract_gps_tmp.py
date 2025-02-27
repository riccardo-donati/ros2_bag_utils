import argparse
import subprocess
import os

def create_out_yaml(output_bag_folder, storage_id):
    yaml_content = f"""output_bags:
- uri: {output_bag_folder}
  storage_id: {storage_id}
  topics: [
  /novatel_bottom/bestgnsspos,
  /novatel_bottom/bestpos, 
  /novatel_bottom/bestvel,
  /novatel_bottom/heading2,
  /novatel_bottom/rawimu,
  /novatel_bottom/time,
  /novatel_bottom/oem7raw,
  /novatel_top/bestgnsspos,
  /novatel_top/bestvel,
  /novatel_top/heading2,
  /novatel_top/rawimu,
  /novatel_top/time,
  /novatel_top/oem7raw,
  /novatel_top/bestpos,
  /vectornav/raw/common,
  /vectornav/raw/gps,
  /vectornav/raw/gps2  
] 
"""
    with open("out.yaml", "w") as yaml_file:
        yaml_file.write(yaml_content)

def convert_bag(input_bag_folder, storage_id):
    # Normalize the input path to remove any trailing slashes
    input_bag_folder = os.path.normpath(input_bag_folder)

    # Convert input path to absolute path
    input_bag_folder = os.path.abspath(input_bag_folder)

    # Generate the output folder name by appending '_gps' to the input folder name
    output_bag_folder = input_bag_folder + "_gps_"+str(storage_id)

    # Create the out.yaml file
    create_out_yaml(output_bag_folder, storage_id)

    try:
        # Run the ros2 bag convert command
        command = ["ros2", "bag", "convert", "-i", input_bag_folder, "-o", "out.yaml"]
        subprocess.run(command, check=True)

        print(f"Conversion complete. Output bag folder: {output_bag_folder}")
    finally:
        # Remove the out.yaml file after conversion
        if os.path.exists("out.yaml"):
            os.remove("out.yaml")
            print("Removed out.yaml file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a ROS 2 bag folder to a specified storage format.")
    parser.add_argument("input_bag_folder", type=str, help="Path to the input bag folder.")
    parser.add_argument("--storage", type=str, default="sqlite3", help="Storage ID for the output bag (e.g., sqlite3, mcap).")

    args = parser.parse_args()

    convert_bag(args.input_bag_folder, args.storage)
