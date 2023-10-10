#!/bin/bash

# Remove any previously generated coverage data
coverage erase

# Run the Django tests using coverage
coverage run --source='.' manage.py test

# Display a brief summary in the terminal
coverage report
