from __future__ import annotations

import json
from dataclasses import asdict

from course_delivery import CourseDeliveryRequest, CourseDeliveryService
from infrai_client import InfraiClient


def run_example() -> None:
    service = CourseDeliveryService(infrai=InfraiClient.from_env())
    request = CourseDeliveryRequest(
        course_id="course-204",
        lesson_title="Checkout flow review",
        learner_count=38,
        deadline_hours=12,
        educator_email="teacher@example.com",
        lesson_notes="Keep the summary short and mention the next assignment.",
    )
    report = service.route_and_report(request)
    print(json.dumps(asdict(report), indent=2))


if __name__ == "__main__":
    run_example()
