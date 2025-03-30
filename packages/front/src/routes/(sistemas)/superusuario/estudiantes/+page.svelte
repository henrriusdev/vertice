<script lang="ts">
  import { onMount } from 'svelte';
  import { enhance } from '$app/forms';
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    TableSearch,
    Button,
    Badge,
    Avatar,
    Modal,
    Label,
    Input,
    Select,
    Textarea,
    Spinner,
    Tabs,
    TabItem,
    Checkbox,
    Pagination,
    Alert
  } from 'flowbite-svelte';
  import {
    PenOutline,
    TrashBinOutline,
    PlusOutline,
    CheckCircleOutline,
    ExclamationCircleOutline
  } from 'flowbite-svelte-icons';

  // Datos de la página
  export let data;
  export let form;

  // Estado para el modal
  let modalVisible = false;
  let isEditing = false;
  let searchTerm = '';
  let currentPage = 1;
  const pageSize = 10;
  let estudianteActual: any = {};
  let showAlert = false;
  let alertMessage = '';
  let alertType: 'success' | 'error' = 'success';

  // Función para mostrar alerta
  function mostrarAlerta(mensaje: string, tipo: 'success' | 'error') {
    alertMessage = mensaje;
    alertType = tipo;
    showAlert = true;
    setTimeout(() => {
      showAlert = false;
    }, 5000);
  }

  // Procesar respuesta del formulario
  $: if (form) {
    if (form.success) {
      modalVisible = false;
      mostrarAlerta(form.message, 'success');
    } else if (form.error) {
      mostrarAlerta(form.error, 'error');
    }
  }

  // Filtrar estudiantes por término de búsqueda
  $: estudiantesFiltrados = data.estudiantes.filter(
    (est: any) =>
      est.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      est.cedula.toLowerCase().includes(searchTerm.toLowerCase()) ||
      est.correo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Paginación
  $: totalPages = Math.ceil(estudiantesFiltrados.length / pageSize);
  $: paginatedEstudiantes = estudiantesFiltrados.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  // Función para abrir el modal en modo edición
  function editarEstudiante(estudiante: any) {
    estudianteActual = { ...estudiante };
    if (typeof estudianteActual.carrera === 'object') {
      estudianteActual.carrera = estudianteActual.carrera.id;
    }
    isEditing = true;
    modalVisible = true;
  }

  // Función para abrir el modal en modo creación
  function crearEstudiante() {
    estudianteActual = {
      cedula: '',
      nombre: '',
      correo: '',
      activo: true,
      semestre: 1,
      carrera: 1,
      promedio: 0,
      direccion: '',
      fecha_nac: '',
      sexo: 'M'
    };
    isEditing = false;
    modalVisible = true;
  }

  // Calcular edad automáticamente al cambiar fecha de nacimiento
  function calcularEdad(fechaNacimiento: string): number {
    if (!fechaNacimiento) return 0;
    
    const hoy = new Date();
    const fechaNac = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - fechaNac.getFullYear();
    const mes = hoy.getMonth() - fechaNac.getMonth();
    
    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
      edad--;
    }
    
    return edad;
  }

  // Actualizar edad cuando cambia la fecha de nacimiento
  $: edad = calcularEdad(estudianteActual.fecha_nac);
</script>

<div class="w-full">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold">Estudiantes</h1>
    <Button color="blue" on:click={crearEstudiante}>
      <PlusOutline class="mr-2 h-5 w-5" />
      Nuevo Estudiante
    </Button>
  </div>

  <!-- Alertas -->
  {#if showAlert}
    <Alert 
      color={alertType === 'success' ? 'green' : 'red'} 
      dismissable 
      bind:open={showAlert}
      class="mb-4"
    >
      <svelte:fragment slot="icon">
        {#if alertType === 'success'}
          <CheckCircleOutline class="h-5 w-5" />
        {:else}
          <ExclamationCircleOutline class="h-5 w-5" />
        {/if}
      </svelte:fragment>
      {alertMessage}
    </Alert>
  {/if}

  <div class="mb-4">
    <TableSearch bind:value={searchTerm} placeholder="Buscar por nombre, cédula o correo..." />
  </div>

  <Table striped={true} hoverable={true}>
    <TableHead>
      <TableHeadCell>Foto</TableHeadCell>
      <TableHeadCell>Nombre</TableHeadCell>
      <TableHeadCell>Cédula</TableHeadCell>
      <TableHeadCell>Correo</TableHeadCell>
      <TableHeadCell>Carrera</TableHeadCell>
      <TableHeadCell>Semestre</TableHeadCell>
      <TableHeadCell>Promedio</TableHeadCell>
      <TableHeadCell>Estado</TableHeadCell>
      <TableHeadCell>Acciones</TableHeadCell>
    </TableHead>
    <TableBody>
      {#each paginatedEstudiantes as estudiante}
        <TableBodyRow>
          <TableBodyCell>
            <Avatar src={estudiante.ruta_foto} size="md" rounded />
          </TableBodyCell>
          <TableBodyCell>{estudiante.nombre}</TableBodyCell>
          <TableBodyCell>{estudiante.cedula}</TableBodyCell>
          <TableBodyCell>{estudiante.correo}</TableBodyCell>
          <TableBodyCell>
            {typeof estudiante.carrera === 'object' ? estudiante.carrera.nombre : ''}
          </TableBodyCell>
          <TableBodyCell>{estudiante.semestre}</TableBodyCell>
          <TableBodyCell>
            <Badge 
              color={estudiante.promedio >= 9 ? 'green' : estudiante.promedio >= 7 ? 'blue' : 'red'}
            >
              {estudiante.promedio.toFixed(1)}
            </Badge>
          </TableBodyCell>
          <TableBodyCell>
            <Badge color={estudiante.activo ? 'green' : 'red'}>
              {estudiante.activo ? 'Activo' : 'Inactivo'}
            </Badge>
          </TableBodyCell>
          <TableBodyCell>
            <div class="flex space-x-2">
              <Button size="xs" color="light" on:click={() => editarEstudiante(estudiante)}>
                <PenOutline class="h-4 w-4" />
              </Button>
              <form action="?/delete" method="POST" use:enhance>
                <input type="hidden" name="id" value={estudiante.id} />
                <Button size="xs" color="red" type="submit">
                  <TrashBinOutline class="h-4 w-4" />
                </Button>
              </form>
            </div>
          </TableBodyCell>
        </TableBodyRow>
      {/each}
      {#if paginatedEstudiantes.length === 0}
        <TableBodyRow>
          <TableBodyCell colspan="9" class="text-center py-4">
            No se encontraron estudiantes
          </TableBodyCell>
        </TableBodyRow>
      {/if}
    </TableBody>
  </Table>

  <!-- Paginación -->
  {#if totalPages > 1}
    <div class="flex justify-center mt-4">
      <Pagination
        {totalPages}
        bind:currentPage
        showControls={true}
        class="mt-4"
      />
    </div>
  {/if}

  <!-- Modal para crear/editar estudiante -->
  <Modal title={isEditing ? 'Editar Estudiante' : 'Nuevo Estudiante'} bind:open={modalVisible} size="xl">
    <form 
      action={isEditing ? "?/edit" : "?/create"} 
      method="POST" 
      use:enhance={() => {
        return async ({ result }) => {
          if (result.type === 'success') {
            modalVisible = false;
            mostrarAlerta(isEditing ? 'Estudiante actualizado exitosamente' : 'Estudiante creado exitosamente', 'success');
          }
        };
      }}
    >
      {#if isEditing}
        <input type="hidden" name="id" value={estudianteActual.id} />
      {/if}

      <Tabs style="underline">
        <TabItem open title="Información Personal">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <Label for="cedula" class="mb-2">Cédula</Label>
              <Input 
                id="cedula" 
                name="cedula"
                placeholder="Ingrese la cédula" 
                value={estudianteActual.cedula} 
                required 
                color={form?.errores?.cedula ? 'red' : undefined}
                helperText={form?.errores?.cedula}
              />
            </div>
            <div>
              <Label for="nombre" class="mb-2">Nombre Completo</Label>
              <Input 
                id="nombre" 
                name="nombre"
                placeholder="Ingrese el nombre completo" 
                value={estudianteActual.nombre} 
                required 
                color={form?.errores?.nombre ? 'red' : undefined}
                helperText={form?.errores?.nombre}
              />
            </div>
            <div>
              <Label for="correo" class="mb-2">Correo Electrónico</Label>
              <Input 
                id="correo" 
                name="correo"
                type="email" 
                placeholder="correo@ejemplo.com" 
                value={estudianteActual.correo} 
                required 
                color={form?.errores?.correo ? 'red' : undefined}
                helperText={form?.errores?.correo}
              />
            </div>
            <div>
              <Label for="fecha_nac" class="mb-2">Fecha de Nacimiento</Label>
              <Input 
                id="fecha_nac" 
                name="fecha_nac"
                type="date" 
                value={estudianteActual.fecha_nac} 
                required 
                color={form?.errores?.fecha_nac ? 'red' : undefined}
                helperText={form?.errores?.fecha_nac}
              />
            </div>
            <div>
              <Label for="edad" class="mb-2">Edad</Label>
              <Input id="edad" type="number" value={edad} disabled />
            </div>
            <div>
              <Label for="sexo" class="mb-2">Sexo</Label>
              <Select 
                id="sexo" 
                name="sexo"
                value={estudianteActual.sexo} 
                required
                color={form?.errores?.sexo ? 'red' : undefined}
                helperText={form?.errores?.sexo}
              >
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
              </Select>
            </div>
            <div class="md:col-span-2">
              <Label for="direccion" class="mb-2">Dirección</Label>
              <Textarea 
                id="direccion" 
                name="direccion"
                placeholder="Ingrese la dirección completa" 
                value={estudianteActual.direccion} 
                rows={3} 
                color={form?.errores?.direccion ? 'red' : undefined}
                helperText={form?.errores?.direccion}
              />
            </div>
            <div class="flex items-center">
              <Checkbox 
                id="activo" 
                name="activo"
                checked={estudianteActual.activo} 
              />
              <Label for="activo" class="ml-2">Usuario Activo</Label>
            </div>
          </div>
        </TabItem>
        <TabItem title="Información Académica">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <Label for="carrera" class="mb-2">Carrera</Label>
              <Select 
                id="carrera" 
                name="carrera"
                value={estudianteActual.carrera} 
                required
                color={form?.errores?.carrera ? 'red' : undefined}
                helperText={form?.errores?.carrera}
              >
                {#each data.carreras as carrera}
                  <option value={carrera.id}>{carrera.nombre}</option>
                {/each}
              </Select>
            </div>
            <div>
              <Label for="semestre" class="mb-2">Semestre</Label>
              <Select 
                id="semestre" 
                name="semestre"
                value={estudianteActual.semestre} 
                required
                color={form?.errores?.semestre ? 'red' : undefined}
                helperText={form?.errores?.semestre}
              >
                {#each Array(10) as _, i}
                  <option value={i + 1}>{i + 1}° Semestre</option>
                {/each}
              </Select>
            </div>
            <div>
              <Label for="promedio" class="mb-2">Promedio</Label>
              <Input 
                id="promedio" 
                name="promedio"
                type="number" 
                min="0" 
                max="10" 
                step="0.1" 
                value={estudianteActual.promedio} 
                required 
                color={form?.errores?.promedio ? 'red' : undefined}
                helperText={form?.errores?.promedio}
              />
            </div>
          </div>
        </TabItem>
      </Tabs>

    </form>
    <svelte:fragment slot="footer">
      <Button color="blue" type="submit">
        {isEditing ? 'Actualizar' : 'Guardar'}
      </Button>
      <Button color="light" on:click={() => (modalVisible = false)}>Cancelar</Button>
    </svelte:fragment>
  </Modal>
</div>