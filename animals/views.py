from rest_framework.views import APIView, Request, Response, status
from .models import Animal
from .serializers import AnimalSerializer


class AnimalView(APIView):
    def get(self, request: Request) -> None:
        animals = Animal.objects.all()

        serializer_animals = []
        for animal in animals:
            serializer_animal = AnimalSerializer(animal)
            serializer_animals.append(serializer_animal.data)

        return Response(serializer_animals, status.HTTP_200_OK)

    def post(self, request: Request) -> None:
        deserializer_animal = AnimalSerializer(data=request.data)

        deserializer_animal.is_valid(raise_exception=True)
        animal = deserializer_animal.save()

        serializer_animal = AnimalSerializer(animal)
        return Response(serializer_animal.data, status.HTTP_201_CREATED)


class AnimalsDetailView(APIView):
    def get_animal_by_param(self, animal_id: int):
        animal_instance = Animal.objects.get(id=animal_id)
        return animal_instance

    def get(self, request: Request, animal_id: int) -> None:
        try:
            animal_instance = self.get_animal_by_param(animal_id)
        except Animal.DoesNotExist:
            message = {'detail': "Not Found."}
            return Response(message, status.HTTP_404_NOT_FOUND)

        serializer_animal = AnimalSerializer(animal_instance)

        return Response(serializer_animal.data, status.HTTP_200_OK)

    def patch(self, request: Request, animal_id: int) -> None:
        try:
            animal_instance = self.get_animal_by_param(animal_id)
        except Animal.DoesNotExist:
            message = {'detail': "Not Found."}
            return Response(message, status.HTTP_404_NOT_FOUND)

        serializer_animal = AnimalSerializer(animal_instance, request.data, partial=True)
        serializer_animal.is_valid(raise_exception=True)

        serializer_animal.save()
        return Response(serializer_animal.data, status.HTTP_200_OK)

    def delete(self, request: Request, animal_id: int) -> None:
        try:
            animal_instance = self.get_animal_by_param(animal_id)
        except Animal.DoesNotExist:
            message = {'detail': "Not Found."}
            return Response(message, status.HTTP_404_NOT_FOUND)

        animal_instance.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
