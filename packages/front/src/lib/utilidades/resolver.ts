// src/lib/utilidades/resolver.ts
import { goto, invalidate, invalidateAll } from '$app/navigation';
import { addToast } from '$lib';
import { fileTypeFromBuffer } from 'file-type';

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
			// Convertir la cadena base64 a un Uint8Array
			const byteCharacters = atob(data.base64);
			const byteArrays = new Uint8Array(byteCharacters.length);
			for (let i = 0; i < byteCharacters.length; i++) {
				byteArrays[i] = byteCharacters.charCodeAt(i);
			}

			// Intentamos detectar el tipo usando file-type a partir de los primeros bytes
			const detectedType = await fileTypeFromBuffer(byteArrays);
			let extension = 'bin';
			if (detectedType && detectedType.ext) {
				extension = detectedType.ext;
			} else {
				// Si file-type no logra determinar el tipo, verificamos si el contenido es texto plano
				const texto = byteArrays.reduce((acc, code) => acc + String.fromCharCode(code), '');
				if (/^[\x20-\x7E\r\n\t]+$/.test(texto)) {
					// Es un archivo de texto, ahora comprobamos si puede ser CSV
					const lines = texto.split(/\r?\n/);
					// Tomamos la primera línea no vacía para analizar
					const firstLine = lines.find(line => line.trim() !== "");
					if (firstLine) {
						// Contamos delimitadores comunes (coma o punto y coma)
						const commaCount = firstLine.split(',').length - 1;
						const semicolonCount = firstLine.split(';').length - 1;
						if (commaCount >= 1 || semicolonCount >= 1) {
							extension = 'csv';
						} else {
							extension = 'txt';
						}
					} else {
						extension = 'txt';
					}
				} else {
					// Como fallback final, se extrae la extensión del MIME type enviado por el backend
					extension = data.type.split('/')[1] || 'bin';
				}
			}

			// Creación del blob y descarga del archivo
			const blob = new Blob([byteArrays], { type: data.type });
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
