"""
RUN EVALUATION - Test Runner
Runs all behavior tests and displays results
"""

import unittest
import sys
from behavior_tests import TestUserManagementSystem


def run_all_tests():
    # Run behavior tests with detailed output
    print("=" * 70)
    print("RUNNING BEHAVIOR TESTS")
    print("=" * 70)
    print("\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestUserManagementSystem)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Display test summary
    print("\n" + "=" * 70)
    print("BEHAVIOR TEST SUMMARY")
    print("=" * 70)
    tests_run = result.testsRun
    tests_passed = tests_run - len(result.failures) - len(result.errors)
    tests_failed = len(result.failures)
    tests_errors = len(result.errors)

    print(f"Total Tests: {tests_run}")
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    print(f"Errors: {tests_errors}")
    print("=" * 70)

    # Return exit code
    return 0 if tests_passed == tests_run else 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
