
# DesmosPics 
Turn your picture into Desmos graphs.

## Special Thanks to
- The source code that turns picture into series of Desmos graphs were achieved by [kevinjycui](https://github.com/kevinjycui) in his project [DesmosBezierRenderer](https://github.com/kevinjycui/DesmosBezierRenderer).
- [Desmos](https://desmos.com/) themselves! Needed to modify their official API's javascript code a bit in order to make this thing working.

## What is this?
This is a website (or API at the same time) that turns your picture into Desmos Graphs. 

![enter image description here](https://raw.githubusercontent.com/gooday2die/DesmosPic/main/frontend/intro.png)

Please check https://gooday2die.net/DesmosPics or http://us.gooday2die.net/DesmosPics for live demo!

## Includes...
- `backend.py` : A Python script that includes all codes for API. 
- `/frontend/` : All elements for frontend web page.

## Installation
### A. Native
1. Simply put  `/frontend` directory into your Apache directory
2. `sudo apt install git python3-dev python3-pip build-essential libagg-dev libpotrace-dev pkg-config`
3. If you do not have PHP and CURL PHP not installed in your system, install them.
4. Install all requirements in `requirements.txt` by `pip install -r requirements.txt`
5. Edit graph saving location using at following files
- 1. `backend.py` at line 155. 
- 2. `index.php` at line 136
6. `python3 backend.py`

### B. Docker
![enter image description here](https://img.shields.io/docker/pulls/isukim/desmos_pic)

DesmosPics supports Docker. You can simply pull the image by
```
docker pull isukim/desmos_pics
```
Then execute the image using
```
docker run -d -p 8080:80 isukim/desmos_pics 
```
This will make the container run web server on port 8080. Also, if you would like to use API as well, use `5001` for the container's  API port.
> For example, if you would like to use `8080` in local host for the web server and `8081` for the API server, use following command:
> ```
> docker run -d -p 8080:80 -p 8081:5001 isukim/desmos_pics
> ```


## Limits
- When the picture needs many functions to be rendered, Desmos API needs very much time to render graphs.

## API
By `python3 backend.py` there will be an API server running in port `5001`. The API has following services.

### Endpoints
- `/pic`
- Method: `POST` and `GET`

#### POST
Post a `png`, `jpeg`, `jpg` image document using `enctype=multipart/form-data`. Send data in following format.
```
{"image": ImageData}
```
If the API server was able to process the image, it will return following `json` as return value.
```
{
	"js_result": "string object that represents javascript code that is needed for representing Desmos graph using their API",
	"text_result": "string object that represents latex expression that represents all functions needed for representing the image"
}
```

## More info
- `./frontend/modified.js` was a modified version of official Desmos API. Since there was abit of minor bug from the original API which can be found [here](https://www.desmos.com/api/v1.7/docs/index.html?lang=ko), I had to modify a bit of code in order for the frontend script to work.


## PRs and Issues
I am not a web programmer, so if you happen to find bugs in frontend or backend, please PR or report issues. 
