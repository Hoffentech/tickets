git add *
git stash
git clean -d -f
git pull origin staging
pip install --no-cache-dir -r requirements.txt
cd hit
python manage.py migrate
python manage.py collectstatic --noinput --clear
exit