import { UserRepository } from '../../domain/repositories/UserRepository';
import { User } from '../../domain/entities/User';
import bcrypt from 'bcryptjs';

export class RegisterUser {
  constructor(private userRepository: UserRepository) {}

  async execute(username: string, email: string, password: string): Promise<User> {
    if (!username || !email || !password) {
      throw new Error('All fields are required');
    }

    const existingUserByEmail = await this.userRepository.findByEmail(email);
    if (existingUserByEmail) {
      throw new Error('Email is already in use');
    }

    const existingUserByUsername = await this.userRepository.findByUsername(username);
    if (existingUserByUsername) {
      throw new Error('Username is already in use');
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = await this.userRepository.create({
      username,
      email,
      password: hashedPassword,
      role: 'user'
    });

    return new User(newUser.id, newUser.username, newUser.email, undefined, newUser.role, newUser.createdAt);
  }
}
