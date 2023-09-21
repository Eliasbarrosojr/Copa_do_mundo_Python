from rest_framework.views import APIView, Request, Response, status
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from utils import data_processing
from .models import Team
from django.forms.models import model_to_dict


class TeamView(APIView):
    def get(self, req: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []
        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        team = Team.objects.create(**req.data)
        team_dict = model_to_dict(team)
        
        try:
            data_processing(team_dict)
        except NegativeTitlesError as err:
            return Response({"error": f'{err.message}'}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as err:
            return Response({"error": f'{err.message}'}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as err:
            return Response({"error": f'{err.message}'}, status.HTTP_400_BAD_REQUEST)
        
        return Response(team_dict, status.HTTP_201_CREATED)


class TeamDetailView(APIView):
    def get(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in req.data.items():
            setattr(team, key, value)

        team.save()

        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)