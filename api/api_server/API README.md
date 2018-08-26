# API Server Documentation

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### Fetch level 1 quote
Fetch price and size of best bid and best ask

**Definition**

`GET /l1_quote?exchange=<exchange_name>&market=<market_ticker>`

**Response**

- `200 OK` on success
- `400 Bad Request` on failure; i.e. invalid exchange and/or market entered. Or (rarely) if the underlying exchange's API server failed

```json
{
	"best ask price": 48.89,
	"best bid size": 83.35073116,
	"timestamp": "2018-08-26 18:39:04.610506",
	"best ask size": 9.5550388,
	"best bid price": 48.88
}
```

This api server was based off of the work of Jake Wright: https://github.com/jakewright/tutorials/tree/master/home-automation/02-device-registry