<script lang="ts">
	import { cedulaMask, Datepicker } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Breadcrumb,
		BreadcrumbItem,
		Button,
		ButtonGroup,
		Card,
		Heading,
		Input,
		Label,
		Modal,
		Navbar,
		NavBrand,
		Select,
		Toggle
	} from 'flowbite-svelte';

	import {
		ArrowRightOutline,
		CreditCardOutline,
		FileLinesOutline,
		PlusOutline,
		SearchOutline
	} from 'flowbite-svelte-icons';

	// Main view state
	let searchQuery = $state('');
	let currentCycleOnly = $state(true);
	let reportType = $state('day');
	let paymentSelection = $state('all');
	let reportDate = $state(new Date());

	// Modal state
	let showPaymentModal = $state(false);
	
	// Payment form state
	let student = $state('');
	let paymentConcept = $state('pre-inscription');
	let paymentDate = $state<Date | null>(null);
	let paymentMethod = $state('transfer');
	let amount = $state('');

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
	
	// Payment concepts
	const paymentConcepts = [
		{ value: 'pre-inscription', name: 'Pre Inscripción' },
		{ value: 'monthly-fee', name: 'Mensualidad' },
		{ value: 'materials', name: 'Materiales' },
		{ value: 'other', name: 'Otro' }
	];

	// Derived state for form validation
	const isFormValid = $derived(
		student.trim() !== '' && 
		paymentConcept !== '' && 
		paymentDate !== null && 
		paymentMethod !== '' && 
		amount.trim() !== ''
	);

	// Functions for main view
	function viewPayment() {
		if (searchQuery) {
			alert('Ver pago: ' + searchQuery);
		} else {
			alert('Por favor ingrese un término de búsqueda');
		}
	}

	function generateReport() {
		alert(`Generando reporte: Tipo=${reportType}, Pagos=${paymentSelection}, Fecha=${reportDate}`);
	}
	
	// Functions for payment form
	function openPaymentModal() {
		// Reset form fields when opening modal
		student = '';
		paymentConcept = 'pre-inscription';
		paymentDate = null;
		paymentMethod = 'transfer';
		amount = '';
		showPaymentModal = true;
	}
	
	function closePaymentModal() {
		showPaymentModal = false;
	}
	
	function submitPayment() {
		if (isFormValid) {
			alert(`Pago registrado:
				Estudiante: ${student}
				Concepto: ${paymentConcept}
				Fecha: ${paymentDate?.toLocaleDateString()}
				Método: ${paymentMethod}
				Monto: ${amount} Bs.`);
			closePaymentModal();
		} else {
			alert('Por favor complete todos los campos requeridos');
		}
	}
	
	function selectPaymentMethod(method: string) {
		paymentMethod = method;
	}

	// Effect example - log state changes
	$effect(() => {
		console.log('Current search query:', searchQuery);
		console.log('Current cycle only:', currentCycleOnly);
	});
</script>

<div class="w-full h-full flex items-center justify-around relative">
	<div class="flex justify-end mb-6 absolute top-0 right-0">
		<Button color="blue" size="lg" on:click={openPaymentModal}>
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
					<Label for="report-date" class="mb-2">Fecha de pagos</Label>
					<Datepicker
						id="report-date"
						bind:value={reportDate}
						maxDate={new Date()}
						placeholder="dd/mm/aaaa"
					/>
				</div>

				<Button
					color="primary"
					size="lg"
					class="w-full"
					on:click={generateReport}
					disabled={!reportDate}
				>
					<FileLinesOutline class="mr-2 h-5 w-5" />
					Generar reporte
				</Button>
			</div>
		</Card>
	</div>
	
	<!-- Payment Form Modal -->
	<Modal title="Formulario de Pago" bind:open={showPaymentModal} size="md" autoclose>
		<div class="space-y-5 space-x-5 grid md:grid-cols-2">
			<!-- Student Field -->
			<div>
				<Label for="student" class="mb-2 font-medium">Estudiante</Label>
				<div class="relative">
					<span class="absolute inset-y-0 left-0 flex items-center pl-2">
						<SearchOutline class="h-5 w-5 text-gray-400" />
					</span>
					<input
						id="student"
						placeholder="Buscar estudiante..."
						bind:value={student}
						use:imask={cedulaMask as any}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 pl-10"
					/>
				</div>
			</div>
			
			<!-- Payment Concept -->
			<div>
				<Label for="payment-concept" class="mb-2 font-medium">Concepto del pago</Label>
				<Select 
					id="payment-concept" 
					items={paymentConcepts} 
					bind:value={paymentConcept}
					class="bg-purple-50 border-purple-200"
				/>
			</div>
			
			<!-- Payment Date -->
			<div>
				<Label for="payment-date" class="mb-2 font-medium">Fecha del Pago</Label>
				<Datepicker
					id="payment-date"
					bind:value={paymentDate}
					maxDate={new Date()}
					placeholder="dd/mm/aaaa"
				/>
			</div>

			<div>
				<Label for="amount" class="mb-2 font-medium">Monto (Bs.)</Label>
				<Input 
					id="amount" 
					type="number" 
					placeholder="Monto" 
					bind:value={amount}
					class="bg-purple-50 border-purple-200"
				/>
			</div>
			
			<!-- Payment Method -->
			<div class="md:col-span-2">
				<Label class="mb-2 font-medium">Método de Pago</Label>
				<div class="flex w-full">
					<ButtonGroup class="w-full">
						<Button 
							color={paymentMethod === 'transfer' ? 'purple' : 'light'} 
							class="flex-1"
							type="button"
							on:click={() => selectPaymentMethod('transfer')}
						>
							Transferencia
						</Button>
						<Button 
							color={paymentMethod === 'cash' ? 'purple' : 'light'} 
							class="flex-1"
							type="button"
							on:click={() => selectPaymentMethod('cash')}
						>
							Efectivo
						</Button>
						<Button 
							color={paymentMethod === 'point' ? 'purple' : 'light'} 
							class="flex-1"
							type="button"
							on:click={() => selectPaymentMethod('point')}
						>
							Punto
						</Button>
					</ButtonGroup>
				</div>
			</div>
			
		</div>
		
		<!-- Modal Footer -->
		<svelte:fragment slot="footer">
			<Button color="alternative" on:click={closePaymentModal}>Cancelar</Button>
			<Button 
				color="primary" 
				on:click={submitPayment}
				disabled={!isFormValid}
			>
				<CreditCardOutline class="mr-2 h-5 w-5" />
				Realizar Pago
			</Button>
		</svelte:fragment>
	</Modal>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		font-family: 'Inter', sans-serif;
	}
	
	/* Custom styling for Flatpickr */
	:global(.flatpickr-calendar) {
		border-radius: 0.5rem;
		box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
	}
	
	:global(.flatpickr-day.selected) {
		background: #9333ea !important;
		border-color: #9333ea !important;
	}
	
	:global(.flatpickr-day:hover) {
		background: #f3e8ff !important;
	}
</style>