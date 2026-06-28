export class Restaurant {
  constructor(
    public readonly id: number,
    public readonly name: string,
    public readonly description: string,
    public readonly cuisine: string,
    public readonly address: string,
    public readonly imageUrl: string | null,
    public readonly lat: number | null,
    public readonly lng: number | null,
    public readonly createdBy: number | null,
    public readonly createdAt?: Date
  ) {}
}
