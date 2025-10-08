"""
EVALUATE REFACTOR - GRADING SYSTEM
Grades the refactored Python code based on Behavior Tests, Code Quality and Legacy Compatibility.
"""

import unittest
import sys
from io import StringIO
from behavior_tests import TestUserManagementSystem


class RefactorEvaluator:
    """Grading system for refactored code"""

    def __init__(self):
        self.total_score = 0
        self.max_score = 100
        self.results = {}

    def run_behavior_tests(self):
        """Run all behavior tests and calculate score"""
        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestUserManagementSystem)

        # Run tests silently
        runner = unittest.TextTestRunner(stream=StringIO(), verbosity=0)
        result = runner.run(suite)

        # Calculate behavior test score (60% of total grade)
        tests_run = result.testsRun
        tests_passed = tests_run - len(result.failures) - len(result.errors)
        behavior_score = (tests_passed / tests_run) * 60 if tests_run > 0 else 0

        self.results['behavior_tests'] = {
            'passed': tests_passed,
            'failed': len(result.failures),
            'errors': len(result.errors),
            'total': tests_run,
            'score': behavior_score
        }

        return behavior_score

    def evaluate_code_quality(self):
        """Evaluate code quality metrics"""
        print("\n" + "=" * 60)
        print("EVALUATING CODE QUALITY")
        print("=" * 60)

        quality_score = 0
        max_quality_score = 20

        try:
            from modern_app import UserManagementSystem

            # Check 1: Class exists (5 points)
            if UserManagementSystem:
                quality_score += 5
                print("✅ Class 'UserManagementSystem' exists (+5 points)")

            # Check 2: Required methods exist (10 points)
            required_methods = [
                'register_user',
                'login_user',
                'change_password',
                'generate_token',
                'menu_loop'
            ]

            system = UserManagementSystem()
            methods_found = 0
            for method in required_methods:
                if hasattr(system, method) and callable(getattr(system, method)):
                    methods_found += 1

            method_score = (methods_found / len(required_methods)) * 10
            quality_score += method_score
            print(f"✅ Required methods found: {methods_found}/{len(required_methods)} (+{method_score:.1f} points)")

            # Check 3: Data structures initialized correctly (5 points)
            has_user_table = hasattr(system, 'user_table') and len(system.user_table) == 100
            has_session_table = hasattr(system, 'session_table') and len(system.session_table) == 50
            has_counters = hasattr(system, 'user_count') and hasattr(system, 'session_count')

            structure_checks = [has_user_table, has_session_table, has_counters]
            structure_score = (sum(structure_checks) / len(structure_checks)) * 5
            quality_score += structure_score
            print(f"✅ Data structures initialized: {sum(structure_checks)}/{len(structure_checks)} (+{structure_score:.1f} points)")

        except ImportError as e:
            print(f"❌ Failed to import modern_app.py: {e}")
            quality_score = 0
        except Exception as e:
            print(f"❌ Error evaluating code quality: {e}")

        self.results['code_quality'] = {
            'score': quality_score,
            'max_score': max_quality_score
        }

        return quality_score

    def evaluate_legacy_compatibility(self):
        """Evaluate compatibility with legacy COBOL behavior"""
        print("\n" + "=" * 60)
        print("EVALUATING LEGACY COMPATIBILITY")
        print("=" * 60)

        compatibility_score = 0
        max_compatibility_score = 20

        try:
            from modern_app import UserManagementSystem
            system = UserManagementSystem()

            # Check 1: Fixed array sizes (5 points)
            if len(system.user_table) == 100 and len(system.session_table) == 50:
                compatibility_score += 5
                print("✅ Fixed array sizes match legacy (100 users, 50 sessions) (+5 points)")
            else:
                print("❌ Array sizes don't match legacy")

            # Check 2: Token generation range (5 points)
            tokens = [system.generate_token() for _ in range(10)]
            valid_tokens = all(100000 <= t <= 999999 for t in tokens)
            if valid_tokens:
                compatibility_score += 5
                print("✅ Token generation matches legacy range (100000-999999) (+5 points)")
            else:
                print("❌ Token generation out of legacy range")

            # Check 3: User data structure (5 points)
            user_entry = system.user_table[0]
            has_correct_fields = (
                'user_name' in user_entry and
                'user_password' in user_entry and
                'user_active' in user_entry
            )
            if has_correct_fields:
                compatibility_score += 5
                print("✅ User data structure matches legacy (+5 points)")
            else:
                print("❌ User data structure doesn't match legacy")

            # Check 4: Session data structure (5 points)
            session_entry = system.session_table[0]
            has_session_fields = (
                'session_token' in session_entry and
                'session_user' in session_entry and
                'session_active' in session_entry
            )
            if has_session_fields:
                compatibility_score += 5
                print("✅ Session data structure matches legacy (+5 points)")
            else:
                print("❌ Session data structure doesn't match legacy")

        except Exception as e:
            print(f"❌ Error evaluating legacy compatibility: {e}")

        self.results['legacy_compatibility'] = {
            'score': compatibility_score,
            'max_score': max_compatibility_score
        }

        return compatibility_score

    def generate_report(self):
        """Generate final grading report"""
        print("\n" + "=" * 60)
        print("FINAL GRADING REPORT")
        print("=" * 60)

        # Calculate total score
        behavior_score = self.results.get('behavior_tests', {}).get('score', 0)
        quality_score = self.results.get('code_quality', {}).get('score', 0)
        compatibility_score = self.results.get('legacy_compatibility', {}).get('score', 0)

        self.total_score = behavior_score + quality_score + compatibility_score

        # Display breakdown
        print("\nSCORE BREAKDOWN:")
        print("-" * 60)

        # Behavior tests
        bt = self.results.get('behavior_tests', {})
        print(f"1. Behavior Tests (60 points max)")
        print(f"   Tests Passed: {bt.get('passed', 0)}/{bt.get('total', 0)}")
        print(f"   Score: {behavior_score:.1f}/60.0")

        # Code quality
        cq = self.results.get('code_quality', {})
        print(f"\n2. Code Quality (20 points max)")
        print(f"   Score: {quality_score:.1f}/20.0")

        # Legacy compatibility
        lc = self.results.get('legacy_compatibility', {})
        print(f"\n3. Legacy Compatibility (20 points max)")
        print(f"   Score: {compatibility_score:.1f}/20.0")

        print("-" * 60)
        print(f"TOTAL SCORE: {self.total_score:.1f}/{self.max_score}")

        # Grade letter
        grade = self.calculate_grade(self.total_score)
        print(f"GRADE: {grade}")
        print("=" * 60)

        return {
            'total_score': self.total_score,
            'max_score': self.max_score,
            'grade': grade,
            'breakdown': self.results
        }

    def calculate_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 90:
            return 'A (Excellent)'
        elif score >= 80:
            return 'B (Good)'
        elif score >= 70:
            return 'C (Satisfactory)'
        elif score >= 60:
            return 'D (Needs Improvement)'
        else:
            return 'F (Fail)'

    def evaluate(self):
        """Run complete evaluation"""
        # Run all evaluation components silently
        behavior_score = self.run_behavior_tests()
        quality_score = self.evaluate_code_quality()
        compatibility_score = self.evaluate_legacy_compatibility()

        # Generate final report
        report = self.generate_report()

        return report


if __name__ == '__main__':
    evaluator = RefactorEvaluator()
    report = evaluator.evaluate()

    # Exit with appropriate code
    if report['total_score'] >= 70:
        sys.exit(0)  # Pass
    else:
        sys.exit(1)  # Fail
