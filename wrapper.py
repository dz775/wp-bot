from functools import wraps

def with_language(func):
    @wraps(func)
    def wrapper(client, clb):
        dest = session_context.get(clb.from_user.wa_id, 'en')
        return func(client, clb, dest)
    return wrapper

# @with_language
# def a(client: WhatsApp, clb: CallbackButton, dest: str):
#     # Use dest variable in function 'a'

# @with_language
# def b(client: WhatsApp, clb: CallbackButton, dest: str):
#     # Use dest variable in function 'b'
