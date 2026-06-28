import { FastifyRequest, FastifyReply } from 'fastify';
import jwt from 'jsonwebtoken';

export const authMiddleware = async (req: FastifyRequest, reply: FastifyReply) => {
  let token = req.cookies.token;

  if (!token) {
    const authHeader = req.headers.authorization;
    if (authHeader) {
      token = authHeader.split(' ')[1];
    }
  }

  if (!token) {
    return reply.code(401).send({ success: false, error: 'Authentication token is missing' });
  }

  try {
    const secret = process.env.JWT_SECRET || 'jdu_secret_key_2026_restaurant';
    const decoded = jwt.verify(token, secret);
    (req as any).user = decoded;
  } catch (error) {
    return reply.code(401).send({ success: false, error: 'Invalid or expired token' });
  }
};
