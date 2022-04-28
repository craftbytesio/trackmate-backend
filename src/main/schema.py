import graphene
import tracks.schema
import account.schema


class Query(
    tracks.schema.Query,
    account.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    account.schema.Mutation,
    tracks.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
