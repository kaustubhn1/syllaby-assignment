from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Book
from .schema import BookSchema


class BookSerializer(ModelSerializer):

    def validate(self, data):
        try:
            errors = BookSchema.model_validate(data['content'])
        except Exception as errors:
            raise ValidationError(errors.errors())
        return super().validate(data)

    class Meta:
        model = Book
        fields = '__all__'