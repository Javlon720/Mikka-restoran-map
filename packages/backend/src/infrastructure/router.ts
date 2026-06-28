import { FastifyInstance } from 'fastify';
import { PgUserRepository } from '../adapters/repositories/pg/PgUserRepository';
import { PgRestaurantRepository } from '../adapters/repositories/pg/PgRestaurantRepository';
import { PgReviewRepository } from '../adapters/repositories/pg/PgReviewRepository';

import { RegisterUser } from '../use-cases/user/RegisterUser';
import { LoginUser } from '../use-cases/user/LoginUser';
import { GoogleLoginUser } from '../use-cases/user/GoogleLoginUser';
import { GetRestaurants } from '../use-cases/restaurant/GetRestaurants';
import { CreateRestaurant } from '../use-cases/restaurant/CreateRestaurant';
import { UpdateRestaurant } from '../use-cases/restaurant/UpdateRestaurant';
import { DeleteRestaurant } from '../use-cases/restaurant/DeleteRestaurant';
import { GetReviewsByRestaurant } from '../use-cases/review/GetReviewsByRestaurant';
import { CreateReview } from '../use-cases/review/CreateReview';
import { GetGeminiResponse } from '../use-cases/chat/GetGeminiResponse';

import { UserController } from '../adapters/controllers/UserController';
import { RestaurantController } from '../adapters/controllers/RestaurantController';
import { ReviewController } from '../adapters/controllers/ReviewController';
import { ChatController } from '../adapters/controllers/ChatController';

import { authMiddleware } from './middleware/auth';
import { upload } from './middleware/upload';

export async function createRouter(app: FastifyInstance): Promise<void> {
  // Instantiate Repositories (Adapters)
  const userRepository = new PgUserRepository();
  const restaurantRepository = new PgRestaurantRepository();
  const reviewRepository = new PgReviewRepository();

  // Instantiate Use Cases (Domain logic)
  const registerUser = new RegisterUser(userRepository);
  const loginUser = new LoginUser(userRepository);
  const googleLoginUser = new GoogleLoginUser(userRepository);

  const getRestaurants = new GetRestaurants(restaurantRepository);
  const createRestaurant = new CreateRestaurant(restaurantRepository);
  const updateRestaurant = new UpdateRestaurant(restaurantRepository);
  const deleteRestaurant = new DeleteRestaurant(restaurantRepository);

  const getReviewsByRestaurant = new GetReviewsByRestaurant(reviewRepository);
  const createReview = new CreateReview(reviewRepository);
  const getGeminiResponse = new GetGeminiResponse(restaurantRepository);

  // Instantiate Controllers (Adapters)
  const userController = new UserController(registerUser, loginUser, googleLoginUser);
  const restaurantController = new RestaurantController(
    getRestaurants,
    createRestaurant,
    updateRestaurant,
    deleteRestaurant,
    restaurantRepository
  );
  const reviewController = new ReviewController(
    getReviewsByRestaurant,
    createReview,
    reviewRepository
  );
  const chatController = new ChatController(getGeminiResponse);

  // User Auth Endpoints
  app.post('/auth/register', (req, reply) => userController.register(req, reply));
  app.post('/auth/login', (req, reply) => userController.login(req, reply));
  app.post('/auth/google', (req, reply) => userController.googleLogin(req, reply));
  app.post('/auth/logout', (req, reply) => userController.logout(req, reply));

  // Config Endpoint
  app.get('/config', async (req, reply) => {
    return reply.send({ googleClientId: process.env.GOOGLE_CLIENT_ID });
  });

  // Chat Endpoint
  app.post('/chat', (req, reply) => chatController.chat(req, reply));

  // Restaurant Endpoints
  app.get('/restaurants', (req, reply) => restaurantController.getAll(req, reply));
  app.get('/restaurants/:id', (req, reply) => restaurantController.getById(req, reply));
  app.post('/restaurants', { preHandler: [authMiddleware, upload] }, (req, reply) => restaurantController.create(req, reply));
  app.put('/restaurants/:id', { preHandler: [authMiddleware, upload] }, (req, reply) => restaurantController.update(req, reply));
  app.delete('/restaurants/:id', { preHandler: [authMiddleware] }, (req, reply) => restaurantController.delete(req, reply));

  // Review Endpoints
  app.get('/restaurants/:restaurantId/reviews', (req, reply) => reviewController.getByRestaurantId(req, reply));
  app.post('/reviews', { preHandler: [authMiddleware, upload] }, (req, reply) => reviewController.create(req, reply));
  app.put('/reviews/:id', { preHandler: [authMiddleware, upload] }, (req, reply) => reviewController.update(req, reply));
  app.delete('/reviews/:id', { preHandler: [authMiddleware] }, (req, reply) => reviewController.delete(req, reply));
}
