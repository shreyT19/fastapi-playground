from fastapi import status, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import VoteSchema
from oauth2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def vote(vote: VoteSchema, db: Session=Depends(get_db), current_user: int = Depends(get_current_user)):
#     vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).first()
#     if(vote.direction == True):
#         #check if the user has already voted on the post
#         if vote_query is not None:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted on this post")
#         else :
#             new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
#             db.add(new_vote)
#             db.commit()
#             return {"message": "Vote was successfully added"}
#     else:
#         if not vote_query:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote was not found")
        
#         vote_query.delete(synchronize_session=False)
#         db.commit()
        
#         return {"message": "Vote was successfully removed"}

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: VoteSchema, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")
        vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).first()
        #check if the post exists in the database else raise an error
        if vote.direction:
            if vote_query is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted on this post")
            else:
                new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
                db.add(new_vote)
                message = "Vote was successfully added"
        else:
            #check if the vote exists
            if vote_query is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote was not found")
            else:
                db.delete(vote_query)
                message = "Vote was successfully removed"
        db.commit()
        return {"message": message}
    except Exception as e:
        db.rollback()
        raise e
        