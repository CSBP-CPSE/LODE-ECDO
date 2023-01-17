# Scrapy for Fire Departments

## Documentation

- [https://docs.scrapy.org/en/latest/intro/tutorial.html](https://docs.scrapy.org/en/latest/intro/tutorial.html)

## How to use

To scrape all of Canada:
``` 
$ scrapy crawl fire -O fire_scrape_canada.json
```
_TODO_: Scrape categories selecitvely, by command-line parameters

## Statistics

```
 'downloader/request_bytes': 3163576,
 'downloader/request_count': 5751,
 'downloader/request_method_count/GET': 5751,
 'downloader/response_bytes': 758263825,
 'downloader/response_count': 5751,
 'downloader/response_status_count/200': 5746,
 'downloader/response_status_count/301': 1,
 'downloader/response_status_count/404': 4,
 'dupefilter/filtered': 797,
 'elapsed_time_seconds': 191.880243
```
