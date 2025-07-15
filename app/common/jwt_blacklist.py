BLACKLIST = set()

def is_token_revoked(jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST