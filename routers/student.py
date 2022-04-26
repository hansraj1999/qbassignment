from fastapi import Depends, APIRouter
from routers import oauth2
from database import schemas
from database.database import get_db
from sqlalchemy.orm import Session
from . import voting_for_president
from . import voting_for_vice_president
router = APIRouter(tags=['Student'], prefix='/Student')


@router.get('/choose_which_position_to_vote')
def choose_which_position_to_vote(choice: schemas.Choice, id_of_candidate: int, current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    if choice.value == "President":
        return voting_for_president.president_voting(id_of_candidate, current_user, db)
    elif choice.value == "Vice President":
        return voting_for_vice_president.vice_president_voting(id_of_candidate, current_user, db)
    else:
        return {'selected': 'Selected Position does not exists'}


@router.get('/standings_for_president_election')
def get_standings_for_president_election(current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return voting_for_president.president_candidates(current_user, db)


@router.get('/standings_for_vice_president_election')
def get_standings_for_vice_president_election(current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return voting_for_vice_president.vice_president_candidates(current_user, db)
