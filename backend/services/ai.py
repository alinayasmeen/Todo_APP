"""
AI Service Integration Module

This module provides integration points for AI services in the Todo App.
It defines interfaces and patterns that can be extended for various AI capabilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..models import Task, User
import asyncio
import logging

logger = logging.getLogger(__name__)


class AITaskSuggestion(BaseModel):
    """
    Model representing an AI-generated task suggestion.
    """
    title: str
    description: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    estimated_duration_minutes: Optional[int] = None
    category: Optional[str] = None


class AIInsight(BaseModel):
    """
    Model representing an AI-generated insight about user productivity.
    """
    insight_type: str  # "productivity", "pattern", "recommendation", etc.
    title: str
    description: str
    data: Dict[str, Any]


class AIServiceInterface(ABC):
    """
    Abstract interface for AI services.
    This defines the contract that any AI service implementation must follow.
    """

    @abstractmethod
    async def generate_task_suggestions(self, user: User, context: Dict[str, Any]) -> List[AITaskSuggestion]:
        """
        Generate task suggestions for a user based on context.

        Args:
            user: The user for whom to generate suggestions
            context: Additional context information (existing tasks, preferences, etc.)

        Returns:
            List of AI-generated task suggestions
        """
        pass

    @abstractmethod
    async def analyze_productivity_patterns(self, user: User, tasks: List[Task]) -> List[AIInsight]:
        """
        Analyze productivity patterns based on user's task history.

        Args:
            user: The user whose patterns to analyze
            tasks: List of user's tasks for analysis

        Returns:
            List of AI-generated insights about productivity patterns
        """
        pass

    @abstractmethod
    async def predict_task_completion_time(self, user: User, task: Task) -> int:
        """
        Predict how long a task will take to complete.

        Args:
            user: The user who will perform the task
            task: The task to analyze

        Returns:
            Estimated completion time in minutes
        """
        pass

    @abstractmethod
    async def categorize_task(self, task: Task) -> str:
        """
        Categorize a task based on its content.

        Args:
            task: The task to categorize

        Returns:
            Category string (e.g., "work", "personal", "health", etc.)
        """
        pass


class MockAIService(AIServiceInterface):
    """
    Mock implementation of AI service for development and testing purposes.
    This simulates AI capabilities without requiring actual AI models.
    """

    async def generate_task_suggestions(self, user: User, context: Dict[str, Any]) -> List[AITaskSuggestion]:
        """
        Generate mock task suggestions.
        """
        logger.info(f"Generating task suggestions for user {user.id}")

        # This would normally call an actual AI model
        suggestions = [
            AITaskSuggestion(
                title="Review quarterly reports",
                description="Review and summarize the latest quarterly reports",
                priority="high",
                estimated_duration_minutes=120,
                category="work"
            ),
            AITaskSuggestion(
                title="Schedule team meeting",
                description="Schedule a team meeting for project planning",
                priority="medium",
                estimated_duration_minutes=60,
                category="work"
            )
        ]

        # Simulate AI processing time
        await asyncio.sleep(0.1)

        return suggestions

    async def analyze_productivity_patterns(self, user: User, tasks: List[Task]) -> List[AIInsight]:
        """
        Generate mock productivity insights.
        """
        logger.info(f"Analyzing productivity patterns for user {user.id}")

        insights = []

        if tasks:
            completed_count = sum(1 for task in tasks if task.completed)
            completion_rate = completed_count / len(tasks) if tasks else 0

            if completion_rate > 0.8:
                insights.append(
                    AIInsight(
                        insight_type="productivity",
                        title="High Completion Rate",
                        description=f"You've completed {completion_rate:.0%} of your tasks!",
                        data={"completion_rate": completion_rate}
                    )
                )
            else:
                insights.append(
                    AIInsight(
                        insight_type="recommendation",
                        title="Task Completion Tip",
                        description="Try breaking larger tasks into smaller, manageable chunks",
                        data={"suggested_action": "break_down_large_tasks"}
                    )
                )

        # Simulate AI processing time
        await asyncio.sleep(0.1)

        return insights

    async def predict_task_completion_time(self, user: User, task: Task) -> int:
        """
        Predict mock completion time for a task.
        """
        logger.info(f"Predicting completion time for task {task.id} for user {user.id}")

        # Simulate prediction based on task title length and complexity
        base_time = 30  # Base time in minutes
        complexity_factor = len(task.title.split()) * 2

        # Simulate AI processing time
        await asyncio.sleep(0.05)

        return base_time + complexity_factor

    async def categorize_task(self, task: Task) -> str:
        """
        Categorize a task based on its content.
        """
        logger.info(f"Categorizing task {task.id}")

        title_lower = task.title.lower()

        if any(word in title_lower for word in ["meeting", "call", "discuss", "talk"]):
            category = "communication"
        elif any(word in title_lower for word in ["report", "write", "document", "draft"]):
            category = "documentation"
        elif any(word in title_lower for word in ["bug", "fix", "code", "develop"]):
            category = "development"
        elif any(word in title_lower for word in ["gym", "exercise", "workout", "health"]):
            category = "health"
        else:
            category = "general"

        # Simulate AI processing time
        await asyncio.sleep(0.05)

        return category


# Global AI service instance
# In production, this would be configured based on environment variables
ai_service: AIServiceInterface = MockAIService()


def get_ai_service() -> AIServiceInterface:
    """
    Get the configured AI service instance.

    Returns:
        AIServiceInterface: The configured AI service
    """
    global ai_service
    return ai_service


async def integrate_ai_suggestions(user: User, existing_context: Dict[str, Any]) -> List[AITaskSuggestion]:
    """
    Integrate AI-generated task suggestions into the application flow.

    Args:
        user: The user requesting suggestions
        existing_context: Context about the user's current situation

    Returns:
        List of AI-generated task suggestions
    """
    service = get_ai_service()
    return await service.generate_task_suggestions(user, existing_context)


async def get_productivity_insights(user: User, tasks: List[Task]) -> List[AIInsight]:
    """
    Get AI-generated productivity insights for a user.

    Args:
        user: The user requesting insights
        tasks: List of user's tasks for analysis

    Returns:
        List of AI-generated insights
    """
    service = get_ai_service()
    return await service.analyze_productivity_patterns(user, tasks)