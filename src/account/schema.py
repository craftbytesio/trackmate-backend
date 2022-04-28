import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(root, info, **kwargs):
        user = info.context.user
        return User.objects.get(username=user)


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, email, password):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        return CreateUserMutation(user=user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUserMutation.Field()
