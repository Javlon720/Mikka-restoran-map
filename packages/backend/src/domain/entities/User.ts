export class User {
  constructor(
    public readonly id: number,
    public readonly username: string,
    public readonly email: string,
    public readonly password?: string,
    public readonly role: 'user' | 'admin' = 'user',
    public readonly createdAt?: Date
  ) {}
}
