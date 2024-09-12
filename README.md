# run_lang

Package `run_lang` executes code in a language.

## Request format
POST to "/"

In Body, the following fields are required:
- lang: "js" or "py" (JavaScript or Python)
- code: a string with source code of a function
- func_name: the name of the function
- tests: an array of test-objects

A test is:
- _id: optional? 
- inputs: array of objects like [{ "value": 1 }, { "value": 11 }]
- "output": the output-value, e.g. 1 or "one"

### Example request:
```JSON
## Dockerization
To build the docker image run the following:

```
docker build -t run_lang .
```

To run it:
```
docker run -p 5000:5000 --name runlang runlang:v1
```

### Example answer:
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

