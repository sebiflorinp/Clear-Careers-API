import jwt


def extract_jwt_token(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION').split(" ")
    if authorization_header[0].lower() == 'bearer':
        return authorization_header[1]


def get_user_id_from_request(request):
    token = extract_jwt_token(request)
    user_id = jwt.decode(token, options={'verify_signature': False}, algorithms=["HS256"])['user_id']
    return user_id

