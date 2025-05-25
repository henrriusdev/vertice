import { MaskedDynamic } from 'imask';

export const cedulaMask = {
	mask: [
		{ mask: 'V-0000000', name: 'V7' },
		{ mask: 'V-00000000', name: 'V8' },
		{ mask: 'E-00000', name: 'E5' },
		{ mask: 'E-000000', name: 'E6' },
		{ mask: 'E-0000000', name: 'E7' },
		{ mask: 'E-00000000', name: 'E8' },
		{ mask: 'E-000000000', name: 'E9' },
		{ mask: 'E-0000000000', name: 'E10' }
	],
	lazy: false,
	overwrite: true,
	dispatch: (appended: string, dynamicMasked: MaskedDynamic) => {
		const raw = (dynamicMasked.value + appended).replace(/[^VE0-9]/gi, '').toUpperCase();
		const tipo = raw[0];
		const digits = raw.slice(1).replace(/\D/g, '');
		const len = digits.length;

		if (tipo === 'V') {
			if (len === 7) return dynamicMasked.compiledMasks.find((m) => m.name === 'V7');
			if (len === 8) return dynamicMasked.compiledMasks.find((m) => m.name === 'V8');
		}

		if (tipo === 'E') {
			if (len >= 5 && len <= 10)
				return dynamicMasked.compiledMasks.find((m) => m.name === `E${len}`);
		}

		return dynamicMasked.compiledMasks[0];
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