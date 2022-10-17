from rest_framework import serializers
from .models import Animal, SexChoices
from groups.models import Group
from traits.models import Trait
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    sex = serializers.ChoiceField(choices=SexChoices.choices, default=SexChoices.Default)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
   
    def create(self, obj: dict) -> None:
        group = obj.pop('group')
        traits = obj.pop('traits')
        group = Group.objects.get_or_create(**group)[0]
        for i in range(len(traits)):
            traits[i] = Trait.objects.get_or_create(**traits[i])[0]
        animal = Animal.objects.create(**obj, group=group)
        animal.traits.set(traits)
        animal.save()

        return animal

    def update(self, instance: Animal, validaded_data: dict) -> None:
        keys_for_update = validaded_data.keys()
        errors = []
        for key in ['sex', 'group', 'traits']:
            if key in keys_for_update:
                message = {str(key): f'You can not update {key} property.'}
                errors.append(message)
        for attr, val in validaded_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance