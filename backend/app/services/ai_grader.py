from typing import Optional, Dict, Any
import httpx
import json
from app.config import get_settings

settings = get_settings()

class AIGraderService:
    @staticmethod
    async def grade_submission(
        assignment_title: str,
        assignment_description: str,
        submission_text: str,
        submission_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates the submission using OpenRouter AI.
        Returns: {
            "grade": int (0-100),
            "feedback": str,
            "status": "approved" | "rejected"
        }
        """
        
        # Prepare the prompt
        prompt = f"""
        You are an expert strict but fair teacher grading a coding assignment.
        
        Assignment Title: {assignment_title}
        Assignment Description: {assignment_description}
        
        Student Submission:
        {submission_text}
        
        Submission URL (if any): {submission_url or "N/A"}
        
        Task:
        1. Evaluate if the submission meets the requirements described in the assignment.
        2. Assign a score from 0 to 100.
        3. Provide constructive feedback (max 3 sentences).
        4. Determine status: "approved" if score >= 70, else "rejected".
        
        Return your response in strictly VALID JSON format:
        {{
            "score": <int>,
            "feedback": "<string>",
            "status": "<approved|rejected>"
        }}
        """

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173", # Optional for OpenRouter
        }
        
        data = {
            "model": settings.ai_model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0 
                )
                
                if response.status_code != 200:
                    print(f"AI Error: {response.text}")
                    return {
                        "score": 0,
                        "feedback": "AI Grading Service Unavailable. Please wait for manual grading.",
                        "status": "pending"
                    }
                
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse JSON from content (handle potential markdown ticks)
                clean_content = content.replace("```json", "").replace("```", "").strip()
                grading = json.loads(clean_content)
                
                return grading

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"AI Exception: {e}")
            return {
                "score": 0,
                "feedback": "An error occurred during auto-grading. Sent for manual review.",
                "status": "pending"
            }
