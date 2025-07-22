<script lang="ts">
    import {cedulaMask, DataTable} from '$lib';
    import {imask} from '@imask/svelte';
    import {Button, Input, Label, Modal, TableSearch, Datepicker} from 'flowbite-svelte';
    import ToastContainer from '$lib/componentes/ToastContainer.svelte';
    import {PenOutline, PlusOutline, TrashBinOutline} from 'flowbite-svelte-icons';
    import type {Docente} from '../../../app';
	import { resolver } from '$lib/utilidades/resolver';
	import { enhance } from '$app/forms';

    // Datos de la página
    let {data} = $props();

    // Estado para el modal
    let modalVisible = $state(false);
    let isEditing = $state(false);
    let searchTerm = $state('');
    let formEl: HTMLFormElement | undefined = $state();
    let docenteActual: Partial<{
        id: number;
        cedula: string;
        nombre: string;
        correo: string;
        fecha_ingreso: Date | undefined;
        titulo: string;
        usuario: number;
    }> = $state({
        cedula: '',
        nombre: '',
        correo: '',
        fecha_ingreso: new Date(),
        titulo: '',
        usuario: 0,
    });


    $effect(() => {
        if (!modalVisible) {
            docenteActual = {};
        }
    });

    $effect(() => {
        if (data.docentes) {
            docentesFiltrados =
                data?.docentes.filter(
                    (est) =>
                        est?.dedicacion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        est?.titulo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        est.fecha_ingreso.toLowerCase().includes(searchTerm.toLowerCase())
                ) ?? [];
        }
    });

    let docentes: Docente[] = $state(data.docentes);
    // Filtrar por carrera si es coordinador
    let docentesFiltrados = $derived(
        docentes.filter(
            (est) =>
                est?.dedicacion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                est?.titulo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                est.fecha_ingreso.toLowerCase().includes(searchTerm.toLowerCase())
        ) ?? []
    );

    // Función para abrir el modal en modo edición
    function editarDocente(docente: any) {
        docenteActual = {...docente};
        isEditing = true;
        modalVisible = true;
    }

    // Función para abrir el modal en modo creación
    function crearDocente() {
        isEditing = false;
        modalVisible = true;
    }

    function handleSubmit() {
        return resolver(() => {
            modalVisible = false;
        });    
    }
</script>

<div class="w-full">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Docentes</h1>
        <Button color="blue" onclick={crearDocente}>
            <PlusOutline class="mr-2 h-5 w-5"/>
            Registrar
        </Button>
    </div>
    <div class="mb-4">
        <TableSearch bind:inputValue={searchTerm} placeholder="Buscar por nombre, cédula o correo..."/>
    </div>

        {#snippet actions(row: Docente)}
    <div class="flex gap-2">
        <Button size="xs" color="light" onclick={() => editarDocente(row)}>
            <PenOutline class="w-4 h-4"/>
        </Button>
        <form action="?/delete" method="POST">
            <input type="hidden" name="cedula" value={row.cedula}/>
            <Button size="xs" color="red" type="submit">
                <TrashBinOutline class="w-4 h-4"/>
            </Button>
        </form>
    </div>
{/snippet}
<DataTable data={docentesFiltrados} {actions}></DataTable>

    <Modal title={isEditing ? 'Editar Docente' : 'Nuevo Docente'} bind:open={modalVisible} size="lg">
        <form action={isEditing ? '?/edit' : '?/create'} use:enhance={handleSubmit} method="POST" bind:this={formEl} class="min-h-[520px]">
            {#if isEditing}
                <input type="hidden" name="id_docente" value={docenteActual!.id}/>
                <input type="hidden" name="id" value={docenteActual!?.usuario}/>
            {/if}

            <div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
                <div class="md:col-span-2">
                    <Label for="cedula" class="mb-2">Cédula</Label>
                    <input
                            id="cedula"
                            name="cedula"
                            placeholder="Ingrese la cédula"
                            value={docenteActual?.cedula || ''}
                            oninput={(e) => {
                                if (docenteActual) docenteActual.cedula = e.currentTarget.value;
                            }}
                            required
                            use:imask={cedulaMask as any}
                            class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
                    />

                </div>
                <div class="md:col-span-2">
                    <Label for="nombre" class="mb-2">Nombre Completo</Label>
                    <Input
                            id="nombre"
                            name="nombre"
                            placeholder="Ingrese el nombre completo"
                            value={docenteActual!.nombre}
                            required
                    />
                </div>
                <div class="md:col-span-2">
                    <Label for="correo" class="mb-2">Correo Electrónico</Label>
                    <Input
                            id="correo"
                            name="correo"
                            type="email"
                            placeholder="correo@ejemplo.com"
                            value={docenteActual?.correo}
                            required
                    />
                </div>
                <div class="md:col-span-2">
                    <Label for="titulo" class="mb-2">Titulo</Label>
                    <Input
                            id="titulo"
                            name="titulo"
                            placeholder="Ingrese el titulo"
                            value={docenteActual!.titulo}
                            required
                    />
                </div>
                <div class="md:col-span-2 z-50">
                    <Label for="fecha_ingreso" class="mb-2">Fecha de ingreso</Label>
                    <Datepicker
                            id="fecha_ingreso"
                            availableTo={new Date()}
                            bind:value={docenteActual.fecha_ingreso}
                            placeholder="Seleccione una fecha"
                            translationLocale="es-VE"
                            dateFormat={{ year: 'numeric', month: '2-digit', day: '2-digit' }}
                    />
                    <input type="hidden" name="fecha_ingreso" value={(docenteActual.fecha_ingreso as Date | undefined)?.toISOString().split('T')[0] ?? ''}/>
                </div>
            </div>
        </form>
        {#snippet footer()}
            <div class="flex justify-between items-center w-full">
                <div>
                    <Button type="button" color="alternative" onclick={() => (modalVisible = false)}>Cancelar</Button>
                    <Button type="submit" color="primary" onclick={() => formEl!.requestSubmit()}>{isEditing ? 'Actualizar' : 'Guardar'}</Button>
                </div>
                <ToastContainer />
            </div>
        {/snippet}
    </Modal>
</div>
