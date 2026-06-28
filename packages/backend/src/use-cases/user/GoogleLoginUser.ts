import { OAuth2Client } from 'google-auth-library';
import { UserRepository } from '../../domain/repositories/UserRepository';
import { User } from '../../domain/entities/User';
import bcrypt from 'bcryptjs';

export class GoogleLoginUser {
  private client: OAuth2Client;

  constructor(private userRepository: UserRepository) {
    this.client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);
  }

  async execute(idToken: string): Promise<User> {
    if (!idToken) {
      throw new Error('Google ID token is required');
    }

    let payload;
    try {
      const ticket = await this.client.verifyIdToken({
        idToken,
        audience: process.env.GOOGLE_CLIENT_ID
      });
      payload = ticket.getPayload();
    } catch (err: any) {
      throw new Error('Invalid Google token: ' + err.message);
    }

    if (!payload || !payload.email) {
      throw new Error('Could not retrieve user details from Google token');
    }

    const email = payload.email;
    let user = await this.userRepository.findByEmail(email);

    if (!user) {
      // Create a unique username based on the email prefix
      const emailPrefix = email.split('@')[0];
      let username = emailPrefix;
      let suffix = 1;

      // Ensure username uniqueness
      while (await this.userRepository.findByUsername(username)) {
        username = `${emailPrefix}${suffix}`;
        suffix++;
      }

      // Generate a secure random password (they login via Google, but DB requires a password)
      const randomPassword = Math.random().toString(36).slice(-10) + Math.random().toString(36).slice(-10);
      const hashedPassword = await bcrypt.hash(randomPassword, 10);

      user = await this.userRepository.create({
        username,
        email,
        password: hashedPassword,
        role: 'user'
      });
    }

    return new User(user.id, user.username, user.email, undefined, user.role, user.createdAt);
  }
}
