<script lang="ts">
  import {goto} from '$app/navigation';
  import {page} from '$app/state';
  import type {Peticion} from '$lib/types';
  import {
    Label,
    PaginationNav,
    Select,
    type SelectOptionType,
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell
  } from 'flowbite-svelte';
  import {ArrowLeftOutline, ArrowRightOutline} from 'flowbite-svelte-icons';

  let {
    data = [],
    actions,
    onSearch
  } = $props<{
    data: any[];
    actions?: (row: any) => ReturnType<import('svelte').Snippet>;
    onSearch?: (key: string, value: string) => string;
  }>();

  const pageOptions: SelectOptionType<number>[] = [
    {value: 3, name: '3'},
    {value: 10, name: '10'},
    {value: 25, name: '25'},
    {value: 50, name: '50'}
  ];

  // lee de URL
  let currentPage = $derived(parseInt(page.url.searchParams.get('page') || '1'));
  let perPage = $derived(parseInt(page.url.searchParams.get('perPage') || '25'));

  let total = $derived(data.length);
  const headers = $derived(
    Object.keys(data[0] || {})
      .filter(
        (k) => k !== 'id' && !['usuario', 'activo', 'billetes', 'horarios', 'notas', 'cambiar_clave', 'pregunta_configurada'].includes(k)
      )
      // place nombre first, and then the rest
      .sort((a, b) =>
        a === 'nombre' ? -1 : b === 'nombre' ? 1 : 0
      )
  );
  let start = $derived((currentPage - 1) * perPage + 1);
  let end = $derived(Math.min(start + perPage - 1, total));
  let paginated = $derived(data.slice(start - 1, end));
  let totalPages = $derived(Math.ceil(total / perPage));

  // navegación reactiva
  function goTo(p: number) {
    goto(`?page=${p}&perPage=${perPage}`, {replaceState: true});
  }

  function changePerPage() {
    goto(`?page=1&perPage=${perPage}`, {replaceState: true});
  }

  function isPeticion(row: any): row is Peticion {
    return (
      row &&
      typeof row === 'object' &&
      'peticion' in row &&
      typeof row.peticion === 'object' &&
      'estado' in row.peticion
    );
  }
</script>

<div class="w-full">
    <div class="overflow-x-auto">
        <Table striped hoverable shadow>
            <TableHead>
                {#each headers as h}
                    {#if h.includes('id_')}
                        <TableHeadCell>{h.replace('id_', '')}</TableHeadCell>
                    {:else if h === 'maximo'}
                        <TableHeadCell>Máximo de Estudiantes</TableHeadCell>
                    {:else}
                        <TableHeadCell>{h.replace(/_/g, ' ')}</TableHeadCell>
                    {/if}
                {/each}
                {#if paginated.some(isPeticion)}
                    <TableHeadCell>Estado</TableHeadCell>
                {/if}
                {#if actions}
                    <TableHeadCell>Acciones</TableHeadCell>
                {/if}
            </TableHead>

            <TableBody class="divide-y">
                {#each paginated as row}
                    <TableBodyRow>
                        {#each headers.length ? headers : Object.keys(row) as h}
                            {#if ['nombre'].includes(h)}
                                <TableBodyCell class="capitalize">{row[h]}</TableBodyCell>
                            {:else if (h.includes('id_') && row[h]) || typeof row[h] === 'object'}
                                <TableBodyCell>{onSearch(h, row[h])}</TableBodyCell>
                            {:else}
                                <TableBodyCell>{row[h]}</TableBodyCell>
                            {/if}
                        {/each}
                        {#if isPeticion(row)}
                            <TableBodyCell class="capitalize">{row.peticion.estado}</TableBodyCell>
                        {/if}
                        {#if actions}
                            <TableBodyCell>
                                {@render actions(row)}
                            </TableBodyCell>
                        {/if}
                    </TableBodyRow>
                {/each}
                {#if paginated.length === 0}
                    <TableBodyRow>
                        <TableBodyCell colspan={headers.length + 1} class="text-center py-4">
                            No se encontraron resultados
                        </TableBodyCell>
                    </TableBodyRow>
                {/if}
            </TableBody>
        </Table>
    </div>

    <div class="flex items-center justify-between mt-4 flex-wrap gap-2">
        <Label for="perPage" class="flex items-center">
            Filas por página
            <Select
                    onchange={changePerPage}
                    bind:value={perPage}
                    items={pageOptions}
                    id="perPage"
                    class="ml-2 w-20"
            />
        </Label>

        <span class="text-sm text-gray-700 dark:text-gray-400">
			Mostrando <b>{start}</b> - <b>{end}</b> de <b>{total}</b>
		</span>

        <PaginationNav {currentPage} {totalPages} onPageChange={goTo}>
            {#snippet prevContent()}
                <span class="sr-only">Anterior</span>
                <ArrowLeftOutline class="h-5 w-5"/>
            {/snippet}
            {#snippet nextContent()}
                <span class="sr-only">Siguiente</span>
                <ArrowRightOutline class="h-5 w-5"/>
            {/snippet}
        </PaginationNav>
    </div>
</div>
