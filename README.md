[![Build Status](https://travis-ci.org/iress/iress-xplan-api-examples.svg?branch=master)](https://travis-ci.org/iress/iress-xplan-api-examples)

# Example Connecting to Iress Xplan RAPI and EDAI
A sample project to demonstrate how backend applications can use basic authentication with Iress Xplan Resourceful API 
and EDAI. This also includes sample code that uses Two Factor Authentication (2FA).

_**Note:** 2FA for the user must use the `Software Token` method._

## Pre-requisites
- [Devbox](https://www.jetify.com/devbox)

Please see `pyproject.toml` for the Python dependencies.

## Setup
```bash
devbox run install
```

## Usage
To view the current usage/help please run:

```bash
devbox run help
```

Or directly:
```bash
python3 src/call.py -h
```

#### Examples

##### RAPI using 2FA
```bash
devbox run call -b https://dev.xplan.iress.com.au -u testuser -p ASDDsf3sdsf2 -o HTHHH72MQ7CBVX3SU25YRKQO6OAI36TD -i FPj9cymketaHXunJE3E3 -tfa -api
```

##### EDAI using 2FA
```bash
devbox run call -b https://dev.xplan.iress.com.au -u testuser -p ASDDsf3sdsf2 -o HTHHH72MQ7CBVX3SU25YRKQO6OAI36TD -i FPj9cymketaHXunJE3E3 -tfa -edai
```

_**Note:**_
 - If you don't specify a password using the `-p` option the script will prompt for the password
 - If you don't specify an OTP Secret using the `-o` option the script will prompt for the secret

## Development
Available commands:
- `devbox run test` - Run tests
- `devbox run lint` - Run linting
- `devbox run format` - Format code
- `devbox run upgrade` - Upgrade dependencies

**Sample result of the above script:**
```
[
    {
        "bookmark": "eyJpZCI6MTI1OX0=",
        "id": 1259,
        "entity_name": "Portfolio Superfund"
    },
    {
        "bookmark": "eyJpZCI6MTQwNn0=",
        "id": 1406,
        "entity_name": "Portfolio Company Pty Ltd"
    },
    {
        "bookmark": "eyJpZCI6MTQwN30=",
        "id": 1407,
        "entity_name": "Portfolio Trust"
    }
]
```

## 2FA Technical Details
[Please see](2FA_TECHNICAL_DOC.md)

## EDAI Authentication Using RAPI
[Please see](EDAI_RAPI_AUTH.md)

## Licence
MIT License (See the included [Licence](LICENSE) file for more information).
