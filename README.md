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
### Example answer:
```JSON
{
    "status": "passed",
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
            "time": 0
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
