from typing import Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from app.config import get_settings
from app.models.user import User
from app.models.quest import Quest
from app.models.monster import Monster
from app.models.quiz_question import QuizQuestion
from app.models.progress import UserProgress
from app.models.item import Item, UserInventory
from app.models.achievement import Achievement, UserAchievement
from app.models.leaderboard import LeaderboardEntry

settings = get_settings()


class GameService:
    """Service for game logic operations."""
    
    
    @staticmethod
    def calculate_max_hp(level: int) -> int:
        """Calculate max HP based on level."""
        return settings.base_hp + (level - 1) * settings.hp_per_level
    
    @staticmethod
    def award_xp(db: Session, user: User, xp_amount: int) -> Tuple[int, bool]:
        """
        Award XP to a user and handle level ups.
        Logic: Flat 100 XP per level.
        When XP >= 100, Level Up and reset XP (carrying over overflow).
        Returns (new_xp_total, leveled_up).
        """
        user.current_xp += xp_amount
        leveled_up = False
        
        # Check for level up
        # Using a while loop to handle multiple level ups at once if massive XP is granted
        XP_THRESHOLD = 100
        
        while user.current_xp >= XP_THRESHOLD:
            user.level += 1
            user.current_xp -= XP_THRESHOLD # Carry over overflow (e.g. 110 -> 10)
            leveled_up = True
            
            # Heal and Increase Stats on Level Up
            user.hp_max = GameService.calculate_max_hp(user.level)
            user.hp_current = user.hp_max
        
        db.commit()
        return user.current_xp, leveled_up
    
    @staticmethod
    def award_gold(db: Session, user: User, gold_amount: int) -> int:
        """Award gold to a user. Returns new gold total."""
        user.gold += gold_amount
        db.commit()
        return user.gold
    
    @staticmethod
    def deal_damage(db: Session, user: User, damage: int) -> int:
        """Deal damage to a user. Returns remaining HP."""
        user.hp_current = max(0, user.hp_current - damage)
        db.commit()
        return user.hp_current
    
    @staticmethod
    def heal_user(db: Session, user: User, heal_amount: int) -> int:
        """Heal a user. Returns new HP."""
        user.hp_current = min(user.hp_max, user.hp_current + heal_amount)
        db.commit()
        return user.hp_current
    
    @staticmethod
    def complete_quest(db: Session, user: User, quest: Quest, score: int = 100) -> dict:
        """
        Mark a quest as completed and award rewards.
        Returns reward summary.
        Force rewards: 50 XP, 10 Gold per lesson.
        """
        # Check if already completed
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user.user_id,
            UserProgress.quest_id == quest.quest_id
        ).first()
        
        first_completion = False
        
        if not progress:
            # First attempt
            progress = UserProgress(
                user_id=user.user_id,
                quest_id=quest.quest_id,
                is_completed=True,
                score=score,
                attempts=1,
                completed_at=datetime.utcnow()
            )
            db.add(progress)
            first_completion = True
        else:
            # Update existing progress
            progress.attempts += 1
            if not progress.is_completed:
                progress.is_completed = True
                progress.completed_at = datetime.utcnow()
                first_completion = True
            if score > progress.score:
                progress.score = score
        
        # Award rewards only on first completion
        xp_earned = 0
        gold_earned = 0
        leveled_up = False
        
        # Award rewards on every completion (per user request: "Every lesson gives 50 XP")
        # Previously restricted to first_completion, but now allowing repeats.
        
        # Enforce 50 XP / 10 Gold rule
        xp_earned = 50
        gold_earned = 10
        
        # Always award XP/Gold
        if xp_earned > 0:
            _, leveled_up_status = GameService.award_xp(db, user, xp_earned)
            if leveled_up_status:
                leveled_up = True
            
        GameService.award_gold(db, user, gold_earned)
        
        # Update Weekly Progress (XP + Quest Count)
        # Note: We increment quest count even on repeat to track "activity"
        GameService.update_weekly_progress(db, user.user_id, xp_added=xp_earned, activity_type="quest_complete")
        
        db.commit()
        
        return {
            "quest_id": quest.quest_id,
            "first_completion": first_completion,
            "xp_earned": xp_earned,
            "gold_earned": gold_earned,
            "leveled_up": leveled_up,
            "new_level": user.level,
            "total_xp": user.current_xp,
            "total_gold": user.gold,
            "event": "LEVEL_UP" if leveled_up else None
        }
    
    @staticmethod
    def submit_battle_answer(
        db: Session,
        user: User,
        question_id: int,
        answer_text: str
    ) -> dict:
        """
        Process a battle answer using DB questions.
        Tracks monster health via UserProgress.score (0-100% defeated).
        """
        # Load Question
        question = db.query(QuizQuestion).filter(QuizQuestion.question_id == question_id).first()
        if not question:
            raise ValueError("Question not found")
        
        monster = question.monster
        quest = monster.quest
        
        is_correct = (answer_text == question.correct_answer)
        
        # Track Progress via UserProgress score (representing % damage to monster)
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user.user_id,
            UserProgress.quest_id == quest.quest_id
        ).first()

        damage_dealt = 0
        damage_received = 0
        monster_defeated = False
        xp_earned = 0
        gold_earned = 0
        leveled_up = False
        message = ""

        if not progress:
            # CHECK ENTRY COST (Only on first attempt/entry)
            if user.gold < monster.entry_cost:
                 return {
                    "is_correct": False,
                    "monster_defeated": False,
                    "player_hp": user.hp_current,
                    "monster_hp_pct": 100,
                    "message": f"Not enough gold to enter! Need {monster.entry_cost} coins.",
                    "error": True
                }
            # Deduct entry cost if applicable (assuming one-time fee per "battle session" logic, 
            # but since progress tracks the session, we check it here).
            # Note: User didn't specify WHEN to deduct, but "Checks if user has enough to enter" implies cost.
            if monster.entry_cost > 0:
                user.gold -= monster.entry_cost
                
            progress = UserProgress(
                user_id=user.user_id,
                quest_id=quest.quest_id,
                is_completed=False,
                score=0,
                attempts=0
            )
            db.add(progress)
        
        current_score = progress.score or 0
        
        # If already defeated, don't allow more damage
        if progress.is_completed:
            return {
                "is_correct": True,
                "monster_defeated": True,
                "player_hp": user.hp_current,
                "monster_hp_pct": 0,
                "message": "Monster already defeated!"
            }

        if is_correct:
            # Player hits Monster
            damage_pct = 20 
            new_score = min(100, current_score + damage_pct)
            progress.score = new_score
            damage_dealt = damage_pct 
            message = "Critical hit! Your answer struck true!"

            if new_score >= 100:
                monster_defeated = True
                # Mark quest complete
                progress.is_completed = True
                progress.completed_at = datetime.utcnow()
                
                # AWARD PASS REWARD
                quest_xp = quest.xp_reward
                battle_gold = monster.pass_reward
                
                if quest_xp > 0:
                    _, leveled_up_status = GameService.award_xp(db, user, quest_xp)
                    if leveled_up_status:
                        leveled_up = True
                if battle_gold > 0:
                    GameService.award_gold(db, user, battle_gold)
                
                # Update Weekly Progress (XP + Battle Count)
                GameService.update_weekly_progress(db, user.user_id, xp_added=quest_xp, activity_type="battle_won")
                
                xp_earned = quest_xp
                gold_earned = battle_gold
                message = f"Victory! {monster.name} has fallen! Earned {battle_gold} coins."
        else:
            # Monster hits Player
            # FAIL PENALTY
            damage_received = monster.fail_penalty # Use new fail_penalty field
            GameService.deal_damage(db, user, damage_received)
            
            error_status = "Glitched" # As requested
            message = f"Wrong! {monster.name} hits you for {damage_received} HP! Status: {error_status}"

        db.commit()

        return {
            "is_correct": is_correct,
            "damage_dealt": damage_dealt,
            "damage_received": damage_received,
            "monster_defeated": monster_defeated,
            "xp_earned": xp_earned,
            "gold_earned": gold_earned,
            "leveled_up": leveled_up if monster_defeated else False, 
            "event": "LEVEL_UP" if (monster_defeated and leveled_up) else None,
            "player_hp": user.hp_current,
            "monster_hp_pct": 100 - (progress.score or 0),
            "message": message,
            "status": "Glitched" if not is_correct else "Normal"
        }
    
    @staticmethod
    def purchase_item(db: Session, user: User, item: Item, quantity: int = 1) -> dict:
        """
        Purchase an item from the shop.
        Returns purchase result.
        """
        total_cost = item.price * quantity
        
        if user.gold < total_cost:
            return {
                "success": False,
                "message": f"Not enough gold! Need {total_cost}, have {user.gold}"
            }
        
        # Deduct gold
        user.gold -= total_cost
        
        # Add to inventory
        inventory = db.query(UserInventory).filter(
            UserInventory.user_id == user.user_id,
            UserInventory.item_id == item.item_id
        ).first()
        
        if inventory:
            inventory.quantity += quantity
        else:
            inventory = UserInventory(
                user_id=user.user_id,
                item_id=item.item_id,
                quantity=quantity,
                is_equipped=False
            )
            db.add(inventory)
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Purchased {quantity}x {item.name} for {total_cost} gold",
            "gold_remaining": user.gold
        }
    
    @staticmethod
    def equip_item(db: Session, user: User, item_id: int, equip: bool = True) -> dict:
        """
        Equip or unequip an item.
        """
        inventory = db.query(UserInventory).filter(
            UserInventory.user_id == user.user_id,
            UserInventory.item_id == item_id
        ).first()
        
        if not inventory:
            return {
                "success": False,
                "message": "Item not in inventory"
            }
        
        inventory.is_equipped = equip
        db.commit()
        
        action = "equipped" if equip else "unequipped"
        return {
            "success": True,
            "message": f"Item {action} successfully"
        }
    
    @staticmethod
    def check_and_award_achievements(db: Session, user: User) -> list:
        """
        Check if user qualifies for any new achievements and award them.
        Returns list of newly unlocked achievements.
        """
        # Get all achievements user doesn't have
        user_achievement_ids = [ua.achievement_id for ua in user.achievements]
        available_achievements = db.query(Achievement).filter(
            ~Achievement.achievement_id.in_(user_achievement_ids) if user_achievement_ids else True
        ).all()
        
        # Count user stats
        quests_completed = db.query(UserProgress).filter(
            UserProgress.user_id == user.user_id,
            UserProgress.is_completed == True
        ).count()
        
        newly_unlocked = []
        
        for achievement in available_achievements:
            qualified = False
            
            # Check quest achievements
            if str(achievement.achievement_type.value).upper() == "QUEST":
                if quests_completed >= achievement.requirement_value:
                    qualified = True
            
            # Add more achievement type checks as needed
            
            if qualified:
                user_achievement = UserAchievement(
                    user_id=user.user_id,
                    achievement_id=achievement.achievement_id
                )
                db.add(user_achievement)
                
                # Award achievement rewards
                if achievement.xp_reward > 0:
                    user.current_xp += achievement.xp_reward
                if achievement.gold_reward > 0:
                    user.gold += achievement.gold_reward
                if achievement.title_reward:
                    user.title = achievement.title_reward
                
                newly_unlocked.append(achievement)
        
        if newly_unlocked:
            db.commit()
        
        return newly_unlocked

    # ============ ENGAGEMENT TRACKING ============
    
    @staticmethod
    def get_or_create_streak(db: Session, user_id: int):
        """Get or create user streak record."""
        from app.models.engagement import UserStreak  # Local import to avoid circular dep
        streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
        if not streak:
            streak = UserStreak(user_id=user_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()
            db.refresh(streak)
        return streak

    @staticmethod
    def update_streak(db: Session, user_id: int):
        """Update user's streak based on activity."""
        from datetime import date, timedelta
        streak = GameService.get_or_create_streak(db, user_id)
        today = date.today()
        
        if streak.last_activity_date == today:
            return streak
        
        # If last activity was yesterday, increment
        if streak.last_activity_date == today - timedelta(days=1):
            streak.current_streak += 1
        else:
            # Streak broken or new
            streak.current_streak = 1
            streak.streak_start_date = today
            
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        
        streak.last_activity_date = today
        db.commit()
        db.refresh(streak)
        return streak

    @staticmethod
    def get_or_create_weekly_goal(db: Session, user_id: int):
        """Get or create weekly goal for current week."""
        from app.models.engagement import WeeklyGoal
        from datetime import date, timedelta
        import datetime as dt_module
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        goal = db.query(WeeklyGoal).filter(
            WeeklyGoal.user_id == user_id,
            WeeklyGoal.week_start == week_start
        ).first()
        
        if not goal:
            goal = WeeklyGoal(
                user_id=user_id,
                week_start=week_start,
                xp_target=500,
                quests_target=10,
                battles_target=3
            )
            db.add(goal)
            db.commit()
            db.refresh(goal)
        
        return goal

    @staticmethod
    def update_weekly_progress(db: Session, user_id: int, xp_added: int = 0, activity_type = None):
        """Update weekly goal progress."""
        from app.models.engagement import ActivityType
        goal = GameService.get_or_create_weekly_goal(db, user_id)
        
        if xp_added > 0:
            goal.xp_earned += xp_added
        
        if activity_type:
            # Handle string or Enum safely
            act_val = str(activity_type.value if hasattr(activity_type, 'value') else activity_type)
            
            # Use ActivityType enum values or direct string match
            if act_val == "quest_complete" or act_val == ActivityType.QUEST_COMPLETE:
                goal.quests_completed += 1
            elif act_val == "battle_won" or act_val == ActivityType.BATTLE_WON:
                goal.battles_won += 1
        
        db.commit()

    @staticmethod
    def log_activity(db: Session, user_id: int, activity_type, title: str, description: str = None, xp: int = 0, gold: int = 0, ref_id: int = None):
        """Log a user activity and update trackers."""
        from app.models.engagement import UserActivity
        
        # Create Activity Record
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            title=title,
            description=description,
            xp_earned=xp,
            gold_earned=gold,
            reference_id=ref_id
        )
        db.add(activity)
        
        # Update Trackers
        GameService.update_streak(db, user_id)
        GameService.update_weekly_progress(db, user_id, xp, activity_type)
        
        db.commit()

