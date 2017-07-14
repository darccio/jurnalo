from graphene_django import DjangoObjectType
from jurnalo.models import Record as RecordModel
import graphene


class Record(DjangoObjectType):
    class Meta:
        model = RecordModel


class Query(graphene.ObjectType):
    records = graphene.List(Record)

    def resolve_records(self, args, context, info):
        return RecordModel.objects.all()


schema = graphene.Schema(query=Query)

