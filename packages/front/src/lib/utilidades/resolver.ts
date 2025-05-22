// src/lib/utilidades/resolver.ts
import { invalidate, invalidateAll, goto } from '$app/navigation';
import { addToast } from '$lib/utilidades/toast.svelte';

export const resolver = (action?: boolean) => {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	return async ({ result, update }: any) => {
		const { data, type } = result || {};

		if (!data || typeof data.message !== 'string') {
			addToast({ type: 'error', message: 'Respuesta malformada del servidor' });
			console.warn('[resolver] return malformado:', result);
			return;
		}

		if (type === 'failure') {
			addToast({ type: 'error', message: data.message });
			return;
		}

		// 🎯 Si incluye base64 → generar archivo
		if (data.base64 && data.type) {
			const byteCharacters = atob(data.base64);
			const byteArrays = new Uint8Array(byteCharacters.length);

			for (let i = 0; i < byteCharacters.length; i++) {
				byteArrays[i] = byteCharacters.charCodeAt(i);
			}

			const blob = new Blob([byteArrays], { type: data.type });
			const extension = data.type.split('/')[1] || 'bin';

			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `reporte.${extension}`;
			a.click();
			URL.revokeObjectURL(url);
		}

		addToast({ type: 'success', message: data.message });

		if (data.invalidate === true) {
			await invalidateAll();
		} else if (typeof data.invalidate === 'string') {
			await invalidate(data.invalidate);
		}

		if (update) await update();

		if (action) {
			action = true
		}
	};
};
