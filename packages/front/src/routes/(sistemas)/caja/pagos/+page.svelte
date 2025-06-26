<script lang="ts">
        import { Button } from 'flowbite-svelte';
        import { goto } from '$app/navigation';
</script>

<div class="flex flex-col items-center gap-6 mt-8">
        <Button color="blue" size="lg" on:click={() => goto('/caja/pagos/registrar')}>
                Registrar Pago
        </Button>
        <Button color="purple" size="lg" on:click={() => goto('/caja/pagos/reportes')}>
                Reportes de Pagos
        </Button>
</div>
