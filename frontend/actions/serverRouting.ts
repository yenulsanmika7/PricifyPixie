import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

export const fetchAmazonProducts = async (keyword: string) => {
    try {
        const response = await api.get(`/amazon_scraper/search_keyword=${keyword}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching data from the backend:', error);
        throw error;
    }
};

export const fetchAmazonProductURL = async (url: string) => {
    try {
        const response = await api.get(`/amazon_scraper/product_url=${url}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching data from the backend:', error);
        throw error;
    }
};

export const fetchAmazonProductByID = async (id: string) => {
    try {
        const response = await api.get(`/amazon_scraper/product=${id}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching data from the backend:', error);
        throw error;
    }
};

export const trackProduct = async (productId: string, email: string) => {
    try {
        const response = await api.get(`/amazon_scraper/tracked_product=${productId}&user_email=${email}`);
        return response.data;
    } catch (error) {
        console.error(`Error while adding product (${productId}) to TrackedProduct database as Tracked product:`, error);
        throw error;
    }
};

export const getTrackedProducts = async () => {
    try {
        const response = await api.get(`/amazon_scraper/all_tracked_products`);
        return response.data;
    } catch (error) {
        console.error(`No tracked Products`, error);
        throw error;
    }
};

