from fastapi import APIRouter, Depends
from database import schemas, models
from database.database import get_db
from sqlalchemy.orm import Session
from . import oauth2

router = APIRouter(tags=['Voting_For_Vice_President'], prefix='/voting/vice_president')


def vice_president_voting(id_of_vice_president: int, current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    details_of_selected_vice_president_candidate = get_details_of_specific_vice_president(id_of_vice_president,current_user, db)
    user_selected_vice_president_candidate = get_user_selected_vice_president_candidate(current_user, db)
    if not details_of_selected_vice_president_candidate:
        return 'Error Selected Candidate Not Found'

    if user_selected_vice_president_candidate['vice_president_voted_for_id'] is None:
        db.query(models.Student).filter(models.Student.email == current_user['email']).update(
            {models.Student.vice_president_voted_for_id: id_of_vice_president, models.Student.vice_president_voted_for_name:
                details_of_selected_vice_president_candidate['name']})

        db.query(models.VicePresident).filter(models.VicePresident.id == id_of_vice_president).update(
            {models.VicePresident.total_votes: details_of_selected_vice_president_candidate['total_votes']+1})
        db.commit()

        details_of_selected_vice_president_candidate = get_details_of_specific_vice_president(id_of_vice_president,current_user, db)
        return {'Message': f'Voted Successfully to {details_of_selected_vice_president_candidate["name"]}',
                f'Total votes for Selected Candidate {details_of_selected_vice_president_candidate["name"]} are'
                : details_of_selected_vice_president_candidate['total_votes'],
                "Standings are as follows": vice_president_candidates(current_user, db)}

    else:
        return {'Message': 'You Have already Voted cant vote Twice'}

    # future update:  if user wants to change the vote
    # if user_selected_vice_president_candidate['vice_president_voted_for_id'] == id_of_vice_president:
    #     return 'Cannot Vote twice to same Candidate'
    #
    # else:
    #     old_voted_candidate = get_details_of_specific_vice_president
    #     (user_selected_president_candidate['vice_president_voted_for_id'], db)
    #
    #     db.query(models.VicePresident).filter(models.VicePresident.id ==
    #     user_selected_president_candidate['vice_president_voted_for_id']).update(
    #         {models.VicePresident.total_votes: old_voted_candidate['total_votes']-1})
    #     db.commit()
    #
    #     db.query(models.Student).filter(models.Student.email == current_user['email']).update(
    #         {models.Student.vice_president_voted_for_id: id_of_vice_president, models.Student.vice_president_voted_for_name:
    #             details_of_selected_president_candidate['name']})
    #
    #     db.query(models.VicePresident).filter(models.VicePresident.id == id_of_vice_president).update(
    #         {models.VicePresident.total_votes: details_of_selected_vice_president_candidate['total_votes'] + 1})
    #     db.commit()
    #
    #     return 'Voting Done'


def vice_president_candidates(current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.VicePresident.id, models.VicePresident.name, models.VicePresident.total_votes).order_by(models.VicePresident.total_votes.desc()).all()
    return query


@router.get('/get_details_of_specific_vice_president')
def get_details_of_specific_vice_president(id_of_vice_president: int,current_user: schemas.Student = Depends(oauth2.get_current_user),  db: Session = Depends(get_db)):
    query = db.query(models.VicePresident.id, models.VicePresident.name, models.VicePresident.total_votes).filter(models.VicePresident.id == id_of_vice_president).first()
    return query


@router.get('/get_user_selected_vice_president_candidate')
def get_user_selected_vice_president_candidate(current_user: schemas.Student = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Student.vice_president_voted_for_id,models.Student.vice_president_voted_for_name).filter(models.Student.email == current_user['email']).first()
    return query
