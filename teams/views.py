from rest_framework.views import APIView, Response, Request, status
from .models import Team
from django.forms.models import model_to_dict


class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []
        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.name = request.data.get("name", team.name)
        team.titles = request.data.get("titles", team.titles)
        team.top_scorer = request.data.get("top_scorer", team.top_scorer)
        team.fifa_code = request.data.get("fifa_code", team.fifa_code)
        team.founded_at = request.data.get("founded_at", team.founded_at)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
