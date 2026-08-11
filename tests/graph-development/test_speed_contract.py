from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class GraphDevelopmentSpeedContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "skills/graph-development/SKILL.md").read_text()
        cls.branch_prompt = (ROOT / "skills/graph-development/branch-worker-prompt.md").read_text()
        cls.continuation_prompt = (ROOT / "skills/graph-development/continuation-prompt.md").read_text()
        cls.planning = (ROOT / "skills/writing-plans/SKILL.md").read_text()

    def test_skill_caps_coordination_and_defines_fast_path(self):
        self.assertIn("coordination steps than implementation nodes", self.skill)
        self.assertIn("validate once → execute graph → review once → verify once → commit once", self.skill)
        self.assertIn("coordination_budget_minutes", self.skill)

    def test_skill_schedules_for_speed_without_restarting_work(self):
        for phrase in (
            "parallel savings exceed coordination cost",
            "critical path",
            "same agent",
            "release parent capacity",
            "retry failed branch only",
            "One repair pass",
            "failing test or explicit human approval",
        ):
            self.assertIn(phrase, self.skill)

    def test_skill_budgets_tests_reviews_commits_and_metrics(self):
        for phrase in (
            "focused tests",
            "full fast suite once",
            "Review scope is locked",
            "Commit at joins",
            "implementation time",
            "coordination time",
        ):
            self.assertIn(phrase, self.skill)

    def test_prompts_propagate_budget_and_timing(self):
        self.assertIn("Coordination budget", self.branch_prompt)
        self.assertIn("Timing", self.branch_prompt)
        self.assertIn("Coordination budget", self.continuation_prompt)
        self.assertIn("critical-path", self.continuation_prompt)
        self.assertIn("Timing", self.continuation_prompt)

    def test_planning_emits_default_coordination_budget(self):
        self.assertIn("coordination_budget_minutes: 5", self.planning)


if __name__ == "__main__":
    unittest.main()
