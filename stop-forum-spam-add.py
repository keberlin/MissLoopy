import requests

api_key = "dejcsw8ph7iu5n"

data = {
    "username": "username",
    "email": "email@server.com",
    "ip_addr": "111.111.111.111",
    "api_key": api_key,
    "evidence": "evidence",
}
requests.post("http://http://www.stopforumspam.com/add", data)
