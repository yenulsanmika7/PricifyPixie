"use client"
import { fetchAmazonProducts, fetchAmazonProductURL } from '@/actions/serverRouting';
import { FormEvent, useState } from 'react'

const Searchbar = ({ products }) => {    
  const [searchPrompt, setSearchPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const isValidAmazonProductURL = (url : string) : boolean => {
    try {
      const parsedURL = new URL(url);
      const hostname = parsedURL.hostname;
      
      if (
        hostname.includes('amazon.com') || 
        hostname.includes('amazon.') || 
        hostname.endsWith('amazon')) {
          return true;        
      }
    } catch (error) {
      return false;      
    }

    return false;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const isValidLink = isValidAmazonProductURL(searchPrompt);
    if (isValidLink) {
      alert(isValidLink ? 'Valid Link.. Success!' : 'Invalid Link! Try with new one:)');
      setIsLoading(true);
      const fetchedProduct = await fetchAmazonProductURL(searchPrompt);
      console.log(fetchedProduct);
      localStorage.setItem('product', fetchedProduct);
    }
    else {
      try {
        setIsLoading(true);
        const fetchedProducts = await fetchAmazonProducts(searchPrompt);
        products(fetchedProducts);
        console.log(fetchedProducts);
      } catch (error) {
          console.log(error);
      } finally {
          setIsLoading(false)
      }
    }    
  }

  return (
    <form className="flex flex-wrap gap-4 mt-12" 
    onSubmit={handleSubmit}
    >
        <input 
        type="text" 
        placeholder="Enter product name or URL"
        onChange={(e) => setSearchPrompt(e.target.value)}
        className="searchbar-input"
        value={searchPrompt}
        />
        
        <button 
        type="submit" 
        className="searchbar-btn"
        disabled={searchPrompt == ''}> 
            {isLoading ? 'Searching...' : 'Search'}
        </button>
    </form>
  )
}

export default Searchbar