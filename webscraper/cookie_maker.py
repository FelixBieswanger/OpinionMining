def create_cookie_string(cookies):
    cookie_string = ""


    for name in cookies.keys():
        cookie_string += name
        cookie_string += "="
        cookie_string += cookies[name]
        cookie_string += ";"

    cookie_string = cookie_string[:-2]  

    return cookie_string
