import requests


def StopForumSpamAdd(username, email, ip, evidence):
    data = {"username": username, "email": email, "ip_addr": ip, "api_key": "dejcsw8ph7iu5n", "evidence": evidence}
    requests.post("http://www.stopforumspam.com/add", data)
