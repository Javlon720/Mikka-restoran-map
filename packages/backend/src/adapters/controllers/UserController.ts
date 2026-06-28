import { FastifyRequest, FastifyReply } from 'fastify';
import { RegisterUser } from '../../use-cases/user/RegisterUser';
import { LoginUser } from '../../use-cases/user/LoginUser';
import { GoogleLoginUser } from '../../use-cases/user/GoogleLoginUser';
import jwt from 'jsonwebtoken';
import '@fastify/cookie';

export class UserController {
  constructor(
    private registerUser: RegisterUser,
    private loginUser: LoginUser,
    private googleLoginUser: GoogleLoginUser
  ) {}

  async register(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const { username, email, password } = req.body as any;
      const user = await this.registerUser.execute(username, email, password);
      reply.code(201).send({
        success: true,
        message: 'Registration successful',
        user
      });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async login(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const { emailOrUsername, password } = req.body as any;
      const user = await this.loginUser.execute(emailOrUsername, password);

      const secret = process.env.JWT_SECRET || 'jdu_secret_key_2026_restaurant';
      const token = jwt.sign(
        { id: user.id, username: user.username, role: user.role },
        secret,
        { expiresIn: '7d' }
      );

      reply.cookie('token', token, {
        path: '/',
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      reply.code(200).send({
        success: true,
        message: 'Login successful',
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role
        }
      });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async googleLogin(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const { idToken } = req.body as any;
      const user = await this.googleLoginUser.execute(idToken);

      const secret = process.env.JWT_SECRET || 'jdu_secret_key_2026_restaurant';
      const token = jwt.sign(
        { id: user.id, username: user.username, role: user.role },
        secret,
        { expiresIn: '7d' }
      );

      reply.cookie('token', token, {
        path: '/',
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      reply.code(200).send({
        success: true,
        message: 'Google login successful',
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role
        }
      });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async logout(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    reply.clearCookie('token', { path: '/' });
    reply.code(200).send({
      success: true,
      message: 'Logout successful'
    });
  }
}
