import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';
import { Restaurant } from '../../domain/entities/Restaurant';

export class CreateRestaurant {
  constructor(private restaurantRepository: RestaurantRepository) {}

  async execute(data: {
    name: string;
    description: string;
    cuisine: string;
    address: string;
    imageUrl: string | null;
    lat: number | null;
    lng: number | null;
    createdBy: number;
  }): Promise<Restaurant> {
    if (!data.name || !data.description || !data.cuisine || !data.address) {
      throw new Error('Name, description, cuisine, and address are required');
    }

    return this.restaurantRepository.create({
      name: data.name,
      description: data.description,
      cuisine: data.cuisine,
      address: data.address,
      imageUrl: data.imageUrl,
      lat: data.lat,
      lng: data.lng,
      createdBy: data.createdBy
    });
  }
}
