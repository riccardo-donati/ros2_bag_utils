#!/bin/bash

# Check if a bag name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <BAGNAME>"
    exit 1
fi

SOURCE_DIR="$1"

# Iterate over all .mcap files in the directory
for MCAP_FILE in "$SOURCE_DIR"/*.mcap; do
    # Extract filename without extension
    FILENAME=$(basename -- "$MCAP_FILE" .mcap)

    # Create folder for the file
    FOLDER="$SOURCE_DIR/$FILENAME"
    mkdir -p "$FOLDER"

    # Move and rename the .mcap file into the folder
    NEW_MCAP_FILE="${FILENAME}_0.mcap"
    mv "$MCAP_FILE" "$FOLDER/$NEW_MCAP_FILE"

    # Reindex the bag file
    echo "Reindexing: $FOLDER"
    ros2 bag reindex "$FOLDER"

    # Convert MCAP to CSV
    echo "Converting MCAP to CSV: $FOLDER"
    $HOME/code/bags/utils/mcap2csv.sh "$FOLDER"
    
    echo "Finished processing: $FOLDER"
done

echo "All .mcap files processed."
