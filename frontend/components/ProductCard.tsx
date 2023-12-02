import { Product } from '@/types';
import Image from 'next/image';
import Link from 'next/link';
import React from 'react'

interface Props {
  product: Product;
}
 
const ProductCard = ({ product }: Props) => {
  const hiResUrl = product.images[0].hiRes == null ? product.images[0].large : product.images[0].hiRes;

  return (
    <Link href={`/products/${product.id}`} className="product-card">
      <div className="product-card_img-container">
        <Image 
          src={hiResUrl}
          alt={product.name}
          width={200}
          height={200}
          className="product-card_img"
        />
      </div>

      <div className="flex flex-col gap-3">
        <h3 className="product-title">{product.name}</h3>

        <div className="flex justify-between">
          <p className="text-black opacity-50 text-lg capitalize">
            {product.stars}
          </p>

          <p className="text-black text-lg font-semibold">
            <span>{product?.price}</span>
          </p>
        </div>
      </div>
    </Link>
  )
}

export default ProductCard