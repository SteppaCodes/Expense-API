# echo "BUILD START"
# python3.9 -m pip install -r requirements.txt
# python3.9 manage.py migrate
# python3.9 manage.py collectstatic --noinput --clear
# echo "BUILD END"

echo "BUILD START"
{
  "installCommand": "npm install && python3 -m pip install -r requirements.txt && pip install urllib3<2 && python3 -m pip install -e .",
  "buildCommand": "npm run build && python3 -m sphinx -M html docs/ _build",
  "outputDirectory": "_build/html",
  "github": {
    "silent": true
  }
}

echo "BUILD END"