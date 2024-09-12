# run_lang

Package `run_lang` executes code in a language.

## Dockerization
To build the docker image run the following:

```
docker build -t run_lang .
```

To run it:
```
docker run -p 5000:5000 --name runlang runlang:v1
```

## Example
```
POST http://localhost:5000/run
```
```json
{
    "lang": "js",
    "code": "function factorial(n) {\n    if (n === 0) return 1;\n    return n * factorial(n - 1);\n}",
    "func_name": "factorial",
    "tests": [
        {
            "_id": "1234654654654d",
            "inputs": [{ "value": 1 }],
            "output": 1
        },
        {
            "_id": "1234654654654",
            "inputs": [{ "value": 5 }],
            "output": 120
        },
        {
            "_id": "12346546544d",
            "inputs": [{ "value": 4 }],
            "output": 24
        }
    ]
}
```
An example out
```json
{
    "status": "passed",
    "message": "<message here>",
    "test_results": [
        {
            "message": "",
            "status": "passed",
            "test_id": "1234654654654d",
            "time": 4
        },
        {
            "message": "",
            "status": "passed",
            "test_id": "1234654654654",
            "time": 1
        },
        {
            "message": "",
            "status": "passed",
            "test_id": "12346546544d",
            "time": 0
        }
    ]
}
```