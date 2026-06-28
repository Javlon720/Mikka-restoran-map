import { Restaurant } from '../entities/Restaurant';

export interface RestaurantRepository {
  findAll(search?: string): Promise<Restaurant[]>;
  findById(id: number): Promise<Restaurant | null>;
  create(restaurant: Omit<Restaurant, 'id' | 'createdAt'>): Promise<Restaurant>;
  update(restaurant: Restaurant): Promise<Restaurant>;
  delete(id: number): Promise<boolean>;
}
