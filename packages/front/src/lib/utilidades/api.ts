import { goto } from '$app/navigation';
import { browser } from '$app/environment';

// Track consecutive 401 errors to avoid redirecting on temporary issues
let consecutiveAuthErrors = 0;
const MAX_AUTH_ERRORS_BEFORE_LOGOUT = 3;

/**
 * Enhanced fetch wrapper that handles authentication errors
 * Automatically redirects to logout only after multiple 401 responses
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
            consecutiveAuthErrors++;
            
            // Only redirect to logout after multiple consecutive failures
            if (consecutiveAuthErrors >= MAX_AUTH_ERRORS_BEFORE_LOGOUT && browser) {
                console.warn(`Session expired after ${consecutiveAuthErrors} consecutive 401 errors, redirecting to logout...`, {
                    url: input.toString(),
                    method: init?.method || 'GET'
                });
                consecutiveAuthErrors = 0; // Reset counter
                goto('/logout');
            } else {
                console.warn(`Authentication error ${consecutiveAuthErrors}/${MAX_AUTH_ERRORS_BEFORE_LOGOUT}`, {
                    url: input.toString(),
                    method: init?.method || 'GET'
                });
            }
            
            return response;
        } else {
            // Reset error counter on successful requests
            consecutiveAuthErrors = 0;
        }
        
        return response;
    } catch (error) {
        // Reset error counter on network errors (not auth related)
        consecutiveAuthErrors = 0;
        
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