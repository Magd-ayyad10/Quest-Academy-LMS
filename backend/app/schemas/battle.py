from pydantic import BaseModel
from typing import List, Optional

class BattleQuestion(BaseModel):
    question_id: int
    question_text: str
    wrong_answers: List[str] # Frontend will shuffle these + correct answer (but we don't send correct answer)
    # Wait, if we don't send correct answer, frontend can't cheat.
    # But frontend needs to render options.
    # Where is the correct answer? Backend holds it.
    # Does frontend receive options including correct one?
    # Yes. We should probably send filtered options.
    # But for simplicity, let's send just the prompt?
    # No, multiple choice needs choices.
    # So we should send "options" list (mixed correct + wrong).
    # But QuizQuestion model stores correct separately.
    # So the response model should be constructed by router or schema method.
    pass

class BattleAttackRequest(BaseModel):
    question_id: int
    answer: str

class BattleAttackResponse(BaseModel):
    is_correct: bool
    damage_dealt: int
    damage_received: int
    monster_defeated: bool
    xp_earned: int
    gold_earned: int
    player_hp: int
    monster_hp_pct: int
    message: str

class BattleStateResponse(BaseModel):
    monster_id: int
    monster_name: str
    monster_image_url: Optional[str]
    description: Optional[str]
    monster_hp_pct: int
    player_hp: int
    questions: List[dict] # {id, text, options}
