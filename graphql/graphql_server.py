import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Calcul:
    a: int
    b: int

    @strawberry.field
    def somme(self) -> int:
        return self.a + self.b

    @strawberry.field
    def produit(self) -> int:
        return self.a * self.b


@strawberry.type
class Query:
    @strawberry.field
    def calcul(self, a: int, b: int) -> Calcul:
        return Calcul(a=a, b=b)


schema = strawberry.Schema(query=Query)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
