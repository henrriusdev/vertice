// src/lib/utilidades/resolver.ts
import { goto, invalidate, invalidateAll } from '$app/navigation';
import { addToast } from './toast';

export const resolver = (setAction: () => void) => {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	return async ({ result, update }: any) => {
		const { data } = result || {};

		console.log(result)
		if (!data) {
			addToast({ type: 'error', message: 'Respuesta malformada del servidor' });
			console.warn('[resolver] return malformado:', result);
			return;
		}

		if (data.type === 'failure') {
			addToast({ type: 'error', message: data.message });
			return;
		}

		if (data.location) {
			await goto(data.location, { replaceState: true });
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

		if (data.type === 'success' && !data.bypasstoast) {
			addToast({ type: 'success', message: data.message });
		}

		if (data.invalidate === true) {
			await invalidateAll();
		} else if (typeof data.invalidate === 'string') {
			await invalidate(data.invalidate);
		}

		if (update) await update();

		if (setAction) {
			setAction()
		}
	};
};
