# Bash script for quickly checking files in a directory are dulicates or not based on md5sum.
# Good for what I needed at the time - checking over 1k+ .bin files from Immo's
# Create an array of checksums and files
declare -A checksums
declare -a files

# Loop through each file in the directory
for file in *; do
  # Skip directories
  if [[ -d $file ]]; then
    continue
  fi

  # Calculate the checksum of the file
  checksum=$(md5sum "$file" | awk '{ print $1 }')

  # Check if the checksum has already been added to the array
  if [[ ${checksums[$checksum]} ]]; then
    # If it has, print the name of the file that has a duplicate checksum
    echo -e "\e[31mDup found:\e[0m /$file \e[36m>>>>>\e[0m /${checksums[$checksum]}"
    echo "$checksum Duplicate checksum: $file <<and>> ${checksums[$checksum]}" >> duplicatefiles.txt
  else
    # If it hasn't, add the checksum to the array with the filename as the value
    checksums[$checksum]=$file
    files+=("$file")
  fi
done
sort -k1,1 duplicatefiles.txt -o duplicatefiles.txt
