from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(source='votes.count', read_only=True)
    class Meta:
        model = Option
        fields = ('id','text','votes')

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Poll
        fields = ('id','title','description','is_active','created_at','updated_at','options')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id','user','option','ip_address','created_at')
