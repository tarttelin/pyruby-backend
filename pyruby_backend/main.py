from firebase_admin import auth
import firebase_admin
from ariadne import QueryType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.requests import Request
from pathlib import Path

sdl_dir = Path(__file__).parent.parent / "sdl"
type_defs = load_schema_from_path(sdl_dir)

query = QueryType()

firebase_admin.initialize_app(options={'projectId': 'pyruby-web-home'})


@query.field("hello")
def resolve_hello(_, info):
    return f"Hello {info.context['user']['name']}!"


def get_context_value(request: Request):
    token = request.headers.get("authorization", None)
    if token is not None:
        user = auth.verify_id_token(token.split(' ')[1])
    else:
        user = {'name': 'Anon'}
    return {'request': request, 'user': user}


schema = make_executable_schema(type_defs, query)

app = Starlette(debug=True)
app.mount("/graphql", GraphQL(schema, context_value=get_context_value, debug=True))
