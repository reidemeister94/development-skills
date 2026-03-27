# Authentication Flow

## Overview of the Authentication System

Our authentication system handles user login and verification. The system is responsible for authenticating users when they attempt to log in. When a user wants to access the system, they must first be authenticated through our authentication flow.

## How Authentication Works

The authentication process works as follows. When a user submits their credentials, the system verifies these credentials against the database. In other words, the login credentials provided by the user are checked against stored credentials to ensure they match.

If the credentials are valid, meaning the username and password match what's in the database, the system generates a JWT token. This JWT token, which is a JSON Web Token, contains the user's ID and role. The token includes the user ID and the user's role information.

The JWT token expires after 24 hours. After 24 hours, the token is no longer valid. This means that every 24 hours, users need to re-authenticate because their tokens expire after a 24-hour period.

## Refresh Token Mechanism

To avoid forcing users to log in every 24 hours (since the access token expires after 24 hours), we implement a refresh token mechanism. The refresh token allows users to get a new access token without re-entering their credentials. This is important because without refresh tokens, users would need to log in again every time their access token expires.

Refresh tokens have a 30-day expiration. They last for 30 days before the user must log in again. The 30-day refresh token expiration provides a good balance between security and user convenience.

## Security Measures

Security is important. The importance of security cannot be overstated. We take security very seriously, as it is a critical aspect of our authentication system.

Passwords are hashed with bcrypt (cost factor 12). We use bcrypt with a cost factor of 12 to hash all passwords. This ensures that passwords are securely stored using the bcrypt hashing algorithm.

Rate limiting is applied: 5 failed attempts lock the account for 15 minutes. If a user fails to authenticate 5 times, their account gets locked for a 15-minute period. This rate limiting of 5 attempts with a 15-minute lockout prevents brute force attacks.
