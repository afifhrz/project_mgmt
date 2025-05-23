# How to setup
1. `python -m virtenv virtenv`
2. activate virtual env
3. `pip install -r requirements.txt`
4. setup database
5. `python manage.py migrate`
6. run seeding `python .\manage.py loaddata auth trial-data`

# Dump Data
run this command
```
cd seeding
python ..\manage.py dumpdata auth -o auth.json
python ..\manage.py dumpdata --exclude=auth --exclude=sessions -o trial-data.json
```

# Remove All Data
`python manage.py flush`
