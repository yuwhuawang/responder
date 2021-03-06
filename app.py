import responder
import graphene

api = responder.API()
# api.mount('/subapp', other_wsgi_app)


@api.route("/")
def hello(req, resp):
    # resp.status = responder.status.ok
    resp.media = {"hello": "world"}


class ThingsResource:
    def on_request(self, req, resp):
        resp.status = responder.status.HTTP_200
        resp.media = ["yolo"]


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


schema = graphene.Schema(query=Query)

# Alerntatively,
api.add_route("/graph", schema)


print(
    api.session()
    .get(
        "http://app/",
        data="{ hello }",
        headers={"Accept": "application/x-yaml"},
        # data="hello",
    )
    .text
)

print(
    api.session()
    .get(
        "http://app/graph",
        data="{ hello }",
        headers={"Accept": "application/x-yaml"},
        # data="hello",
    )
    .text
)
# {hello: Hello stranger}

api.run(port=5000, expose_tracebacks=True)
