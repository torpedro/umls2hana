#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo $DIR
CONFIG_FILE=${DIR}/config.sh
# check the config file
if [ ! -f ${CONFIG_FILE} ]; then
	echo "Config file 'config.sh' could not be found!"
	echo "Plese copy 'sample.config.sh' to 'config.sh' and change the values according to your installation."
	exit
fi

source ${CONFIG_FILE}

# check if it's a HANA user
if [ `expr "$USER" : '.*adm$'` -eq 0 ]; then
	echo "This script should only be executed by a <>adm user."
	exit
fi


# check & read user input
if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ./hana-compile.sh input_xml [output_dict_filename]"
    exit
fi

INPUT_XML=$1
OUTPUT_DICT_FILENAME=$2

if [ "$#" -lt 2 ]; then
	INPUT_BASE=$(basename "$INPUT_XML")
	INPUT_FNAME="${INPUT_BASE%.*}"
	OUTPUT_DICT_FILENAME=$INPUT_FNAME.nc
fi

echo ""
echo " * Compiling xml file: ${INPUT_XML}"
echo " * Output dictionary file: ${OUTPUT_DICT_FILENAME}"

# Setup execution variables
OUTPUT_FILE=$LANG_DIR/$OUTPUT_DICT_FILENAME
CC=$DAT_BIN_DIR/tf-ncc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDB_LIB_DIR:$DAT_BIN_DIR


# If the file already exists, prompt the user for removal
# Exit if removal is denied
# Remove the previous existing dictionary
if [ -f ${OUTPUT_FILE} ]; then
	echo "$OUTPUT_DICT_FILENAME already exists."
	while [ -z $prompt ]; do 
		read -p "Remove (y/n)? " choice;
		case "$choice" in
			y|Y ) prompt=true; break;;
			n|N ) exit 0;;
		esac;
	done;
	prompt=;
	
	rm -f ${OUTPUT_FILE}	
fi

# Compile
${CC} -d ${LANG_DIR} -o ${OUTPUT_FILE} ${INPUT_XML}