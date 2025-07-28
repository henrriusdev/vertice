export function getRandomColor() {
	const colors = [
		'blue',
		'green',
		'purple',
		'yellow',
		'red',
		'pink',
		'indigo',
		'gray',
		'orange',
		'cyan',
		'teal',
		'violet',
		'lime',
		'sky',
		'amber'
	];
	return colors[Math.floor(Math.random() * colors.length)];
}
