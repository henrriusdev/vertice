<script lang="ts">
	import { cedulaMask, Datepicker } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Breadcrumb,
		BreadcrumbItem,
		Button,
		Card,
		Heading,
		Input,
		Label,
		Navbar,
		NavBrand,
		Select,
		Toggle
	} from 'flowbite-svelte';

	import {
		ArrowRightOutline,
		FileLinesOutline,
		PlusOutline,
		SearchOutline
	} from 'flowbite-svelte-icons';

	// Using Svelte 5 runes for state management
	let searchQuery = $state('');
	let currentCycleOnly = $state(true);
	let reportType = $state('day');
	let paymentSelection = $state('all');
	let paymentDate = $state(new Date());

	// Report types
	const reportTypes = [
		{ value: 'day', name: 'Día' },
		{ value: 'week', name: 'Semana' },
		{ value: 'month', name: 'Mes' }
	];

	// Payment selections
	const paymentSelections = [
		{ value: 'all', name: 'Todos' },
		{ value: 'pending', name: 'Pendientes' },
		{ value: 'completed', name: 'Completados' }
	];

	// Functions
	function viewPayment() {
		if (searchQuery) {
			alert('Ver pago: ' + searchQuery);
		} else {
			alert('Por favor ingrese un término de búsqueda');
		}
	}

	function generateReport() {
		alert(`Generando reporte: Tipo=${reportType}, Pagos=${paymentSelection}, Fecha=${paymentDate}`);
	}

	function registerPayment() {
		alert('Registrar nuevo pago');
	}

	// Effect example - log state changes
	$effect(() => {
		console.log('Current search query:', searchQuery);
		console.log('Current cycle only:', currentCycleOnly);
	});
</script>

<div class="w-full h-full flex items-center justify-around relative">
	<div class="flex justify-end mb-6 absolute top-0 right-0">
		<Button color="blue" size="lg" on:click={registerPayment}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Registrar Pago
		</Button>
	</div>

	<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		<!-- Search Payments Section -->
		<Card padding="xl">
			<Heading tag="h2" class="text-2xl font-bold text-blue-600 mb-6">Buscar Pagos</Heading>

			<div class="space-y-6">
				<div>
					<Label for="search-payments" class="mb-2">Seleccione el estudiante</Label>
					<div class="relative">
						<span class="absolute inset-y-0 left-0 flex items-center pl-2">
							<SearchOutline class="h-5 w-5 text-gray-400" />
						</span>
						<input
							id="search-payments"
							placeholder="Buscar pagos..."
							bind:value={searchQuery}
							use:imask={cedulaMask as any}
							class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 pl-10"
						/>
					</div>
				</div>

				<div class="flex items-center">
					<Toggle bind:checked={currentCycleOnly} class="mr-3" />
					<Label>Pagos del ciclo actual</Label>
				</div>

				<Button
					color="primary"
					size="lg"
					class="w-full"
					on:click={viewPayment}
					disabled={!searchQuery}
				>
					Ver pago
				</Button>
			</div>
		</Card>

		<!-- Reports Section -->
		<Card padding="xl">
			<Heading tag="h2" class="text-2xl font-bold text-blue-600 mb-6">Reportes</Heading>

			<div class="space-y-6">
				<div>
					<Label for="report-type" class="mb-2">Seleccione su tipo de reporte</Label>
					<Select id="report-type" items={reportTypes} bind:value={reportType} />
				</div>

				<div>
					<Label for="payment-selection" class="mb-2"
						>¿Cuáles pagos desea que estén en el reporte?</Label
					>
					<Select id="payment-selection" items={paymentSelections} bind:value={paymentSelection} />
				</div>

				<div>
					<Label for="payment-date" class="mb-2">Fecha de pagos</Label>
					<Datepicker
						id="payment-date"
						bind:value={paymentDate}
						maxDate={new Date()}
						placeholder="dd/mm/aaaa"
					/>
				</div>

				<Button
					color="primary"
					size="lg"
					class="w-full"
					on:click={generateReport}
					disabled={!paymentDate}
				>
					<FileLinesOutline class="mr-2 h-5 w-5" />
					Generar reporte
				</Button>
			</div>
		</Card>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		font-family: 'Inter', sans-serif;
	}
</style>
