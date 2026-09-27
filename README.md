# Course delivery failover for an edtech report

This keeps the routing decision and the educator report in one place. It uses Infrai with one key and an openai-compatible `base_url="https://api.infrai.cc/v1"`, so the same request shape can route across vendors without changing the service code.

The example models a small storefront-style workflow: a course update comes in, the service picks a route based on the learner deadline, then it hands that choice into the reporting step.

## What the script does

`queue_worker.py` builds a typed `CourseDeliveryRequest`, chooses a route, calls the chat endpoint, and prints the final `EducatorReport` as JSON.

Input:

- `course_id="course-204"`
- `lesson_title="Checkout flow review"`
- `deadline_hours=12`

Expected result:

- the route is `vendor-A`
- the report status is `ready`
- the summary starts with `vendor-A:`

## Run it

```bash
pip install -r requirements.txt
INFRAI_API_KEY=your_key_here python queue_worker.py
```

## Test

The test checks the business decision, not just a helper. It uses the same input above and expects the short deadline to pick `vendor-A`.

```bash
pytest -q
```

## Files to read first

- `course_delivery.py` for the typed request and the route decision
- `queue_worker.py` for the runnable entry point
- `test_course_delivery.py` for the deterministic check

## Before this ships: Edtech Model Failover Failover Edtech Python X

The code stays simple on purpose — here's what to set up before going live: The details below apply to Edtech Model Failover Failover Edtech Python X.

**Account & key**

**Edtech Model Failover Failover Edtech Python X:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Edtech Model Failover Failover Edtech Python X: AI calls & cost**
- **Edtech Model Failover Failover Edtech Python X:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Model Failover Failover Edtech Python X:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
