"use client"

import "react-responsive-carousel/lib/styles/carousel.min.css";
import { Carousel } from 'react-responsive-carousel';
import Image from 'next/image';

const heroImages = [
  { imgUrl: '/assets/images/hero-3.png', alt: "smart-watch" },
  { imgUrl: '/assets/images/hero-2.png', alt: "lamp" },
  { imgUrl: '/assets/images/hero-2.png', alt: "macbook" },
  { imgUrl: '/assets/images/hero-2.png', alt: "chair" },
];

function HeroCarousel() {

  return (
    <div className="hero-carousel">
      <Carousel showThumbs={false} autoPlay infiniteLoop interval={2000} showArrows={false} showStatus={false}>
        {heroImages.map((image) => (
          <Image 
            src={image.imgUrl}
            alt={image.alt}
            width={100}
            height={100}
            className='object-contain'
            key={image.alt}
          />
        ))}
      </Carousel>

      <Image 
        src="/assets/images/hand-drawn-arrow.svg"
        alt="arrow"
        width={175}
        height={175}
        className="max-xl:hidden absoulute -left-[15%] bottom-0 z-0"
      />
    </div>
  );
}

export default HeroCarousel;
