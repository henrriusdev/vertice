<script lang="ts">
  import {enhance} from '$app/forms';
  import {goto} from '$app/navigation';
  import {DataTable, ConfirmDeleteModal} from '$lib/componentes';
  import {resolver} from '$lib/utilidades/resolver';
  import type {SubmitFunction} from '@sveltejs/kit';
  import {Button, Input, Label, Modal, MultiSelect, Select} from 'flowbite-svelte';
  import ToastContainer from '$lib/componentes/ToastContainer.svelte';
  import {
    CalendarMonthOutline,
    InfoCircleOutline,
    PenOutline,
    PlusOutline,
    TrashBinOutline,
    UsersGroupOutline
  } from 'flowbite-svelte-icons';
  import type {Horario, Materia} from '../../../app';
  import type {PageData} from './$types';

  interface Form {
    id: string;
    nombre: string;
    prelacion: (string | number)[];
    unidad_credito: number;
    hp: number;
    ht: number;
    semestre: number;
    id_carrera: string;
    ciclo: string;
    maximo: number;
    id_docente: string;
    horarios: Horario[];
  }

  const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

  let form: Form = $state({
    id: '',
    nombre: '',
    prelacion: [],
    unidad_credito: 0,
    hp: 0,
    ht: 0,
    semestre: 1,
    id_carrera: '',
    ciclo: '',
    maximo: 0,
    id_docente: '',
    horarios: []
  });

  let formEl: HTMLFormElement;
  let horarios: Horario[] = $state([]);
  let {data}: { data: PageData } = $props();
  let showModal = $state(false);
  let showHorario = $state(false);
  let editMode = $state(false);
  let filtroCarrera: number | null = $state(data.rol === 'coordinador' ? data.carrera_id : null);
  let filtroDocente: number | null = $state(null);
  let filtroSemestre = $state('');
  let searchTerm = $state('');
  let showAyuda = $state(false);
  // Estado para el modal de confirmación de eliminación
  let deleteModalOpen = $state(false);
  let selectedMateriaForDelete: Materia | null = $state(null);

  // Opciones de prelación calculadas dinámicamente
  let opcionesPrelacion = $derived.by(() => {
    return data.materias
      .filter(
        (m) => m.id_carrera == form.id_carrera && m.semestre < form.semestre && m.id !== form.id
      )
      .map((m) => ({value: m.id, name: m.nombre}));
  });

  const materiasFiltradas = $derived(
    data.materias.filter((mat) => {
      const matchCarrera = !filtroCarrera || mat.id_carrera === filtroCarrera;
      const matchDocente = !filtroDocente || mat.id_docente === filtroDocente;
      const matchSemestre = !filtroSemestre || mat.semestre === +filtroSemestre;

      const matchSearch = (() => {
        if (!searchTerm.trim()) return true;
        try {
          const fixedExpr = searchTerm
            .replace(
              /([a-zA-Z_]+)\s*==?\s*([a-zA-Z_]+)/g,
              (_, field, value) => `${field} == "${value}"`
            )
            .replace(/<>/g, '!=')
            .replace(/=/g, '==');

          return Function('mat', `with (mat) { return ${fixedExpr} }`)(mat);
        } catch {
          return [mat.nombre, mat.id].some((v) =>
            v.toLowerCase().includes(searchTerm.toLowerCase())
          );
        }
      })();
      return matchCarrera && matchDocente && matchSemestre && matchSearch;
    })
  );

  function openModal(materia: Materia | null = null) {
    if (materia) {
      form = {...materia};
      editMode = true;
    } else {
      form = {
        id: '',
        nombre: '',
        prelacion: [],
        unidad_credito: 0,
        hp: 0,
        ht: 0,
        semestre: 1,
        id_carrera: '',
        ciclo: '',
        maximo: 30,
        id_docente: '',
        horarios: []
      };
      editMode = false;
    }
    showModal = true;
  }

  function addHorario() {
    form.horarios.push({dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00'});
  }

  function removeHorario(index: number) {
    form.horarios.splice(index, 1);
  }

  function openHorario(row: Materia) {
    horarios = row.horarios;
    showHorario = true;
  }

  // Función para abrir el modal de eliminación
  function confirmarEliminarMateria(materia: Materia) {
    selectedMateriaForDelete = materia;
    deleteModalOpen = true;
  }

  function searchName(key: 'id_docente' | 'id_carrera', value: number): string {
    if (key === 'id_docente') {
      return data.docentes.find((d) => d.id === value)?.nombre || '';
    }

    if (key === 'id_carrera') {
      return data.carreras.find((c) => c.id === value)?.nombre || '';
    }

    return '';
  }

  const handleSubmit: SubmitFunction = () => {
    return resolver(() => (showModal = false));
  };
</script>

<!-- Tabla de materias -->
<div class="flex justify-between items-center mb-4">
    <h1 class="text-2xl font-bold">Materias</h1>
    {#if ['coordinador', 'administrador'].includes(data.rol.toLowerCase())}
        <Button onclick={() => openModal()} class="btn btn-primary"
        >
            <PlusOutline class="h-5 w-5 mr-4"/>
            Crear Materia
        </Button
        >
    {/if}
</div>

<div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
    <div>
        <Label>Carrera</Label>
        <Select
                bind:value={filtroCarrera}
                items={[
				{ value: '', name: 'Todas' },
				...data.carreras.map((c) => ({ value: c.id, name: c.nombre }))
			]}
        />
    </div>
    <div>
        <Label>Docente</Label>
        <Select
                bind:value={filtroDocente}
                items={[
				{ value: '', name: 'Todos' },
				...data.docentes.map((d) => ({ value: d.id, name: d.nombre }))
			]}
        />
    </div>
    <div>
        <Label>Semestre</Label>
        <Select
                bind:value={filtroSemestre}
                items={[
				{ value: '', name: 'Todos' },
				...Array(10)
					.fill(null)
					.map((_, i) => ({ value: `${i + 1}`, name: `${i + 1}°` }))
			]}
        />
    </div>
    <div class="col-span-2">
        <Label>Búsqueda o condición</Label>
        <Input bind:value={searchTerm} placeholder="Nombre, código o expresión...">
            {#snippet right()}
                <Button
                        color="primary"
                        size="xs"
                        title="Ayuda"
                        class="p-2!"
                        onclick={() => (showAyuda = true)}
                >
                    <InfoCircleOutline class="w-6 h-6"/>
                </Button>
            {/snippet}
        </Input>
    </div>
</div>

{#snippet action(row: Materia)}
    <div class="flex justify-between items-center">
        {#if ['coordinador', 'administrador'].includes(data.rol.toLowerCase())}
            <Button pill class="p-1.5!" size="xs" color="light" onclick={() => openModal(row)}>
                <PenOutline class="w-5 h-5"/>
            </Button>
            <Button pill class="p-1.5!" size="xs" color="red" onclick={() => confirmarEliminarMateria(row)}>
                <TrashBinOutline class="w-5 h-5"/>
            </Button>
        {:else if ['control', 'superusuario', 'coordinador'].includes(data.rol.toLowerCase())}
            <Button
                    pill
                    class="p-1.5!"
                    size="xs"
                    color="primary"
                    onclick={() => goto(`/materias/${row.id}`)}
            >
                <UsersGroupOutline class="w-5 h-5"/>
            </Button>
        {/if}
        <Button pill class="p-1.5!" size="xs" color="alternative" onclick={() => openHorario(row)}>
            <CalendarMonthOutline class="w-5 h-5"/>
        </Button>
    </div>
{/snippet}

<DataTable data={materiasFiltradas} actions={action} onSearch={searchName}/>

<!-- Modal de creación/edición -->
<Modal bind:open={showModal} size="lg">
    {#snippet header()}
        <div>{editMode ? 'Editar Materia' : 'Crear Materia'}</div>
    {/snippet}
    <form
            method="POST"
            use:enhance={handleSubmit}
            bind:this={formEl}
            action={editMode ? `?/edit` : '?/create'}
    >
        <div class="grid grid-cols-4 gap-4">
            <div class="col-span-2">
                <Label for="id" class="mb-2">Código</Label>
                <Input id="id" name="id" bind:value={form.id} class="input" required readonly={editMode}/>
            </div>
            <div class="col-span-2">
                <Label for="nombre" class="mb-2">Nombre</Label>
                <Input name="nombre" bind:value={form.nombre} class="input" required/>
            </div>
            <div>
                <Label for="unidad_credito" class="mb-2">Unidades de crédito</Label>
                <Input
                        id="unidad_credito"
                        name="unidad_credito"
                        type="number"
                        bind:value={form.unidad_credito}
                        class="input"
                        required
                />
            </div>
            <div>
                <Label for="hp" class="mb-2">Horas prácticas</Label>
                <Input id="hp" name="hp" type="number" bind:value={form.hp} class="input" required/>
            </div>
            <div>
                <Label for="ht" class="mb-2">Horas Teóricas</Label>
                <Input id="ht" name="ht" type="number" bind:value={form.ht} class="input" required/>
            </div>
            <div>
                <Label for="semestre" class="mb-2">Semestre</Label>
                <Input
                        id="semestre"
                        name="semestre"
                        type="number"
                        bind:value={form.semestre}
                        class="input"
                        required
                />
            </div>
            <div class="col-span-3">
                <Label for="id_carrera" class="mb-2">Carrera</Label>
                <Select
                        id="id_carrera"
                        name="id_carrera"
                        bind:value={form.id_carrera}
                        class="select"
                        required
                        items={data.carreras.map((c) => ({ value: c.id, name: c.nombre }))}
                        placeholder="Seleccione"
                ></Select>
                <Input type="hidden" name="id_carrera" bind:value={form.id_carrera}/>
            </div>
            <div class="col-span-3">
                <Label for="id_docente" class="mb-2">Docente</Label>
                <Select
                        id="id_docente"
                        name="id_docente"
                        placeholder="Seleccione"
                        bind:value={form.id_docente}
                        class="select"
                        items={data.docentes.map((d) => ({ value: d.id, name: d.nombre }))}
                ></Select>
                <input type="hidden" name="id_docente" bind:value={form.id_docente}/>
            </div>
            <div>
                <Label for="maximo" class="mb-2">Máximo de estudiantes</Label>
                <Input id="maximo" name="maximo" type="number" bind:value={form.maximo} class="input"/>
            </div>
            <div class="col-span-4">
                <Label for="prelacion" class="mb-2">Prelación</Label>
                <MultiSelect
                        id="prelacion"
                        dropdownClass="z-[99999]!"
                        name="prelacion"
                        bind:value={form.prelacion}
                        items={opcionesPrelacion}
                        disabled={form.semestre < 2}
                        placeholder="Seleccione las prelaciones"
                />
            </div>
        </div>

        <div class="mt-4">
            <h2 class="font-bold mb-2">Horarios</h2>
            {#each form.horarios as h, i}
                <div class="flex gap-2 mb-2">
                    <Select bind:value={h.dia} class="select min-w-[15%]">
                        {#each dias as d}
                            <option>{d}</option>
                        {/each}
                    </Select>
                    <Input type="time" bind:value={h.hora_inicio} class="input"/>
                    <Input type="time" bind:value={h.hora_fin} class="input"/>
                    <Button type="button" color="red" size="sm" class="p-1" onclick={() => removeHorario(i)}
                    >✕
                    </Button
                    >
                </div>
            {/each}
            <Button type="button" color="primary" outline size="sm" onclick={addHorario}
            >
                <PlusOutline class="h-5 w-5 mr-2"/>
                Agregar Horario
            </Button
            >
            <input type="hidden" name="horarios" value={JSON.stringify(form.horarios)}/>
        </div>
    </form>
    {#snippet footer()}
        <div class="flex justify-between items-center w-full">
            <div>
                <Button type="button" color="alternative" onclick={() => (showModal = false)}
                >Cancellar
                </Button
                >
                <Button type="submit" color="primary" onclick={() => formEl.requestSubmit()}
                >{editMode ? 'Actualizar' : 'Guardar'}</Button
                >
            </div>
            <ToastContainer/>
        </div>
    {/snippet}
</Modal>
<Modal bind:open={showHorario} size="md">
    {#snippet header()}
        <h3 class="text-2xl font-bold">Horario de la materia seleccionada</h3>
    {/snippet}
    <DataTable
            data={horarios.map((h) => ({
			dia: h.dia,
			'Hora de inicio': h.hora_inicio,
			'Hora de finalización': h.hora_fin
		}))}
    />
</Modal>
<Modal bind:open={showAyuda} size="md">
    {#snippet header()}
        <h3 class="text-lg font-bold">Guía de expresiones</h3>
    {/snippet}
    <ul class="list-disc list-inside space-y-1">
        <li><code>ht &gt; 4</code> → Horas teóricas mayores a 4</li>
        <li><code>hp &lt;= 5</code> → Horas prácticas menores o iguales a 5</li>
        <li><code>maximo != 30</code> → Máximo de estudiantes distinto de 30</li>
        <li><code>semestre == 9</code> → Solo materias del 9° semestre</li>
        <li><code>nombre == 'mate'</code> → Nombre contiene "mate"</li>
    </ul>
    {#snippet footer()}
        <div>
            <Button onclick={() => (showAyuda = false)}>Cerrar</Button>
        </div>
    {/snippet}
</Modal>

<!-- Modal de confirmación de eliminación -->
<ConfirmDeleteModal
    bind:open={deleteModalOpen}
    title="Eliminar Materia"
    message="¿Estás seguro de que deseas eliminar la materia {selectedMateriaForDelete?.nombre}? Esta acción no se puede deshacer."
    action="?/delete"
    formData={{ id: selectedMateriaForDelete?.id || '' }}
    onSuccess={() => {
        selectedMateriaForDelete = null;
    }}
/>
