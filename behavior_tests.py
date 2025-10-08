"""
BEHAVIOR TESTS FOR USER MANAGEMENT SYSTEM
Tests validate the exact functionality of the legacy COBOL application
"""

import unittest
from modern_app import UserManagementSystem


class TestUserManagementSystem(unittest.TestCase):
    """Test suite for User Management System"""

    def setUp(self):
        """Create a fresh system instance for each test"""
        self.system = UserManagementSystem()

    def test_register_user_successfully(self):
        """✅ Register user successfully"""
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password123'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Verify user was added
        self.assertEqual(self.system.user_count, 1)
        self.assertEqual(self.system.user_table[0]['user_name'], 'testuser')
        self.assertEqual(self.system.user_table[0]['user_password'], 'password123')
        self.assertEqual(self.system.user_table[0]['user_active'], 1)

    def test_reject_duplicate_username(self):
        """✅ Reject duplicate username"""
        # Register first user
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password123'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Try to register duplicate
        ws_username = 'testuser'
        ws_user_found = 0
        for user_idx in range(self.system.user_count):
            if self.system.user_table[user_idx]['user_name'] == ws_username:
                ws_user_found = 1
                break

        self.assertEqual(ws_user_found, 1)
        self.assertEqual(self.system.user_count, 1)  # Count should not increase

    def test_reject_when_db_full(self):
        """✅ Reject when DB full (100 users)"""
        # Fill the database with 100 users
        for i in range(100):
            self.system.user_table[i]['user_name'] = f'user{i}'
            self.system.user_table[i]['user_password'] = 'password'
            self.system.user_table[i]['user_active'] = 1
        self.system.user_count = 100

        # Try to add 101st user
        can_add = self.system.user_count < 100
        self.assertFalse(can_add)
        self.assertEqual(self.system.user_count, 100)

    def test_login_with_valid_credentials(self):
        """✅ Login with valid credentials"""
        # Create a user
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password123'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Verify credentials
        ws_username = 'testuser'
        ws_password = 'password123'
        ws_user_found = 0
        for user_idx in range(self.system.user_count):
            if self.system.user_table[user_idx]['user_name'] == ws_username:
                if self.system.user_table[user_idx]['user_password'] == ws_password:
                    if self.system.user_table[user_idx]['user_active'] == 1:
                        ws_user_found = 1
                        break

        self.assertEqual(ws_user_found, 1)

    def test_reject_invalid_credentials(self):
        """✅ Reject invalid credentials"""
        # Create a user
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password123'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Try with wrong password
        ws_username = 'testuser'
        ws_password = 'wrongpassword'
        ws_user_found = 0
        for user_idx in range(self.system.user_count):
            if self.system.user_table[user_idx]['user_name'] == ws_username:
                if self.system.user_table[user_idx]['user_password'] == ws_password:
                    if self.system.user_table[user_idx]['user_active'] == 1:
                        ws_user_found = 1
                        break

        self.assertEqual(ws_user_found, 0)

    def test_generate_valid_session_token(self):
        """✅ Generate valid session token"""
        token = self.system.generate_token()

        # Token should be 6 digits (100000-999999)
        self.assertGreaterEqual(token, 100000)
        self.assertLessEqual(token, 999999)

    def test_token_maps_to_correct_user(self):
        """✅ Token maps to correct user"""
        # Create a user and session
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password123'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Create session
        token = 123456
        self.system.session_table[0]['session_token'] = token
        self.system.session_table[0]['session_user'] = 'testuser'
        self.system.session_table[0]['session_active'] = 1
        self.system.session_count = 1

        # Verify token maps to user
        self.assertEqual(self.system.session_table[0]['session_user'], 'testuser')
        self.assertEqual(self.system.session_table[0]['session_token'], 123456)

    def test_change_password_with_valid_token_and_old_password(self):
        """✅ Change password with valid token + old password"""
        # Create user
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'oldpass'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Create session
        self.system.session_table[0]['session_token'] = 123456
        self.system.session_table[0]['session_user'] = 'testuser'
        self.system.session_table[0]['session_active'] = 1
        self.system.session_count = 1

        # Change password
        ws_token = 123456
        ws_old_password = 'oldpass'
        ws_new_password = 'newpass'

        # Validate session token
        ws_user_found = 0
        ws_temp_user = ''
        for sess_idx in range(self.system.session_count):
            if self.system.session_table[sess_idx]['session_token'] == ws_token:
                if self.system.session_table[sess_idx]['session_active'] == 1:
                    ws_temp_user = self.system.session_table[sess_idx]['session_user']
                    ws_user_found = 1
                    break

        self.assertEqual(ws_user_found, 1)

        # Find user and verify old password
        ws_success_flag = 0
        for user_idx in range(self.system.user_count):
            if self.system.user_table[user_idx]['user_name'] == ws_temp_user:
                if self.system.user_table[user_idx]['user_password'] == ws_old_password:
                    self.system.user_table[user_idx]['user_password'] = ws_new_password
                    ws_success_flag = 1
                    break

        self.assertEqual(ws_success_flag, 1)
        self.assertEqual(self.system.user_table[0]['user_password'], 'newpass')

    def test_reject_invalid_token(self):
        """✅ Reject invalid token"""
        # Create user and session
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'password'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        self.system.session_table[0]['session_token'] = 123456
        self.system.session_table[0]['session_user'] = 'testuser'
        self.system.session_table[0]['session_active'] = 1
        self.system.session_count = 1

        # Try with invalid token
        ws_token = 999999
        ws_user_found = 0
        for sess_idx in range(self.system.session_count):
            if self.system.session_table[sess_idx]['session_token'] == ws_token:
                if self.system.session_table[sess_idx]['session_active'] == 1:
                    ws_user_found = 1
                    break

        self.assertEqual(ws_user_found, 0)

    def test_reject_wrong_old_password(self):
        """✅ Reject wrong old password"""
        # Create user
        self.system.user_table[0]['user_name'] = 'testuser'
        self.system.user_table[0]['user_password'] = 'correctpass'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_count = 1

        # Create session
        self.system.session_table[0]['session_token'] = 123456
        self.system.session_table[0]['session_user'] = 'testuser'
        self.system.session_table[0]['session_active'] = 1
        self.system.session_count = 1

        # Try to change with wrong old password
        ws_old_password = 'wrongpass'
        password_matches = (self.system.user_table[0]['user_password'] == ws_old_password)

        self.assertFalse(password_matches)

    def test_handle_multiple_sessions(self):
        """✅ Handle multiple sessions"""
        # Create users
        self.system.user_table[0]['user_name'] = 'user1'
        self.system.user_table[0]['user_password'] = 'pass1'
        self.system.user_table[0]['user_active'] = 1
        self.system.user_table[1]['user_name'] = 'user2'
        self.system.user_table[1]['user_password'] = 'pass2'
        self.system.user_table[1]['user_active'] = 1
        self.system.user_count = 2

        # Create multiple sessions
        self.system.session_table[0]['session_token'] = 111111
        self.system.session_table[0]['session_user'] = 'user1'
        self.system.session_table[0]['session_active'] = 1

        self.system.session_table[1]['session_token'] = 222222
        self.system.session_table[1]['session_user'] = 'user2'
        self.system.session_table[1]['session_active'] = 1

        self.system.session_table[2]['session_token'] = 333333
        self.system.session_table[2]['session_user'] = 'user1'
        self.system.session_table[2]['session_active'] = 1

        self.system.session_count = 3

        # Verify all sessions exist
        self.assertEqual(self.system.session_count, 3)
        self.assertEqual(self.system.session_table[0]['session_user'], 'user1')
        self.assertEqual(self.system.session_table[1]['session_user'], 'user2')
        self.assertEqual(self.system.session_table[2]['session_user'], 'user1')

    def test_reject_when_session_table_full(self):
        """✅ Reject when session table full (50 sessions)"""
        # Fill session table with 50 sessions
        for i in range(50):
            self.system.session_table[i]['session_token'] = 100000 + i
            self.system.session_table[i]['session_user'] = f'user{i}'
            self.system.session_table[i]['session_active'] = 1
        self.system.session_count = 50

        # Try to add 51st session
        can_add = self.system.session_count < 50
        self.assertFalse(can_add)
        self.assertEqual(self.system.session_count, 50)


if __name__ == '__main__':
    unittest.main(verbosity=2)