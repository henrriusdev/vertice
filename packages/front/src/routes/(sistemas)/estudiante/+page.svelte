<script lang="ts">
    import type { PageData } from './$types';
    import { goto } from '$app/navigation';
    import { 
        Table, 
        TableBody, 
        TableBodyCell, 
        TableBodyRow, 
        TableHead, 
        TableHeadCell, 
        Card, 
        Button, 
        Alert, 
        Badge 
    } from 'flowbite-svelte';

    let { data, inscripcion = true }: { data: PageData, inscripcion: boolean } = $props();
    
    // Datos dummy para simular materias inscritas
    const materiasInscritas = [
        { 
            materia: 'Cálculo Diferencial', 
            docente: 'Dr. Alejandro Méndez', 
            dias: 'Lunes, Miércoles', 
            horario: '08:00 - 10:00' 
        },
        { 
            materia: 'Programación Orientada a Objetos', 
            docente: 'Ing. María González', 
            dias: 'Martes, Jueves', 
            horario: '10:00 - 12:00' 
        },
        { 
            materia: 'Física I', 
            docente: 'Dr. Carlos Ramírez', 
            dias: 'Lunes, Viernes', 
            horario: '14:00 - 16:00' 
        }
    ];

    // Función para redirigir a la página de inscripción
    const irAInscripcion = () => {
        goto('/estudiante/inscripcion');
    };
</script>

<div class="w-full p-4">
    <h2 class="text-2xl font-bold mb-4">
        Hola de nuevo, {data.nombre}!
    </h2>
    
    <div class="flex items-center mb-6">
        <h3 class="text-lg font-semibold mr-3">Estado de inscripción:</h3>
        {#if inscripcion}
            <Badge color="green">Abierta</Badge>
        {:else}
            <Badge color="red">Cerrada</Badge>
        {/if}
    </div>

    <Card padding="xl" size="none">
        <h3 class="text-xl font-semibold mb-4">Materias Inscritas</h3>
        
        {#if materiasInscritas.length > 0}
            <Table striped={true} hoverable={true}>
                <TableHead>
                    <TableHeadCell>Materia</TableHeadCell>
                    <TableHeadCell>Docente</TableHeadCell>
                    <TableHeadCell>Días</TableHeadCell>
                    <TableHeadCell>Horario</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each materiasInscritas as materia}
                        <TableBodyRow>
                            <TableBodyCell>{materia.materia}</TableBodyCell>
                            <TableBodyCell>{materia.docente}</TableBodyCell>
                            <TableBodyCell>{materia.dias}</TableBodyCell>
                            <TableBodyCell>{materia.horario}</TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        {:else}
            <Alert color="primary">
                No tienes materias inscritas actualmente
            </Alert>
        {/if}
        
        {#if inscripcion}
            <div class="mt-6">
                <Button color="primary" on:click={irAInscripcion}>
                    Ir a inscripción de materias
                </Button>
            </div>
        {/if}
    </Card>
</div>