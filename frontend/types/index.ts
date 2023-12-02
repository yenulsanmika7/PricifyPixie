export type Product = {
  id: number;
  name: string;
  price: string;
  stars: string;
  rating_count: string[];
  feature_bullets: string[];
  images: {
    hiRes: string;
    thumb: string;
    large: string;
    main: { [key: string]: [number, number] };
    variant: string;
    lowRes: null;
    shoppableScene: null;
  }[];
  variant_data: string;
  product_url: string;
};
