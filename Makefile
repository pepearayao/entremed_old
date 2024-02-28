# Makefile to delete build and project.egg-info directories

# Define the directories containing the folders to delete
ENTREMED_DIR := entremed_scrapper

# Define the directories to delete
DIRS_TO_DELETE := $(ENTREMED_DIR)/build $(ENTREMED_DIR)/project.egg-info $(ENTREMED_DIR)/twistd.pid $(ENTREMED_DIR)/entremed/scrapyd/ $(ENTREMED_DIR)/entremed.egg

# Define phony targets
.PHONY: clean_scrappy_egg

# Define the default target
clean_scrapy_egg:
	@echo "Deleting directories: $(DIRS_TO_DELETE)"
	@rm -rf $(DIRS_TO_DELETE)
	@echo "Cleanup complete!"

build_docker:
	@echo "Dockerizing"
	@docker compose up -d --build

build_compose: clean_scrapy_egg build_docker

down_compose:
	@docker compose down

upload_stack_compose:
	@echo "Uploading...."
	@scp compose-prod.yml ubuntu@3.75.123.154:.
	@scp secrets_generator.py ubuntu@3.75.123.154:.
	@scp Makefile ubuntu@3.75.123.154:.
	@scp -r visualizer/ ubuntu@3.75.123.154:.
	@echo "Done."
