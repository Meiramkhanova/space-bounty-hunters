from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import HuntLog, WantedCriminal
from .serializers import HuntLogSerializer, WantedCriminalSerializer


def _parse_bool(value, field_name):
    value = str(value).strip().lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no"):
        return False
    raise ValidationError({field_name: "Expected true or false."})


def _parse_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError({field_name: "Expected an integer."})


class WantedCriminalViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """List and retrieve wanted criminals with filtering and sorting."""

    serializer_class = WantedCriminalSerializer
    queryset = WantedCriminal.objects.all()

    def get_queryset(self):
        qs = WantedCriminal.objects.all()
        params = self.request.query_params

        min_reward = params.get("min_reward")
        max_reward = params.get("max_reward")
        if min_reward is not None:
            qs = qs.filter(reward__gte=_parse_int(min_reward, "min_reward"))
        if max_reward is not None:
            qs = qs.filter(reward__lte=_parse_int(max_reward, "max_reward"))

        for field in ("armed", "has_crew", "escape_master"):
            raw = params.get(field)
            if raw is not None:
                qs = qs.filter(**{field: _parse_bool(raw, field)})

        sort = params.get("sort")
        if sort == "reward":
            qs = qs.order_by("reward")
        elif sort == "-reward":
            qs = qs.order_by("-reward")
        else:
            qs = qs.order_by("id")

        return qs


class HuntLogViewSet(viewsets.ModelViewSet):
    """Full CRUD for bounty hunting journal entries."""

    serializer_class = HuntLogSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = HuntLog.objects.select_related("criminal").all()
        criminal_id = self.request.query_params.get("criminal_id")
        if criminal_id is not None:
            qs = qs.filter(criminal_id=_parse_int(criminal_id, "criminal_id"))
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
