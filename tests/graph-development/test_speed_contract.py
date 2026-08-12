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
        self.assertIn("implement all → verify all → clean code → optional tests → commit once", self.skill)
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
            "Do not add new tests during implementation",
            "Existing tests affected by code changes are the exception",
            "run existing affected tests",
            "Verify scope is locked",
            "Commit at joins",
            "implementation time",
            "coordination time",
        ):
            self.assertIn(phrase, self.skill)

    def test_skill_defines_sequential_development_verification_quality_and_test_phases(self):
        phases = (
            "## Phase 1: Full Development",
            "## Phase 2: Full Verification",
            "## Phase 3: Clean-Code Quality",
            "## Phase 4: Optional New Tests",
        )
        positions = [self.skill.index(phase) for phase in phases]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("compare every delivered behavior with the plan and specs", self.skill.lower())
        self.assertIn("available clean-code skills", self.skill)
        self.assertIn("Ask the human whether to add new tests", self.skill)

    def test_prompts_do_not_require_per_node_tests(self):
        self.assertNotIn("focused tests", self.branch_prompt)
        self.assertNotIn("focused integration tests", self.continuation_prompt)
        self.assertIn("existing affected tests", self.branch_prompt.lower())
        self.assertIn("spec verification happens after full implementation", self.branch_prompt)
        self.assertIn("full verification phase", self.continuation_prompt)

    def test_prompts_propagate_budget_and_timing(self):
        self.assertIn("Coordination budget", self.branch_prompt)
        self.assertIn("Timing", self.branch_prompt)
        self.assertIn("Coordination budget", self.continuation_prompt)
        self.assertIn("critical-path", self.continuation_prompt)
        self.assertIn("Timing", self.continuation_prompt)

    def test_planning_emits_default_coordination_budget(self):
        self.assertIn("coordination_budget_minutes: 5", self.planning)

    def test_skill_routes_supported_models_at_medium_effort(self):
        for model in (
            "gpt-5.6-sol",
            "gpt-5.6-terra",
            "gpt-5.6-luna",
            "gpt-5.3-codex-spark",
        ):
            self.assertIn(model, self.skill)
        self.assertIn("reasoning_effort: medium", self.skill)
        self.assertIn("Explicit human model choice wins", self.skill)
        self.assertIn("Select once per branch", self.skill)

    def test_prompts_carry_selected_model_and_medium_effort(self):
        for prompt in (self.branch_prompt, self.continuation_prompt):
            self.assertIn("Selected model", prompt)
            self.assertIn("Reasoning effort: medium", prompt)


if __name__ == "__main__":
    unittest.main()
