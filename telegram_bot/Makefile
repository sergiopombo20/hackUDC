# Display available commands
help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies from requirements.txt"
	@echo "  make run      - Launch the Telegram bot (bot.py)"
	@echo "  make clean    - Remove temporary files and venv"
#	@echo "  make test     - Run tests (pytest)"
#	@echo "  make lint     - Run linter (flake8)"

.DEFAULT_GOAL := run

# Run the bot
run: install
	venv/bin/python bot.py

# Install dependencies
install: check-conf
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

# Check for bot.conf file
check-conf:
	@test -f bot.conf || (echo "Error: bot.conf file does not exist. Please create it (cp bot.conf.sample bot.conf) and populate vars." && exit 1)

# Clean temporary files and caches
clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -rf venv

# Lint the code using flake8
# lint:
#	flake8 .

# Run tests with pytest
# test:
#	pytest
