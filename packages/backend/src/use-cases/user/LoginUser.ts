import { UserRepository } from '../../domain/repositories/UserRepository';
import { User } from '../../domain/entities/User';
import bcrypt from 'bcryptjs';

export class LoginUser {
  constructor(private userRepository: UserRepository) {}

  async execute(emailOrUsername: string, password: string): Promise<User> {
    if (!emailOrUsername || !password) {
      throw new Error('Email/Username and password are required');
    }

    let user = await this.userRepository.findByEmail(emailOrUsername);
    if (!user) {
      user = await this.userRepository.findByUsername(emailOrUsername);
    }

    if (!user || !user.password) {
      throw new Error('Invalid email/username or password');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new Error('Invalid email/username or password');
    }

    return new User(user.id, user.username, user.email, undefined, user.role, user.createdAt);
  }
}
