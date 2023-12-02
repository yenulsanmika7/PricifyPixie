"use client"
import { fetchAmazonProductByID, trackProduct } from "@/actions/serverRouting";
import { redirect } from "next/navigation";
import Image from "next/image"
import Link from "next/link";
import { MouseEventHandler, useState } from 'react'
import Modal from "@/components/Modal";

type Props =  {
    params: { id: string }
}

const ProductDetails = async ({ params: { id } } : Props) => {
  const productId = id;
  const product = await fetchAmazonProductByID(productId);

  if (!product) redirect('/')

  const hiResUrl = product.images[0].hiRes == null ? product.images[0].large : product.images[0].hiRes;
  const matches = product.rating_count.match(/^([\d,]+)\s/);
  let rating_count = 0

  if (matches) {
    const numericPart = matches[1];
    rating_count = parseInt(numericPart.replace(/,/g, ''), 10);
  } else {
    console.log("No match found.");
  }
  

  return (
    <div className="product-container">
        <div className="flex gap-28 xl:flex-row flex-col">
            <div>
                <Image
                src={hiResUrl}    
                alt={product.name}    
                width={450}
                height={400}
                className="mx-auto"        
                />
            </div>

            <div className="flex-1 flex flex-col">
              <div className="flex justify-between items-start gap-5 flex-wrap pb-6">
                <div className="flex flex-col gap-3">
                  <p className="text-[24px] text-secondary font-semibold">{product.name}</p>

                  <Link
                  href={product.product_url}
                  target="_blank"
                  className="text-base text-black opacity-50" >
                    Visit Product
                  </Link>

                  <div className="flex items-center gap-3">
                    <div className="product-hearts">
                        <Image 
                        src="/assets/icons/red-heart.svg" 
                        alt="heart" 
                        width={20}
                        height={20}
                        />

                      <p className="text-base font-semibold text-[#D46F77]">{rating_count}</p>
                    </div>

                    <div className="p-2 bg-white-200 rounded-10">
                      <Image
                       src="/assets/icons/bookmark.svg"
                       alt="bookmark"
                       width={20}
                       height={20}
                      />
                    </div> 

                    <div className="p-2 bg-white-200 rounded-10">
                      <Image
                       src="/assets/icons/share.svg"
                       alt="share"
                       width={20}
                       height={20}
                      />
                    </div> 

                  </div>
                </div>
              </div>

              <div className="product-info">
                <div className="flex flex-col gap-2">
                  <p className="text-[34px] text-secondary font-bold">{product.price}</p>
                </div>

                <div className="flex flex-col gap-4">
                  <div className="flex gap-3">
                    <div className="product-reviews">
                      <Image 
                      src="/assets/icons/comment.svg"
                      alt="question"     
                      width={16}
                      height={16}                 
                      />
                      <p className="text-sm text-secondary font-semibold">{product.question_count} Questions</p>
                    </div>
                  </div>                  
                </div>
              </div>    

              <Modal productId={id} />       
            </div>
        </div>
        <div className="flex flex-col gap-16 pt-10 ">
          <div className="flex flex-col gap-5 pt-6">
                <h3 className="text-2xl text-secondary font-semibold">Product Description</h3>

                <div className="flex flex-col gap-4">
                  {product?.description}
                </div>
              </div>
          </div>
    </div>
  )
}

export default ProductDetails