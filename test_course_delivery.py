from __future__ import annotations

from course_delivery import CourseDeliveryRequest, CourseDeliveryService


class StubInfrai:
    def chat_completion(self, *, model: str, messages: list[dict[str, str]]):
        assert model == "auto"
        assert messages[-1]["role"] == "user"
        return {
            "ok": True,
            "data": {"choices": [{"message": {"content": "Report drafted for the educator."}}]},
            "error": None,
            "metadata": {},
        }


def test_course_delivery_routes_short_deadlines_and_builds_report():
    service = CourseDeliveryService(infrai=StubInfrai())
    request = CourseDeliveryRequest(
        course_id="course-204",
        lesson_title="Checkout flow review",
        learner_count=38,
        deadline_hours=12,
        educator_email="teacher@example.com",
        lesson_notes="Keep the summary short and mention the next assignment.",
    )

    report = service.route_and_report(request)

    assert report.vendor == "auto"
    assert report.reporting_status == "ready"
    assert report.summary.startswith("vendor-A:")
    assert "Report drafted for the educator." in report.summary
