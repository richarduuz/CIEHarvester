# CIEHarvester

## Requirements

* Docker 19.3.x (for containerization)
* Docker-compose  1.27.4

## Containerisation 

Download the `docker-compose.yml` file

Run the `docker-compose.yml` file via

```bash
docker-compose up
```



## Test

Make HTTP GET request to `your ipaddress:5000/test` via

```bash
curl <your ipaddress>:5000/test
```

if you get json like the one below, then you succeed

```bash
{"status":"Just for test"}
```

## Visit

Go to the `<your ipaddress>:8080`, you will see the homepage

## Progress

* ~~Primitive login system~~
* ~~yunhan~~
* ~~ICKEY~~
* ~~TI~~
* More platforms
* Improve sustainability