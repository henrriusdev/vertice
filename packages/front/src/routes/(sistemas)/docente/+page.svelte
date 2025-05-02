<script lang="ts">
  import {GrillaHorario} from '$lib';

  let {data} = $props();

  const materias = $derived(data.materiasAsignadas);
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-6">Hola de nuevo, {data.nombre}!</h1>
  <GrillaHorario {materias} docente />
</div>
