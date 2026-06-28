import { FastifyRequest, FastifyReply } from 'fastify';
import { GetRestaurants } from '../../use-cases/restaurant/GetRestaurants';
import { CreateRestaurant } from '../../use-cases/restaurant/CreateRestaurant';
import { UpdateRestaurant } from '../../use-cases/restaurant/UpdateRestaurant';
import { DeleteRestaurant } from '../../use-cases/restaurant/DeleteRestaurant';
import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';

export class RestaurantController {
  constructor(
    private getRestaurants: GetRestaurants,
    private createRestaurant: CreateRestaurant,
    private updateRestaurant: UpdateRestaurant,
    private deleteRestaurant: DeleteRestaurant,
    private restaurantRepository: RestaurantRepository
  ) {}

  async getAll(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const search = (req.query as any).search as string | undefined;
      const restaurants = await this.getRestaurants.execute(search);
      reply.code(200).send({ success: true, data: restaurants });
    } catch (error: any) {
      reply.code(500).send({ success: false, error: error.message });
    }
  }

  async getById(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const id = parseInt((req.params as any).id, 10);
      const restaurant = await this.restaurantRepository.findById(id);
      if (!restaurant) {
        reply.code(404).send({ success: false, error: 'Restaurant not found' });
        return;
      }
      reply.code(200).send({ success: true, data: restaurant });
    } catch (error: any) {
      reply.code(500).send({ success: false, error: error.message });
    }
  }

  async create(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user || user.role !== 'admin') {
        reply.code(403).send({ success: false, error: 'Access denied. Admins only.' });
        return;
      }

      const { name, description, cuisine, address, lat, lng } = req.body as any;
      const file = (req as any).file;
      const imageUrl = file ? `/uploads/${file.filename}` : null;

      const restaurant = await this.createRestaurant.execute({
        name,
        description,
        cuisine,
        address,
        imageUrl,
        lat: lat ? parseFloat(lat) : null,
        lng: lng ? parseFloat(lng) : null,
        createdBy: user.id
      });

      reply.code(201).send({ success: true, data: restaurant });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async update(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user || user.role !== 'admin') {
        reply.code(403).send({ success: false, error: 'Access denied. Admins only.' });
        return;
      }

      const id = parseInt((req.params as any).id, 10);
      const { name, description, cuisine, address, lat, lng } = req.body as any;
      const file = (req as any).file;
      const imageUrl = file ? `/uploads/${file.filename}` : undefined;

      const restaurant = await this.updateRestaurant.execute(id, {
        name,
        description,
        cuisine,
        address,
        imageUrl: imageUrl !== undefined ? imageUrl : null,
        lat: lat ? parseFloat(lat) : null,
        lng: lng ? parseFloat(lng) : null
      });

      reply.code(200).send({ success: true, data: restaurant });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async delete(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user || user.role !== 'admin') {
        reply.code(403).send({ success: false, error: 'Access denied. Admins only.' });
        return;
      }

      const id = parseInt((req.params as any).id, 10);
      await this.deleteRestaurant.execute(id);
      reply.code(200).send({ success: true, message: 'Restaurant deleted successfully' });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }
}
