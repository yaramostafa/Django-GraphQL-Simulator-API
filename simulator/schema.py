import graphene
from graphene_django.types import DjangoObjectType
from .models import Simulator

class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = "__all__"


# For the Query (to list all my created simulators)
class Query(graphene.ObjectType):
    all_simulators = graphene.List(SimulatorType)
    simulator_by_id = graphene.Field(SimulatorType, id=graphene.Int(required=True))

    def resolve_all_simulators(root, info):
        return Simulator.objects.all()
    
    def resolve_simulator_by_id(root, info, id):
        return Simulator.objects.get(pk=id)


# Mutation to create a simulator
class CreateSimulator(graphene.Mutation):
    class Arguments:
        start_date = graphene.DateTime(required=True)
        interval = graphene.String(required=True)
        kpi_id = graphene.Int(required=True)
    
    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, start_date, interval, kpi_id):
        simulator = Simulator(start_date=start_date, interval=interval, kpi_id=kpi_id)
        simulator.save()
        return CreateSimulator(simulator=simulator)

# Mutation to update my simulators
class UpdateSimulator(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        start_date = graphene.DateTime()
        interval = graphene.String()
        kpi_id = graphene.Int()
    
    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, id, start_date=None, interval=None, kpi_id=None):
        simulator = Simulator.objects.get(pk=id)
        if start_date:
            simulator.start_date = start_date
        if interval:
            simulator.interval = interval
        if kpi_id:
            simulator.kpi_id = kpi_id
        simulator.save()
        return UpdateSimulator(simulator=simulator)

# Mutation to delete a simulator
class DeleteSimulator(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            simulator = Simulator.objects.get(pk=id)
            simulator.delete()
            return DeleteSimulator(success=True)
        except Simulator.DoesNotExist:
            return DeleteSimulator(success=False)


# Root for the Mutations
class Mutation(graphene.ObjectType):
    create_simulator = CreateSimulator.Field()
    update_simulator = UpdateSimulator.Field()
    delete_simulator = DeleteSimulator.Field()


# Final Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
