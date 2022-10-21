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



