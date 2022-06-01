pwd
echo "listing files in root directory"
pwd
ls -a


echo "listing files in search_api directory"
cd /search_api
pwd
ls -a

echo "Running Gunicorn"
cd ..
gunicorn -b :5000 search_api.api:app