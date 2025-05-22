import { writable } from 'svelte/store';

export type Toast = {
	id: number;
	type: 'success' | 'error' | 'info';
	message: string;
};

const store = writable<Toast[]>([]);
let idCounter = 0;

// ✅ función global, sin necesidad de toastStore
export function addToast(toast: Omit<Toast, 'id'>) {
	const id = idCounter++;
	store.update((toasts) => [...toasts, { id, ...toast }]);

	setTimeout(() => {
		store.update((toasts) => toasts.filter((t) => t.id !== id));
	}, 4000);
}

// 👇 Exportar como default para que lo uses directamente
export { store as toasts };
