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

Go to the `<your ipaddress>:8080`, you will see the homepage.

Click the 开始使用

Input the password ysy1001, the website will jump the the search page

Input the chip model number, wait for about 30 seconds, results will pop up. 

## Progress

* ~~Primitive login system~~
* ~~yunhan~~
* ~~ICKEY~~
* ~~TI~~
* ~~Adjust password input interfact~~
* More platforms
  * Digikey
* Improve sustainability
* Function
  * Export Excel
  * Import Excel

