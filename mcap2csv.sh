#!/bin/bash

# Check if a bag name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <BAGNAME>"
    exit 1
fi

BAGNAME="$1"
BAGNAME="$(realpath "${BAGNAME}")"

GPS_DB3="${BAGNAME}_gps_sqlite3"
# Run the first script
python3 $HOME/code/bags/utils/extract_gps_tmp.py "$BAGNAME"

# Run the second script and automatically respond with 'n'
echo $GPS_DB3
cd $HOME/bag_parser/bag_parser/
echo "n" | python3 bag_parser_2.py "$GPS_DB3"

mv $GPS_DB3/Parsed_Data $BAGNAME
rm -r $GPS_DB3