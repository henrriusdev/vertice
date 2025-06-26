<script lang="ts">
	import { cedulaMask, Datepicker } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Button,
		ButtonGroup,
		Card,
		Heading,
		Input,
		Label,
		Modal,
		Select,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Toggle
	} from 'flowbite-svelte';
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';

	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';
	import {
               CreditCardOutline,
               PlusOutline,
               SearchOutline,
               TrashBinOutline
        } from 'flowbite-svelte-icons';
	import type { PageServerData } from './$types';
	import { goto } from '$app/navigation';
	import { resolver } from '$lib/utilidades/resolver';

	let { data }: { data: PageServerData } = $props();

	// Main view state
	let searchQuery = $state('');
	let currentCycleOnly = $state(true);

	// Payment concepts
	const paymentConcepts = [
		{ value: 'inscripcion', name: 'Inscripción' },
		{ value: 'servicios', name: 'Servicios Estudiantiles' },
		{ value: 'cuota1', name: 'Cuota 1' },
		{ value: 'cuota2', name: 'Cuota 2' },
		{ value: 'cuota3', name: 'Cuota 3' },
		{ value: 'cuota4', name: 'Cuota 4' },
		{ value: 'cuota5', name: 'Cuota 5' }
	];

	let serial: string = $state('');
	let monto: number = $state(1);
	let billetes: { serial: string; monto: number }[] = $state([]);

	// Derived state for form validation
        const isFormValid = $derived(
                student.trim() !== '' &&
                        paymentConcept !== '' &&
                        paymentDate !== null &&
                        paymentMethod !== '' &&
                        amount !== '' &&
                        exchangeRate !== ''
        );

        $effect(() => {
                if (!showPaymentModal) {
                        // Reset form fields when modal is closed
                        student = '';
                       paymentConcept = 'inscripcion';
                        paymentDate = null;
                        paymentMethod = 'transfer';
                        amount = '';
                        exchangeRate = '';
                        billetes = [];
                        serial = '';
                }
        });


	// Functions for payment form
        function openPaymentModal() {
                // Reset form fields when opening modal
                student = '';
                paymentConcept = 'inscripcion';
                paymentDate = null;
                paymentMethod = 'transfer';
                amount = '';
                exchangeRate = '';
                showPaymentModal = true;
        }

	function closePaymentModal() {
		showPaymentModal = false;
	}

	$inspect(paymentDate)
	const handleSubmit: SubmitFunction = ({ formData, cancel }) => {
		// Validación de campos
		
		if (!student.includes('-')) {
			alert('Por favor, seleccione si el estudiante es extranjero o no');
			return cancel();
		}
		
		if (!data.estudiantes.includes(student)) {
			alert('No hay algún estudiante con esa cédula en nuestro sistema');
			return cancel();
		}

		// Agrega campos dinámicos
		if (paymentMethod === 'cash') {
			for (const billete of billetes) {
				formData.append('billetes', JSON.stringify(billete));
			}
		}

		if (paymentMethod === 'transfer') {
			const refInput = document.getElementById('payment-reference') as HTMLInputElement;
			if (!refInput?.value.trim()) {
				alert('Por favor, introduzca la referencia de transferencia');
				return cancel();
			}
			formData.append('referencia_transferencia', refInput.value.trim());
		}

                formData.append('payment-method', paymentMethod);
                formData.append('tasa_divisa', exchangeRate);

		// fecha formateada
		if (paymentDate) {
			formData.append('fecha_pago', paymentDate.toISOString().split('T')[0]);
		}

               return resolver(() => closePaymentModal());
	};

	function agregarBillete() {
		billetes.push({ serial: serial, monto: monto });
	}

	function borrarBillete(i: number) {
		billetes = billetes.filter((bil, index) => i !== index);
	}

	function selectPaymentMethod(method: string) {
		paymentMethod = method;
	}

	function viewPayment() {
		if (!searchQuery) return;
		const params = new URLSearchParams();
		if (currentCycleOnly) params.set('ciclo_actual', 'true');
		searchQuery = searchQuery.split('_')[0]
		goto(`/caja/pagos/${searchQuery}?${params.toString()}`);
	}
</script>

<div class="w-full h-full flex items-center justify-around relative">
	<div class="flex justify-end mb-6 absolute top-0 right-0">
		<Button color="blue" size="lg" onclick={openPaymentModal}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Registrar Pago
		</Button>
	</div>

	<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		<!-- Search Payments Section -->
		<Card class="p-6">
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
					onclick={viewPayment}
					disabled={!searchQuery}
				>
					Ver pago
				</Button>
			</div>
		</Card>

	</div>

	<!-- Payment Form Modal -->
	<Modal title="Formulario de Pago" bind:open={showPaymentModal} size="md">
		<form
			bind:this={form}
			method="post"
			use:enhance={handleSubmit}
			action="?/crear"
			class="space-y-5 space-x-5 grid md:grid-cols-6"
		>
			<!-- Student Field -->
			<div class="md:col-span-3">
				<Label for="student" class="mb-2 font-medium">Estudiante</Label>
				<div class="relative">
					<span class="absolute inset-y-0 left-0 flex items-center pl-2">
						<SearchOutline class="h-5 w-5 text-gray-400" />
					</span>
					<input
						id="student"
						name="student"
						placeholder="Buscar estudiante..."
						bind:value={student}
						use:imask={cedulaMask as any}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 pl-10"
					/>
				</div>
			</div>

			<!-- Payment Concept -->
			<div class="md:col-span-3">
				<Label for="payment-concept" class="mb-2 font-medium">Concepto del pago</Label>
				<Select
					id="payment-concept"
					name="payment-concept"
					items={paymentConcepts}
					bind:value={paymentConcept}
					class="bg-purple-50 border-purple-200"
				/>
			</div>

			<!-- Payment Date -->
			<div class="md:col-span-3">
				<Label for="payment-date" class="mb-2 font-medium">Fecha del Pago</Label>
				<Datepicker
					bind:value={paymentDate}
					maxYear={new Date().getFullYear()}
				/>
				<input type="hidden" name="payment-date" value={paymentDate?.toISOString().split('T')[0] ?? ''} />
			</div>

                        <div class="md:col-span-3">
                                <Label for="amount" class="mb-2 font-medium">Monto (Bs.)</Label>
                                <Input
                                        id="amount"
                                        name="amount"
                                        type="number"
                                        placeholder="Monto"
                                        bind:value={amount}
                                        class="bg-purple-50 border-purple-200"
                                />
                        </div>

                        <div class="md:col-span-3">
                                <Label for="exchange" class="mb-2 font-medium">Tasa de cambio ($)</Label>
                                <Input
                                        id="exchange"
                                        name="tasa_divisa"
                                        type="number"
                                        step="0.01"
                                        placeholder="Tasa"
                                        bind:value={exchangeRate}
                                        class="bg-purple-50 border-purple-200"
                                />
                        </div>

			<!-- Payment Method -->
			<div class="md:col-span-full">
				<Label class="mb-2 font-medium">Método de Pago</Label>
				<div class="flex w-full">
					<ButtonGroup class="w-full">
						<Button
							color={paymentMethod === 'transfer' ? 'purple' : 'light'}
							class="flex-1"
							type="button"
							onclick={() => selectPaymentMethod('transfer')}
						>
							Transferencia
						</Button>
						<Button
							color={paymentMethod === 'cash' ? 'purple' : 'light'}
							class="flex-1"
							type="button"
							onclick={() => selectPaymentMethod('cash')}
						>
							Efectivo
						</Button>
						<Button
							color={paymentMethod === 'point' ? 'purple' : 'light'}
							class="flex-1"
							type="button"
							onclick={() => selectPaymentMethod('point')}
						>
							Punto
						</Button>
					</ButtonGroup>
				</div>
			</div>

			<!-- Payment Reference (if transfer) -->
			{#if paymentMethod === 'transfer'}
				<div class="md:col-span-full">
					<Label for="payment-reference" class="mb-2 font-medium">Referencia</Label>
					<Input id="payment-reference" type="text" placeholder="Referencia" />
				</div>
				<!-- Table for cash-->
			{:else if paymentMethod === 'cash'}
				<div class="md:col-span-full">
					<div class="flex justify-between items-end w-full gap-5 mb-4">
						<div class="w-full">
							<Label for="reference" class="mb-2 font-medium">Serial del billete</Label>
							<Input id="reference" type="text" bind:value={serial} />
						</div>
						<div class="w-full">
							<Label for="amount" class="mb-2 font-medium">Monto</Label>
							<Select
								id="amount"
								bind:value={monto}
								items={[
									{ value: 1, name: '1$' },
									{ value: 2, name: '2$' },
									{ value: 5, name: '5$' },
									{ value: 10, name: '10$' },
									{ value: 20, name: '20$' },
									{ value: 50, name: '50$' },
									{ value: 100, name: '100$' }
								]}
							/>
						</div>
						<Button color="purple" class="w-full" outline onclick={agregarBillete}
							>Añadir billete</Button
						>
					</div>
					<Table>
						<TableHead>
							<TableHeadCell>Serial</TableHeadCell>
							<TableHeadCell>Monto</TableHeadCell>
							<TableHeadCell>Acciones</TableHeadCell>
						</TableHead>
						<TableBody class="divide-y">
							{#each billetes as billete, i}
								<TableBodyRow>
									<TableBodyCell>{billete.serial}</TableBodyCell>
									<TableBodyCell>{billete.monto}$</TableBodyCell>
									<TableBodyCell>
										<Button color="red" onclick={() => borrarBillete(i)} size="xs" outline>
											<TrashBinOutline class="w-5 h-5" />
										</Button>
									</TableBodyCell>
								</TableBodyRow>
							{/each}
						</TableBody>
					</Table>
				</div>
			{/if}
		</form>

		<!-- Modal Footer -->
		{#snippet footer()}
			<div class="flex justify-between items-center w-full">
				<div>
					<Button color="alternative" onclick={closePaymentModal}>Cancelar</Button>
					<Button color="primary" onclick={() => form?.requestSubmit()} disabled={!isFormValid}>
						<CreditCardOutline class="mr-2 h-5 w-5" />
						Realizar Pago
					</Button>
				</div>
				<ToastContainer />
			</div>
		{/snippet}
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
		box-shadow:
			0 10px 15px -3px rgba(0, 0, 0, 0.1),
			0 4px 6px -2px rgba(0, 0, 0, 0.05);
	}

	:global(.flatpickr-day.selected) {
		background: #9333ea !important;
		border-color: #9333ea !important;
	}

	:global(.flatpickr-day:hover) {
		background: #f3e8ff !important;
	}
</style>
