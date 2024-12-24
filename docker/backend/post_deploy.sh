#! /bin/sh

set -e
set -u
set -x

# Create logs folder if it does not exists
mkdir -p logs

# Wait for DB
dockerize -wait tcp://postgres:"${POSTGRES_INTERNAL_PORT}" -timeout 30s

umask 000 # setting broad permissions to share log volume

# Migrate models
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

# Collect static files to serve them with nginx
python3 manage.py collectstatic --no-input

# Create the superuser for the platform
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model();User.objects.filter(email='${SUPERUSER_MAIL}').exists() or User.objects.create_superuser('${SUPERUSER_MAIL}', '${SUPERUSER_PASSWORD}')"

# Load fixtures
python3 manage.py loaddata apps/questions/fixtures/categories.json
python3 manage.py loaddata apps/questions/fixtures/levels.json
python3 manage.py loaddata apps/questions/fixtures/questions.json
python3 manage.py loaddata apps/questions/fixtures/question_level_categories.json

# Set the number of Django threads to use
num_threads=${DJANGO_THREADS}

# Start the gunicorn server
/usr/local/bin/gunicorn backend.wsgi:application --workers "${num_threads}" --bind :"${BACKEND_PORT}" --timeout "$CONF_GUNICORN_TIMEOUT" "$CONF_GUNICORN_EXTRA_ARGS"
