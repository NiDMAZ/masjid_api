from rest_framework import serializers


class JummahKhateebSerializer(serializers.Serializer):
    date = serializers.DateField()
    khateeb = serializers.CharField(max_length=32)

    def create(self, validated_data):
        pass

    def update(self, validated_data):
        pass
