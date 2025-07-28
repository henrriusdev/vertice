import { goto, invalidate, invalidateAll } from '$app/navigation';
import { addToast } from '$lib';
import { fileTypeFromBuffer } from 'file-type';

export const resolver = (setAction: () => void) => {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	return async ({ result, update }: any) => {
		const { data } = result || {};

		if (!data) {
			addToast({ type: 'error', message: 'Respuesta malformada del servidor' });
			console.warn('[resolver] return malformado:', result);
			return;
		}

		if (data.type === 'failure') {
			addToast({ type: 'error', message: data.message });
			if (setAction) {
				setAction()
			}
			return;
		}

		if (data.location) {
			await goto(data.location, { replaceState: true });
		}

		// 🎯 Si incluye base64 → generar archivo
		if (data.base64 && data.type) {
			// Convert base64 to Uint8Array for file-type detection
			const byteCharacters = atob(data.base64);
			const byteArrays = new Uint8Array(byteCharacters.length);
			for (let i = 0; i < byteCharacters.length; i++) {
				byteArrays[i] = byteCharacters.charCodeAt(i);
			}

			// Default extension
			let extension = 'bin';

			// Try to detect file type using file-type library
			try {
				const detectedType = await fileTypeFromBuffer(byteArrays);
				
				if (detectedType && detectedType.ext) {
					extension = detectedType.ext;
				} else {
					if (byteArrays.length >= 5 &&
						byteArrays[0] === 0x25 && // %
						byteArrays[1] === 0x50 && // P
						byteArrays[2] === 0x44 && // D
						byteArrays[3] === 0x46 && // F
						byteArrays[4] === 0x2D) {  // -
						extension = 'pdf';
					} else if (data.type.includes('pdf')) {
						extension = 'pdf';
					} else {
						const mimeExtension = data.type.split('/')[1];
						if (mimeExtension && !mimeExtension.includes(';')) {
							extension = mimeExtension === 'plain' ? 'txt' : mimeExtension;
						}
					}
				}
			} catch (error) {
				console.error('Error detecting file type:', error);
				
				// Fallback to MIME type if detection fails
				if (data.type.includes('pdf')) {
					extension = 'pdf';
				} else {
					const mimeExtension = data.type.split('/')[1];
					if (mimeExtension && !mimeExtension.includes(';')) {
						extension = mimeExtension;
					}
				}
			}

			// Creación del blob y descarga del archivo
			const blob = new Blob([byteArrays], { type: data.type });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `${data?.filename ?? 'reporte'}.${extension}`;
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
