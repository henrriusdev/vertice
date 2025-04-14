<script lang="ts">
  import { enhance } from '$app/forms';
  import DataTable from '$lib/componentes/DataTable.svelte';
  import { Button, Modal, Input, Select } from 'flowbite-svelte';
  import { PenOutline, TrashBinOutline } from 'flowbite-svelte-icons';
  import type { PageData } from './$types';
  import type { Materia } from '../../../app';

  let { data }: { data: PageData } = $props();
  let showModal = $state(false);
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
    prelacion: '',
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
        id: '', nombre: '', prelacion: '', unidad_credito: 0, hp: 0, ht: 0,
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
    <Button onclick={() => openModal()} class="btn btn-primary">Crear Materia</Button>
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
  <form method="POST" use:enhance bind:this={formEl} action={editMode ? `/coordinador/materias/${selectedId}` : '/coordinador/materias'}>
    <div class="grid grid-cols-2 gap-4">
      <Input name="id" bind:value={form.id} placeholder="Código" class="input" required />
      <Input name="nombre" bind:value={form.nombre} placeholder="Nombre" class="input" required />
      <Input name="prelacion" bind:value={form.prelacion} placeholder="Prelación" class="input" />
      <Input name="unidad_credito" type="number" bind:value={form.unidad_credito} placeholder="UC" class="input" required />
      <Input name="hp" type="number" bind:value={form.hp} placeholder="Horas Prácticas" class="input" required />
      <Input name="ht" type="number" bind:value={form.ht} placeholder="Horas Teóricas" class="input" required />
      <Input name="semestre" type="number" bind:value={form.semestre} placeholder="Semestre" class="input" required />
      
      <Select name="id_carrera" placeholder="Carrera" bind:value={form.id_carrera} class="select" required items={data.carreras.map((c) => ({ value: c.id, name: c.nombre }))}>
      </Select>
      
      <Input name="ciclo" bind:value={form.ciclo} placeholder="Ciclo" class="input" required />
      <Input name="modalidad" bind:value={form.modalidad} placeholder="Modalidad" class="input" />
      <Input name="maximo" type="number" bind:value={form.maximo} placeholder="Max. Estudiantes" class="input" />
      
      <Select name="id_docente" placeholder="Docente" bind:value={form.id_docente} class="select" items={data.docentes.map((d) => ({ value: d.id, name: d.nombre }))}>
      </Select>
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
      <Button type="button" color="secondary" size="sm" onclick={addHorario}>+ Agregar Horario</Button>
      <input type="hidden" name="horarios" value={JSON.stringify(form.horarios)} />
    </div>

  </form>
  <div slot="footer">
    <Button type="button" color="secondary" onclick={() => showModal = false}>Cancelar</Button>
    <Button type="submit" color="primary" onclick="{() => formEl.requestSubmit()}">{editMode ? 'Actualizar' : 'Guardar'}</Button>
  </div>
</Modal>
