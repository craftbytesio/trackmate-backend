from datetime import datetime, timedelta
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum, Avg
from graphql_jwt.decorators import login_required

from .models import Track


class TrackType(DjangoObjectType):
    class Meta:
        model = Track
        fields = ('id', 'date', 'user', 'distance_m')


class StatisticType(graphene.ObjectType):
    count = graphene.Int()
    weekly_count = graphene.Int()
    sum = graphene.Float()
    avg = graphene.Float()


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)
    sanity_check = graphene.Field(TrackType)
    track_statistics = graphene.Field(StatisticType)

    @login_required
    def resolve_tracks(self, info):
        user = info.context.user
        return Track.objects.filter(user=user)

    @login_required
    def resolve_sanity_check(self, info):
        user = info.context.user
        return Track.objects.filter(user=user)[0]

    @login_required
    def resolve_track_statistics(self, info):
        statistics = StatisticType()
        user = info.context.user

        user_tracks = Track.objects.filter(user=user)

        dt = datetime.now()

        start_week = dt - timedelta(days=dt.weekday())
        end_week = start_week + timedelta(days=6)

        weekly_tracks = user_tracks.filter(
            date__range=[start_week, end_week]
        )

        sum_tracks = user_tracks.aggregate(Sum('distance_m'))['distance_m__sum']

        if sum_tracks:
            statistics.sum = sum_tracks
        else:
            statistics.sum = 0

        statistics.count = user_tracks.count()

        statistics.weekly_count = weekly_tracks.count()

        avg = user_tracks.aggregate(Avg('distance_m'))['distance_m__avg']

        if avg:
            statistics.avg = round(avg)
        else:
            statistics.avg = 0

        return statistics


class CreateTrackMutation(graphene.Mutation):
    class Arguments:
        distance_m = graphene.Int(required=True)
        assessment = graphene.Int(required=True)
        date = graphene.Date(required=True)

    track = graphene.Field(TrackType)

    @classmethod
    def mutate(cls, root, info, distance_m, assessment, date):
        track = Track.objects.create(
            distance_m=distance_m,
            date=date,
            assessment=assessment,
            user=info.context.user,
        )
        track.save()
        return CreateTrackMutation(track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrackMutation.Field()
