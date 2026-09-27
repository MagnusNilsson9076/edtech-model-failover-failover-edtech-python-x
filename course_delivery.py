from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field

from infrai_client import InfraiClient, InfraiError


class CourseDeliveryRequest(BaseModel):
    course_id: str = Field(min_length=1)
    lesson_title: str = Field(min_length=1)
    learner_count: int = Field(ge=1)
    deadline_hours: int = Field(ge=1)
    educator_email: str = Field(min_length=3)
    lesson_notes: str = Field(min_length=1)


class DeliveryDecision(BaseModel):
    vendor: Literal["auto"]
    model: str
    route: str
    learner_deadline_hours: int


class EducatorReport(BaseModel):
    course_id: str
    lesson_title: str
    vendor: str
    summary: str
    reporting_status: Literal["ready"]


@dataclass(frozen=True)
class CourseDeliveryService:
    infrai: InfraiClient

    def route_and_report(self, request: CourseDeliveryRequest) -> EducatorReport:
        decision = self._choose_route(request)
        draft = self.infrai.chat_completion(
            model=decision.model,
            messages=[
                {"role": "system", "content": "Write a brief educator report for an online course."},
                {
                    "role": "user",
                    "content": (
                        f"Course: {request.course_id}\n"
                        f"Lesson: {request.lesson_title}\n"
                        f"Learners: {request.learner_count}\n"
                        f"Deadline hours: {request.deadline_hours}\n"
                        f"Notes: {request.lesson_notes}"
                    ),
                },
            ],
        )
        content = draft["data"]["choices"][0]["message"]["content"]
        return EducatorReport(
            course_id=request.course_id,
            lesson_title=request.lesson_title,
            vendor=decision.vendor,
            summary=f"{decision.route}: {content}",
            reporting_status="ready",
        )

    def _choose_route(self, request: CourseDeliveryRequest) -> DeliveryDecision:
        route = "vendor-A" if request.deadline_hours <= 24 else "vendor-B"
        return DeliveryDecision(vendor="auto", model="auto", route=route, learner_deadline_hours=request.deadline_hours)
