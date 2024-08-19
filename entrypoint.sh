#!/bin/bash

# Initialize the database
flask db init

# Apply the migration to the database
flask db upgrade

# Start the Flask application
flask run --host=0.0.0.0 --debug