# Define shell
SHELL := /bin/bash

# Define the directories
SRC_DIR := Capstone_3/src
DATA_DIR := Capstone_3/data
RAW_DIR := $(DATA_DIR)/raw
INTERIM_DIR := $(DATA_DIR)/interim
PROCESSED_DIR := $(DATA_DIR)/processed

# Define commands
.PHONY: all data consolidate database features

all: features

data: $(RAW_DIR)/users
	python $(SRC_DIR)/data/make_data.py

consolidate: $(INTERIM_DIR)/consolidated_data.csv
	python $(SRC_DIR)/data/make_consolidated_data.py

database: $(PROCESSED_DIR)/books.db 
	python $(SRC_DIR)/data/make_database.py

features: $(SRC_DIR)/features/make_X.py database
	python $(SRC_DIR)/features/make_X.py

# Define how to check if the folders/files are updated
$(RAW_DIR)/users:
	@echo "Checking for new files in $(RAW_DIR)/users"

$(INTERIM_DIR)/consolidated_data.csv:
	@echo "Checking for new consolidated data in $(INTERIM_DIR)"

$(PROCESSED_DIR)/books.db:
	@echo "Checking for new database in $(PROCESSED_DIR)"