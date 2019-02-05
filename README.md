<p align="center"><img src="https://github.com/swiftype/swiftype-app-search-python/blob/master/logo-app-search.png?raw=true" alt="Elastic App Search Logo"></p>

<p align="center"><a href="https://circleci.com/gh/swiftype/swiftype-app-search-python"><img src="https://circleci.com/gh/swiftype/swiftype-app-search-python.svg?style=svg" alt="CircleCI buidl"></a>
<a href="https://github.com/swiftype/swiftype-app-search-python/releases"><img src="https://img.shields.io/github/release/swiftype/swiftype-app-search-python/all.svg?style=flat-square" alt="GitHub release" /></a></p>

> A first-party Python client for building excellent, relevant search experiences with [Elastic App Search](https://www.elastic.co/cloud/app-search-service).

## Contents

+ [Getting started](#getting-started-)
+ [Dependencies](#dependencies)
+ [Usage](#usage)
+ [Running tests](#running-tests)
+ [FAQ](#faq-)
+ [Contribute](#contribute-)
+ [License](#license-)

***

## Getting started 🐣

To install the client, use pip:

```python
python -m pip install swiftype_app_search
```

You can also download the project source and run::

```python
python setup.py install
```

## Dependencies

+ Python 2.7 / Python 3.3
+ [Requests](https://github.com/requests/requests)
+ [PyJWT](https://github.com/jpadilla/pyjwt)

## Usage

### Instantiating a client

```python
>>> from swiftype_app_search import Client
>>> host_identifier = 'host-c5s2mj'
>>> api_key = 'private-mu75psc5egt9ppzuycnc2mc3'
>>> client = Client(host_identifier, api_key)
```

### Using with App Search Managed Deploys

The client can be configured to use a managed deploy by adjusting the `base_endpoint` and `use_https` parameters. Since managed deploys do not rely on a `host_identifier`, it can be omitted.

```python
>>> from swiftype_app_search import Client
>>> client = Client(api_key='private-mu75psc5egt9ppzuycnc2mc3', base_endpoint='localhost:3002/api/as/v1', use_https=False)
```

### Index multiple document

```python
>>> engine_name = 'favorite-videos'
>>> document = {
      'id': 'INscMGmhmX4',
      'url': 'https://www.youtube.com/watch?v=INscMGmhmX4',
      'title': 'The Original Grumpy Cat',
      'body': 'A wonderful video of a magnificent cat.'
    }
>>> client.index_document(engine_name, document)
{'id': 'INscMGmhmX4'}
```

### Index documents

```python
>>> engine_name = 'favorite-videos'
>>> documents = [
    {
      'id': 'INscMGmhmX4',
      'url': 'https://www.youtube.com/watch?v=INscMGmhmX4',
      'title': 'The Original Grumpy Cat',
      'body': 'A wonderful video of a magnificent cat.'
    },
    {
      'id': 'JNDFojsd02',
      'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
      'title': 'Another Grumpy Cat',
      'body': 'A great video of another cool cat.'
    }
]

>>> client.index_documents(engine_name, documents)
[{'id': 'INscMGmhmX4', 'errors': []}, {'id': 'JNDFojsd02', 'errors': []}]
```

### Indexing: Updating documents (Partial Updates)

```python
>>> engine_name = 'favorite-videos'
>>> documents = [
    {
      'id': 'INscMGmhmX4',
      'title': 'Updated title'
    }
]

>>> client.update_documents(engine_name, documents)
```

### Get Documents

```python
>>> engine_name = 'favorite-videos'
>>> client.get_documents(engine_name, ['INscMGmhmX4'])
[{'id': 'INscMGmhmX4','url': 'https://www.youtube.com/watch?v=INscMGmhmX4','title': 'The Original Grumpy Cat','body': 'A wonderful video of a magnificent cat.'}]
```

### List Documents
```python
>>> engine_name = 'favorite-videos'
>>> client.list_documents(engine_name, current=1, size=20)
{
    'meta': {
        'page': {
        'current': 1,
        'total_pages': 1,
        'total_results': 2,
        'size': 20
        }
    },
    'results': [{'id': 'INscMGmhmX4','url': 'https://www.youtube.com/watch?v=INscMGmhmX4','title': 'The Original Grumpy Cat','body': 'A wonderful video of a magnificent cat.'}]
}
```

### Destroy Documents

```python
>>> engine_name = 'favorite-videos'
>>> client.destroy_documents(engine_name, ['INscMGmhmX4'])
[{'id': 'INscMGmhmX4','result': True}]
```

### List Engines

```python
>>> client.list_engines(current=1, size=20)
{
    'meta': {
        'page': {
        'current': 1,
        'total_pages': 1,
        'total_results': 2,
        'size': 20
        }
    },
    'results': [{'name': 'favorite-videos'}, {'name': 'another-engine'}]
}
```

### Get an Engine

```python
>>> client.get_engine('favorite-videos')
{'name': 'favorite-videos'}
```

### Create an Engine

```python
>>> client.create_engine('favorite-videos', 'en')
{'name': 'favorite-videos', 'type': 'default', 'language': 'en'}
```

### Destroy an Engine

```python
>>> client.destroy_engine('favorite-videos')
{'deleted': True}
```

### Running search

```python
>>> client.search('favorite-videos', 'grumpy cat', {})
{'meta': {'page': {'current': 1, 'total_pages': 1, 'total_results': 2, 'size': 10}, ...}, 'results': [...]}
```

### Multi-Search

```python
>>> client.multi_search('favorite-videos', [{
  'query': 'cat',
  'options': { 'search_fields': { 'title': {} }}
},{
  'query': 'dog',
  'options': { 'search_fields': { 'body': {} }}
}])
[{'meta': {...}, 'results': [...]}, {'meta': {...}, 'results': [...]}]
```

### Query Suggestion

```python
>>> client.query_suggestion('favorite-videos', 'cat', {
  'size': 10,
  'types': {
    'documents': {
      'fields': ['title']
    }
  }
})
{'results': {'documents': [{'suggestion': 'cat'}]}, 'meta': {'request_id': '390be384ad5888353e1b32adcfaaf1c9'}}
```

### Clickthrough Tracking

```python
>>> client.click(engine_name, {'query': 'cat', 'document_id': 'INscMGmhmX4'})
```


### Create a Signed Search Key

Creating a search key that will only search over the body field.

```python
>>> api_key = 'private-mu75psc5egt9ppzuycnc2mc3'
>>> api_key_name = 'my-api-token'
>>> signed_search_key = Client.create_signed_search_key(api_key, api_key_name, {'search_fields': { 'body': {}}})
>>> client = Client(host_identifier, signed_search_key)
```

## Running tests

```python
python setup.py test
```

## FAQ 🔮

### Where do I report issues with the client?

If something is not working as expected, please open an [issue](https://github.com/swiftype/swiftype-app-search-python/issues/new).

### Where can I learn more about App Search?

Your best bet is to read the [documentation](https://swiftype.com/documentation/app-search).

### Where else can I go to get help?

You can checkout the [Elastic App Search community discuss forums](https://discuss.elastic.co/c/app-search).

## Contribute 🚀

We welcome contributors to the project. Before you begin, a couple notes...

+ Prior to opening a pull request, please create an issue to [discuss the scope of your proposal](https://github.com/swiftype/swiftype-app-search-python/issues).
+ Please write simple code and concise documentation, when appropriate.

## License 📗

[MIT](https://github.com/swiftype/swiftype-app-search-python/blob/master/LICENSE.txt) © [Elastic](https://github.com/elastic)

Thank you to all the [contributors](https://github.com/swiftype/swiftype-app-search-python/graphs/contributors)!
