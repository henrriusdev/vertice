import { goto } from '$app/navigation';
import { browser } from '$app/environment';

/**
 * Enhanced fetch wrapper that handles authentication errors
 * Automatically redirects to logout on 401 responses
 */
export async function apiCall(
    fetch: typeof window.fetch,
    input: RequestInfo | URL,
    init?: RequestInit
): Promise<Response> {
    try {
        const response = await fetch(input, init);
        
        // Handle 401 Unauthorized responses
        if (response.status === 401) {
            // Only redirect to logout in browser environment
            if (browser) {
                console.warn('Session expired (401), redirecting to logout...', {
                    url: input.toString(),
                    method: init?.method || 'GET'
                });
                // Clear any existing session data immediately
                if (typeof document !== 'undefined') {
                    // Clear cookies
                    document.cookie = 'sesion=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                }
                // Redirect to logout
                goto('/logout');
            }
            // Still return the response so callers can handle it if needed
            return response;
        }
        
        return response;
    } catch (error) {
        // Log network errors for debugging
        console.error('Network error in API call:', {
            url: input.toString(),
            method: init?.method || 'GET',
            error: error
        });
        // Re-throw network or other errors
        throw error;
    }
}

/**
 * API call wrapper that also parses JSON and handles common error scenarios
 */
export async function apiJson<T = any>(
    fetch: typeof window.fetch,
    input: RequestInfo | URL,
    init?: RequestInit
): Promise<T> {
    const response = await apiCall(fetch, input, init);
    
    if (!response.ok) {
        // For 401 errors, let the user see the logout process
        if (response.status === 401) {
            throw new Error('Su sesión ha expirado. Será redirigido al inicio de sesión.');
        }
        
        const error = await response.json().catch(() => ({ data: { message: 'Error en la respuesta del servidor' } }));
        
        // Enhanced error handling with error codes
        if (error?.data?.error_code) {
            throw {
                message: error.data.message || `HTTP ${response.status}: ${response.statusText}`,
                code: error.data.error_code,
                status: response.status
            };
        }
        
        throw new Error(error?.data?.message || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
}