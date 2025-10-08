# User Management System Behavior

## 1. User Registration
- MUST accept username and password
- MUST reject if username already exists
- MUST reject if 100 users already registered
- MUST store user as "active"

## 2. User Login
- MUST check username exists
- MUST check password matches
- MUST check user is active
- MUST generate 6-digit session token
- MUST reject if Session Table full

## 3. Change Password
- MUST validate session token exists and is active
- MUST verify old password is correct
- MUST update to new password
- MUST reject invalid tokens
- MUST reject wrong old password