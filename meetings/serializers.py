from django.forms import widgets
from rest_framework import serializers
from meetings.models import Meeting
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    meetings = serializers.PrimaryKeyRelatedField(many=True, queryset=Meeting.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'meetings')

class MeetingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = Meeting
        fields = ('id', 'user', 'created', 'sinceWhen', 'tilWhen')

    def validate(self, data):
        if data['sinceWhen'] >= data['tilWhen']:
            raise serializers.ValidationError("End time must be after start time.")
        for exist in Meeting.objects.all():
            if self.instance != None and exist.id == self.instance.id:
                continue
            if exist.sinceWhen < data['sinceWhen'] and data['sinceWhen'] < exist.tilWhen:
                raise serializers.ValidationError("New meeting must be start after other meeting end.")
            if exist.sinceWhen < data['tilWhen'] and data['tilWhen'] < exist.tilWhen:
                raise serializers.ValidationError("New meeting must be end before other meeting start.")
            if data['sinceWhen'] <= exist.sinceWhen and exist.tilWhen <= data['tilWhen']:
                raise serializers.ValidationError("You cannot make reservation during other meeting proceeding.")
        return data

    def create(self, validated_data):
        return Meeting.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sinceWhen = validated_data.get('sinceWhen', instance.sinceWhen)
        instance.tilWhen = validated_data.get('tilWhen', instance.tilWhen)
        instance.save()
        return instance