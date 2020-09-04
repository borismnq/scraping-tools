
# Run Scraping tools project

1. In `docker-compose.yml` file, update `FB_EMAIL` and `FB_PASS` values with your respective facebook credentials

2. `$ docker-compose build`

3. `$ docker-compose up`

---

# Endpoints requests examples

## Instagram

`data = {'users':['claroperu']}`
`requests.post(url='http://127.0.0.1:8000/api/instagram/',data=json.dumps(data))`

## Elpais

`requests.post(url='http://127.0.0.1:8000/api/elpais/')`

## Facebook

`requests.post(url='http://127.0.0.1:8000/api/facebook/')`

---

# Helpers

- To run default tests:
`$ docker-compose run scrap_tools sh -c "python manage.py test"`

- To apply black codeformatter:
`$ docker-compose run scrap_tools sh -c "python black ./"`
