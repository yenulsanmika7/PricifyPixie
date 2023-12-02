"use client";
import HeroCarousel from '@/components/HeroCarousel'
import Searchbar from '@/components/Searchbar'
import ProductCard from "@/components/ProductCard"
import Image from 'next/image'
import { useState } from 'react'
import { Product } from '@/types';

interface Props {
  product: Product;
}

const Home = () => {
  let [products, setProducts] = useState<Product[]>([]);

  return (
    <>
      <section className="px-6 md:px-20 py-24">
        <div className="flex max-xl:flex-col gap-16">
          <div className="flex flex-col justify-center">
            <p className="small-text font-Inter">
              Smart Shopping Starts Here
              <Image 
                src="assets/icons/arrow-right.svg"
                alt="arrow-right"
                width={16}
                height={16}
              ></Image>
            </p>

            <h1 className="head-text">
              Unleash the Power of
              <span className="text-primary"> PriceWise</span>
            </h1>

            <p className="mt-6 font-Inter">Powerful, self-serve product and growth analytics to help you convert, engage, and retain more.</p>

            <Searchbar products={setProducts} />
          </div>

          <HeroCarousel />
        </div>
      </section>

      {products.length > 0 && (
        <section className='search-section'>
          <h2 className="section-text">Searched Results</h2>
  
          <div className='flex flex-wrap gap-x-20 gap-y-16'>
            {products.map((product) => (
              <ProductCard key={product.name} product={product} />
            ))}
          </div>
        </section>
      )}
    </>
  )
}

export default Home