<img src="https://avatars2.githubusercontent.com/u/13437736?v=3&s=200" width="50px"> [![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://proversity.org)

# Bibblio API Python
Python wrapper of Bibblio API

Register in [Bibblio](bibblio.org) and get your CLIENT_ID and CLIENT_SECRET

## Install
```pip install bibbliothon```

## Configuration
```python
import bibbliothon
```

set client_id and client_secret

```python
bibbliothon.client_id = 'YOUR_CLIENT_ID'
```

```python
bibbliothon.client_secret = 'YOUR_CLIENT_SECRET'
```

get access_token

```python
bibbliothon.access_token = bibblio.Token.get_access_token()['access_token']
```

* the access token has a duration of 5 minutes, remember to update it.

## Usage

For more information use [Bibblio API Documentation](http://docs.bibblio.apiary.io/)
* payload is always a dict
* limit and page are optional and integers
* text is a string
* content_item_id is a string

### Discovery

```python
response = bibbliothon.Discovery.content_recommendations(content_item_id)
```

```python (Legacy)
response = bibbliothon.Discovery.recommendations(payload)
```

### Enrichment

```python
response = bibbliothon.Enrichment.create_content_item(payload)
```

```python
response = bibbliothon.Enrichment.get_content_items(limit=10, page=1)
```

```python
response = bibbliothon.Enrichment.get_content_item(content_item_id)
```

```python
response = bibbliothon.Enrichment.update_content_item(content_item_id, payload)
```

```python
response = bibbliothon.Enrichment.delete_content_item(content_item_id)
```

```python (Legacy)
response = bibbliothon.Enrichment.metadata(text)
```



