<script lang="ts">
  import { enhance } from '$app/forms';
  import DataTable from '$lib/componentes/DataTable.svelte';
  import { Button, Modal, Input, Select, Label, MultiSelect } from 'flowbite-svelte';
  import { PenOutline, PlusOutline, TrashBinOutline } from 'flowbite-svelte-icons';
  import type { PageData } from './$types';
  import type { Materia } from '../../../app';

  let { data }: { data: PageData } = $props();
  let showModal = $state(true);
  let editMode = $state(false);
  let selectedId = $state('');

  const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

  interface Form {
    id: number;
    nombre: string;
    prelacion: string;
    unidad_credito: number;
    hp: number;
    ht: number;
    semestre: number;
    id_carrera: string;
    ciclo: string;
    modalidad: string;
    maximo: number;
    id_docente: string;
    horarios: { dia: string; inicio: string; fin: string }[]
  }
  
  let form = $state({
    id: '',
    nombre: '',
    prelacion: [] as (string | number)[],
    unidad_credito: 0,
    hp: 0,
    ht: 0,
    semestre: 1,
    id_carrera: '',
    ciclo: '',
    modalidad: '',
    maximo: 0,
    id_docente: '',
    horarios: [] as { dia: string; inicio: string; fin: string }[]
  });

  let formEl: HTMLFormElement;

  function openModal(materia: Materia | null = null) {
    if (materia) {
      form = { ...materia };
      editMode = true;
      selectedId = materia.id;
    } else {
      form = {
        id: '', nombre: '', prelacion: [], unidad_credito: 0, hp: 0, ht: 0,
        semestre: 1, id_carrera: '', ciclo: '', modalidad: '', maximo: 0,
        id_docente: '', horarios: []
      };
      editMode = false;
      selectedId = '';
    }
    showModal = true;
  }

  function addHorario() {
    form.horarios.push({ dia: 'Lunes', inicio: '08:00', fin: '10:00' });
  }

  function removeHorario(index: number) {
    form.horarios.splice(index, 1);
  }
</script>

<!-- Tabla de materias -->
<div class="p-4">
  <div class="flex justify-between items-center mb-4">
    <h1 class="text-xl font-bold">Materias</h1>
    <Button onclick={() => openModal()} class="btn btn-primary"><PlusOutline class="h-5 w-5 mr-4"/>Crear Materia</Button>
  </div>

  {#snippet action(row: Materia)}
  <div class="flex justify-between items-center">
    <Button pill class="p-1.5!" size="xs" color="light" onclick={() => openModal(row)}>
      <PenOutline class="w-5 h-5" />
    </Button>
    <form action="?/delete" method="POST">
      <input type="hidden" name="id" value={row.id} />
      <Button pill class="p-1.5!" size="xs" color="red" type="submit">
        <TrashBinOutline class="w-5 h-5" />
      </Button>
    </form>
  </div>
  {/snippet}

  <DataTable data={data.materias} actions={action} />
</div>

<!-- Modal de creación/edición -->
<Modal bind:open={showModal} size="lg">
  <div slot="header">{editMode ? 'Editar Materia' : 'Crear Materia'}</div>
  <form method="POST" use:enhance bind:this={formEl} action={editMode ? `?/edit` : '?/create'}>
    <div class="grid grid-cols-4 gap-4">
      <div class="col-span-2">
        <Label for="id" class="mb-2">Código</Label>
        <Input id="id"  name="id" bind:value={form.id} class="input" required readonly={editMode} />
      </div>
      <div class="col-span-2">
        <Label for="nombre" class="mb-2">Nombre</Label>
        <Input name="nombre" bind:value={form.nombre} class="input" required />
      </div>
      <div>
        <Label for="unidad_credito" class="mb-2">Unidades de crédito</Label>
        <Input id="unidad_credito" name="unidad_credito" type="number" bind:value={form.unidad_credito} class="input" required />
      </div>
      <div>
        <Label for="hp" class="mb-2">Horas prácticas</Label>
        <Input id="hp" name="hp" type="number" bind:value={form.hp} class="input" required />
      </div>
      <div>
        <Label for="ht" class="mb-2">Horas Teóricas</Label>
        <Input id="ht" name="ht" type="number" bind:value={form.ht} class="input" required />
      </div>
      <div>
        <Label for="semestre" class="mb-2">Semestre</Label>
        <Input id="semestre" name="semestre" type="number" bind:value={form.semestre} class="input" required />
      </div>
      <div class="col-span-3">
        <Label for="id_carrera" class="mb-2">Carrera</Label>
        <Select id="id_carrera" name="id_carrera" bind:value={form.id_carrera} class="select" required items={data.carreras.map((c) => ({ value: c.id, name: c.nombre }))} placeholder="Seleccione"></Select>
      </div>
      <div>
        <Label for="modalidad" class="mb-2">Modalidad</Label>
        <Select id="modalidad" name="modalidad" bind:value={form.modalidad} class="input" items={[{value:'presencial',name:'Presencial'},{value:'virtual',name:'Virtual'}]} placeholder="Seleccione" />
      </div>
      <div class="col-span-3">
        <Label for="id_docente" class="mb-2">Docente</Label>
        <Select id="id_docente" name="id_docente" placeholder="Seleccione" bind:value={form.id_docente} class="select" items={data.docentes.map((d) => ({ value: d.id, name: d.nombre }))}></Select>
      </div>
      <div>
        <Label for="maximo" class="mb-2">Máximo de estudiantes</Label>
        <Input id="maximo" name="maximo" type="number" bind:value={form.maximo} class="input" />
      </div>
      <div class="col-span-4">
        <Label for="prelacion" class="mb-2">Prelación</Label>
        <MultiSelect id="prelacion" name="prelacion" bind:value={form.prelacion} class="input" items={[]} />
      </div>
    </div>

    <div class="mt-4">
      <h2 class="font-bold mb-2">Horarios</h2>
      {#each form.horarios as h, i}
        <div class="flex gap-2 mb-2">
          <Select bind:value={h.dia} class="select">
            {#each dias as d}
              <option>{d}</option>
            {/each}
          </Select>
          <Input type="time" bind:value={h.inicio} class="input" />
          <Input type="time" bind:value={h.fin} class="input" />
          <Button type="button" color="red" size="sm" class="p-1" onclick={() => removeHorario(i)}>✕</Button>
        </div>
      {/each}
      <Button type="button" color="primary" outline size="sm" onclick={addHorario}><PlusOutline class="h-5 w-5 mr-2"/> Agregar Horario</Button>
      <input type="hidden" name="horarios" value={JSON.stringify(form.horarios)} />
    </div>

  </form>
  <div slot="footer">
    <Button type="button" color="alternative" onclick={() => showModal = false}>Cancelar</Button>
    <Button type="submit" color="primary" onclick={() => formEl.requestSubmit()}>{editMode ? 'Actualizar' : 'Guardar'}</Button>
  </div>
</Modal>
