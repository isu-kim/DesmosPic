# DesmosPics
Turn your picture into Desmos graphs.

## Special Thanks to
- The source code that turns picture into series of Desmos graphs were achieved by [kevinjycui](https://github.com/kevinjycui) in his project [DesmosBezierRenderer](https://github.com/kevinjycui/DesmosBezierRenderer).
- [Desmos](https://desmos.com/) themselves! Needed to modify their official API's javascript code a bit in order to make this thing working.

## What is this?
This is a website (or API at the same time) that turns your picture into Desmos Graphs. 

![enter image description here](https://raw.githubusercontent.com/gooday2die/DesmosPic/main/frontend/intro.png)

Please check https://gooday2die.net/DesmosPics for live demo!

## Includes...
- `backend.py` : A Python script that includes all codes for API. 
- `/frontend/` : All elements for frontend web page.

## Installation
1. Simply put  `/frontend` directory into your Apache directory
2. Install all requirements in `requirements.txt`
3. `python3 backend.py`

## Limits
- When the picture needs many functions to be represented, Desmos API needs very much time to render graphs.

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


## PRs and Issues
I am not a web programmer, so if you happen to find bugs in frontend or backend, please PR or report issues. 
