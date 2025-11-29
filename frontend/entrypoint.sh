#!/bin/sh

# Define the directory containing the HTML files
HTML_DIR="/srv"

# Backup the original files (optional)
for file in $HTML_DIR/*.html; do
    cp "$file" "$file.bak"
done

# Iterate through all environment variables
for var in $(env | grep '^APP_'); do
    # Extract the variable name and value
    VAR_NAME=$(echo "$var" | cut -d'=' -f1)
    VAR_VALUE=$(echo "$var" | cut -d'=' -f2-)

    # Convert VAR_NAME into the format %VARNAME%
    PLACEHOLDER="%${VAR_NAME}%"

    # Replace %VARNAME% in all HTML files with the actual value
    for file in $HTML_DIR/*.html; do
        sed -i "s|${PLACEHOLDER}|${VAR_VALUE}|g" "$file"
    done

done

# Execute the CMD passed to the container
echo "Now running $@"
exec "$@"
