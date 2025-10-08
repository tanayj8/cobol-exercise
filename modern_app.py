"""
USER MANAGEMENT SYSTEM - PYTHON VERSION
Replicates the exact functionality of the legacy COBOL application
"""

import random


class UserManagementSystem:
    def __init__(self):
        """Initialize the user management system"""
        # User database - fixed array (max 100 users)
        self.user_table = []
        for _ in range(100):
            self.user_table.append({
                'user_name': '',
                'user_password': '',
                'user_active': 0
            })

        # Session table - fixed array (max 50 sessions)
        self.session_table = []
        for _ in range(50):
            self.session_table.append({
                'session_token': 0,
                'session_user': '',
                'session_active': 0
            })

        # Counters
        self.user_count = 0
        self.session_count = 0

        # Status flags
        self.ws_user_found = 0
        self.ws_success_flag = 0

    def display_welcome(self):
        """Display welcome banner"""
        print("========================================")
        print("   USER MANAGEMENT SYSTEM v1.0         ")
        print("   LEGACY MAINFRAME APPLICATION        ")
        print("========================================")

    def display_menu(self):
        """Display main menu"""
        print(" ")
        print("MAIN MENU:")
        print("1. REGISTER NEW USER")
        print("2. LOGIN")
        print("3. CHANGE PASSWORD")
        print("4. EXIT")
        choice = input("ENTER CHOICE (1-4): ")
        return choice

    def register_user(self):
        """Register a new user"""
        print("--- USER REGISTRATION ---")
        ws_username = input("ENTER USERNAME: ")
        ws_password = input("ENTER PASSWORD: ")

        # Check if user already exists
        self.ws_user_found = 0
        for user_idx in range(self.user_count):
            if self.user_table[user_idx]['user_name'] == ws_username:
                self.ws_user_found = 1
                break

        if self.ws_user_found == 1:
            print("ERROR: USERNAME ALREADY EXISTS!")
        else:
            if self.user_count < 100:
                user_idx = self.user_count
                self.user_table[user_idx]['user_name'] = ws_username
                self.user_table[user_idx]['user_password'] = ws_password
                self.user_table[user_idx]['user_active'] = 1
                self.user_count += 1
                print("SUCCESS: USER REGISTERED!")
            else:
                print("ERROR: USER DATABASE FULL!")

    def login_user(self):
        """Login a user"""
        print("--- USER LOGIN ---")
        ws_username = input("ENTER USERNAME: ")
        ws_password = input("ENTER PASSWORD: ")

        # Verify credentials
        self.ws_user_found = 0
        for user_idx in range(self.user_count):
            if self.user_table[user_idx]['user_name'] == ws_username:
                if self.user_table[user_idx]['user_password'] == ws_password:
                    if self.user_table[user_idx]['user_active'] == 1:
                        self.ws_user_found = 1
                        break

        if self.ws_user_found == 1:
            ws_random_num = self.generate_token()
            if self.session_count < 50:
                sess_idx = self.session_count
                self.session_table[sess_idx]['session_token'] = ws_random_num
                self.session_table[sess_idx]['session_user'] = ws_username
                self.session_table[sess_idx]['session_active'] = 1
                self.session_count += 1
                print("SUCCESS: LOGIN APPROVED")
                print(f"YOUR SESSION TOKEN: {self.session_table[sess_idx]['session_token']}")
            else:
                print("ERROR: SESSION TABLE FULL!")
        else:
            print("ERROR: INVALID CREDENTIALS!")

    def change_password(self):
        """Change user password"""
        print("--- CHANGE PASSWORD ---")
        ws_token = int(input("ENTER SESSION TOKEN: "))
        ws_old_password = input("ENTER OLD PASSWORD: ")
        ws_new_password = input("ENTER NEW PASSWORD: ")

        # Validate session token
        self.ws_user_found = 0
        ws_temp_user = ''
        for sess_idx in range(self.session_count):
            if self.session_table[sess_idx]['session_token'] == ws_token:
                if self.session_table[sess_idx]['session_active'] == 1:
                    ws_temp_user = self.session_table[sess_idx]['session_user']
                    self.ws_user_found = 1
                    break

        if self.ws_user_found == 0:
            print("ERROR: INVALID SESSION TOKEN!")
        else:
            # Find user and verify old password
            self.ws_success_flag = 0
            for user_idx in range(self.user_count):
                if self.user_table[user_idx]['user_name'] == ws_temp_user:
                    if self.user_table[user_idx]['user_password'] == ws_old_password:
                        self.user_table[user_idx]['user_password'] = ws_new_password
                        self.ws_success_flag = 1
                        print("SUCCESS: PASSWORD CHANGED!")
                    else:
                        print("ERROR: OLD PASSWORD INCORRECT!")
                        self.ws_success_flag = 1
                    break

    def generate_token(self):
        """Generate a 6-digit session token (not cryptographically secure!)"""
        # Simple pseudo-random number generation
        ws_random_num = int(random.random() * 900000 + 100000)
        return ws_random_num

    def menu_loop(self):
        """Main menu loop"""
        while True:
            ws_menu_choice = self.display_menu()

            if ws_menu_choice == '1':
                self.register_user()
            elif ws_menu_choice == '2':
                self.login_user()
            elif ws_menu_choice == '3':
                self.change_password()
            elif ws_menu_choice == '4':
                print("SYSTEM SHUTDOWN...")
                break
            else:
                print("INVALID CHOICE. TRY AGAIN.")

    def run(self):
        """Main entry point"""
        self.display_welcome()
        self.menu_loop()


if __name__ == "__main__":
    system = UserManagementSystem()
    system.run()
