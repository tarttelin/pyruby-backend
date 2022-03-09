from firebase_admin import auth
import firebase_admin
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path, \
    snake_case_fallback_resolvers, SchemaDirectiveVisitor
from ariadne.asgi import GraphQL
from graphql.type.definition import GraphQLField, GraphQLObjectType, GraphQLInterfaceType, GraphQLError
from graphql import default_field_resolver
from typing import Union
from starlette.applications import Starlette
from starlette.requests import Request
from pathlib import Path
from .user_resolvers import register_resolvers

sdl_dir = Path(__file__).parent.parent / "sdl"
type_defs = load_schema_from_path(sdl_dir)

query = QueryType()
mutation = MutationType()

firebase_admin.initialize_app(options={'projectId': 'pyruby-web-home'})

object_types = register_resolvers(query, mutation)


def get_context_value(request: Request):
    token = request.headers.get("authorization", None)
    if token is not None:
        user = auth.verify_id_token(token.split(' ')[1])
    else:
        user = {'name': 'Anon'}
    return {'request': request, 'user': user}


class HasRoleDirective(SchemaDirectiveVisitor):
    def visit_field_definition(
            self,
            field: GraphQLField,
            object_type: Union[GraphQLObjectType, GraphQLInterfaceType],
    ) -> GraphQLField:
        roles = self.args.get("roles")
        original_resolver = field.resolve or default_field_resolver

        def resolve_has_permissions(obj, info, **kwargs):
            if not info.context['user']['role'] in roles:
                raise GraphQLError("User does not have the right permissions")
            else:
                return original_resolver(obj, info, **kwargs)

        field.resolve = resolve_has_permissions
        return field


schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers, *object_types,
                                directives={"hasAuth": HasRoleDirective})

app = Starlette(debug=True)
app.mount("/graphql", GraphQL(schema, context_value=get_context_value, debug=True))
