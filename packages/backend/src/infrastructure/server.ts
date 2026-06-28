import fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import fastifyStatic from '@fastify/static';
import fastifyMultipart from '@fastify/multipart';
import fastifyCookie from '@fastify/cookie';
import path from 'path';
import fs from 'fs';
import { createRouter } from './router';

export function createServer(): FastifyInstance {
  const app = fastify({ logger: false });

  // Register CORS
  app.register(cors);

  // Register Cookie plugin
  app.register(fastifyCookie, {
    secret: process.env.COOKIE_SECRET || 'jdu_cookie_secret_key_2026_restaurant',
  });

  // Register Multipart handling (crucial for uploads!)
  app.register(fastifyMultipart);

  // Set up paths for frontend assets
  const distPath = path.join(__dirname, '../../../frontend/dist');
  const srcPath = path.join(__dirname, '../../../frontend');
  const frontendPath = fs.existsSync(distPath) ? distPath : srcPath;

  // Register static file serving for frontend files (primary static server)
  app.register(fastifyStatic, {
    root: frontendPath,
    prefix: '/'
  });

  // Register static file serving for uploads directory under "/uploads" prefix (secondary static server)
  app.register(fastifyStatic, {
    root: path.join(__dirname, '../uploads'),
    prefix: '/uploads/',
    decorateReply: false
  });

  // Register API router under "/api" prefix
  app.register(async (apiApp) => {
    await createRouter(apiApp);
  }, { prefix: '/api' });

  // SPA fallback for routing
  app.setNotFoundHandler((req, reply) => {
    if (req.url.startsWith('/api')) {
      return reply.code(404).send({ success: false, error: 'Not Found' });
    }
    return reply.sendFile('index.html');
  });

  return app;
}
