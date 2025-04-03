import { MaskedDynamic } from 'imask';

export const cedulaMask = {
	mask: [
		// V - de 7 a 8 dígitos
		{ mask: 'V-0.000.000', startsWith: 'V', lazy: false, name: 'V7' },
		{ mask: 'V-00.000.000', startsWith: 'V', lazy: false, name: 'V8' },

		// E - de 5 a 10 dígitos
		{ mask: 'E-00.000', startsWith: 'E', lazy: false, name: 'E5' },
		{ mask: 'E-000.000', startsWith: 'E', lazy: false, name: 'E6' },
		{ mask: 'E-0.000.000', startsWith: 'E', lazy: false, name: 'E7' },
    { mask: 'E-00.000.000', startsWith: 'E', lazy: false, name: 'E8' },
    { mask: 'E-000.000.000', startsWith: 'E', lazy: false, name: 'E9' },
    { mask: 'E-0.000.000.000', startsWith: 'E', lazy: false, name: 'E10' },
	],
	lazy: false,
	overwrite: true,
	prepare: (str: string) => str.toUpperCase().replace(/[^VE0-9]/g, ''),
	dispatch: (appended: string, dynamicMasked: MaskedDynamic) => {
		const raw = (dynamicMasked.value + appended).toUpperCase().replace(/[^VE0-9]/g, '');

		const tipo = raw[0];
		const digits = raw.replace(/[^0-9]/g, '');

		if (tipo === 'V') {
			// eslint-disable-next-line
			if (digits.length >= 8) return dynamicMasked.compiledMasks.find((m: any) => m.name === 'V8');
			// eslint-disable-next-line
			return dynamicMasked.compiledMasks.find((m: any) => m.name === 'V7');
		}

    if (tipo === 'E') {
			const name = digits.length > 10 ? 'E10' : `E${digits.length < 5 ? 5 : digits.length}`;
			// eslint-disable-next-line
      return dynamicMasked.compiledMasks.find((m: any) => m.name === name);
		}

		// fallback si aún no hay tipo claro
		return ""
	}
};

export const nota = {
	mask: Number,
	scale: 2,
	padFractionalZeros: true,
	normalizeZeros: true,
	radix: '.',
	mapToRadix: [',', '.'],
	min: 0,
	max: 20,
	autofix: true
}

export const telefono = {
	mask: '(0000) 000-0000',
	autofix: true,
	normalizeZeros: true
}