<script lang="ts">
        import { Button, Card, Heading, Label, Select, Datepicker } from 'flowbite-svelte';
        import { FileLinesOutline } from 'flowbite-svelte-icons';
        import { enhance } from '$app/forms';
        import { resolver } from '$lib/utilidades/resolver';

        let reportType = $state('dia');
        let paymentSelection = $state('todos');
        let reportDate: Date | { from?: Date; to?: Date } | undefined = $state(new Date());
</script>

<div class="w-full flex justify-center mt-8">
        <Card class="p-6 w-full max-w-xl">
                <Heading tag="h2" class="text-2xl font-bold text-blue-600 mb-6">Reportes de pagos</Heading>

                <form
                        method="POST"
                        action="?/generarReporte"
                        use:enhance={({ formData }) => {
                                formData.append('tipo', reportType);
                                formData.append('filtro', paymentSelection);
                                if (reportType === 'dia') {
                                        formData.append('fecha', (reportDate as Date)?.toISOString().split('T')[0]);
                                }
                                if (reportType === 'fechas' || reportType === 'monto') {
                                        formData.append('fi', (reportDate as any).from.toISOString().split('T')[0]);
                                        formData.append('ff', (reportDate as any).to.toISOString().split('T')[0]);
                                }
                                return resolver(() => {});
                        }}
                        class="space-y-6"
                >
                        <div>
                                <Label for="report-type" class="mb-2">Seleccione su tipo de reporte</Label>
                                <Select id="report-type" bind:value={reportType} items={[
                                        { value: 'dia', name: 'Día' },
                                        { value: 'fechas', name: 'Entre fechas especificas' },
                                        { value: 'monto', name: 'Montos totales' }
                                ]} />
                        </div>

                        <div>
                                <Label for="payment-selection" class="mb-2">
                                        ¿Cuáles pagos desea que estén en el reporte?
                                </Label>
                                <Select
                                        id="payment-selection"
                                        bind:value={paymentSelection}
                                        items={[
                                                { value: 'todos', name: 'Todos' },
                                                { value: 'transferencia', name: 'Transferencias' },
                                                { value: 'efectivo', name: 'Efectivo' },
                                                { value: 'punto', name: 'Punto de venta' }
                                        ]}
                                />
                        </div>

                        <div>
                                <Label for="report-date" class="mb-2">Fecha de pagos</Label>
                                <Datepicker bind:value={reportDate} dateRange={reportType !== 'dia'} availableTo={new Date()} locale="es"
                                placeholder="Seleccione una fecha" />
                        </div>

                        <Button color="primary" size="lg" class="w-full" disabled={!reportDate} type="submit">
                                <FileLinesOutline class="mr-2 h-5 w-5" />
                                Generar reporte
                        </Button>
                </form>
        </Card>
</div>
